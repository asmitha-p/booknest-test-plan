"""Shared fixtures: mock server, WebDriver (setup/teardown), logged-in session,
and automatic screenshot capture when a test fails."""
import datetime
import pathlib
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Make project root importable when running `pytest` from any directory
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import settings                      # noqa: E402
from pages.dashboard_page import DashboardPage   # noqa: E402
from pages.login_page import LoginPage           # noqa: E402
import run_mock_server                           # noqa: E402

SCREENSHOT_DIR = ROOT / "screenshots"


@pytest.fixture(scope="session", autouse=True)
def mock_server():
    """SETUP (once per run): start the simulated web app. TEARDOWN: stop it."""
    server = None
    if settings.START_MOCK_SERVER:
        server = run_mock_server.start_in_background()
    yield
    if server:
        server.shutdown()
        server.server_close()


def _build_driver():
    if settings.BROWSER == "firefox":
        opts = FirefoxOptions()
        if settings.HEADLESS:
            opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)
    opts = ChromeOptions()
    if settings.HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)  # Selenium Manager fetches the driver


@pytest.fixture
def driver():
    """SETUP: fresh browser per test (isolated session storage).
    TEARDOWN: always quit the browser, even if the test failed."""
    drv = _build_driver()
    drv.implicitly_wait(0)  # we use explicit waits only; never mix the two
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Precondition helper: returns a driver already authenticated."""
    LoginPage(driver).open().login(**settings.VALID_USER)
    DashboardPage(driver).wait_for_url_contains("dashboard.html")
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Error handling: on failure, save a screenshot named after the test."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if drv:
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{item.name}_{stamp}.png".replace("[", "_").replace("]", "")
            try:
                drv.save_screenshot(str(SCREENSHOT_DIR / name))
            except Exception as exc:  # never let screenshot problems hide the real failure
                print(f"Could not capture screenshot: {exc}")

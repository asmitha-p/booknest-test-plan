"""BasePage: shared Selenium helpers used by every page object.

All waiting is *explicit* (WebDriverWait) - no time.sleep() - which keeps tests
fast and avoids flaky failures.
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


class BasePage:
    path = ""  # overridden by subclasses, e.g. "/login.html"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.DEFAULT_TIMEOUT)

    # ---- navigation -------------------------------------------------------
    def open(self):
        self.driver.get(f"{settings.BASE_URL}{self.path}")
        return self

    def wait_for_url_contains(self, fragment: str):
        self.wait.until(EC.url_contains(fragment))

    # ---- element helpers --------------------------------------------------
    def find(self, locator):
        """Wait until the element is visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.find(locator).text.strip()

    def is_visible(self, locator, timeout: int = 2) -> bool:
        """True if the element becomes visible within `timeout` seconds."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

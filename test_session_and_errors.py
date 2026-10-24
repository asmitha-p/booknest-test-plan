"""Workflow 5 & 6 - Session handling (logout, protected pages) and error pages."""
import pytest
from selenium.webdriver.common.by import By

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_logout_returns_to_login_page(logged_in_driver):
    DashboardPage(logged_in_driver).logout()

    assert "login.html" in logged_in_driver.current_url


def test_protected_page_not_accessible_after_logout(logged_in_driver):
    DashboardPage(logged_in_driver).logout()
    # Try to reach a protected page directly after the session ended
    logged_in_driver.get(f"{settings.BASE_URL}/dashboard.html")

    LoginPage(logged_in_driver).wait_for_url_contains("login.html")
    assert "login.html" in logged_in_driver.current_url


@pytest.mark.negative
@pytest.mark.parametrize("page", ["dashboard.html", "products.html", "contact.html"])
def test_protected_pages_redirect_anonymous_user_to_login(driver, page):
    driver.get(f"{settings.BASE_URL}/{page}")

    LoginPage(driver).wait_for_url_contains("login.html")
    assert "login.html" in driver.current_url


@pytest.mark.negative
def test_unknown_url_shows_404_page(driver):
    driver.get(f"{settings.BASE_URL}/this-page-does-not-exist.html")

    heading = driver.find_element(By.ID, "error-title").text
    assert "404" in heading
    assert "Page Not Found" in heading

"""Workflow 1 - Authentication: valid login and invalid-credential handling."""
import pytest

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials_shows_dashboard(driver):
    LoginPage(driver).open().login(**settings.VALID_USER)

    dashboard = DashboardPage(driver)
    dashboard.wait_for_url_contains("dashboard.html")
    assert dashboard.welcome_text() == f"Welcome, {settings.VALID_USER['username']}"


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("testuser", "wrong-password", "Invalid username or password"),
        ("unknown", "Password123!", "Invalid username or password"),
        ("", "", "Username and password are required"),
        ("testuser", "", "Username and password are required"),
    ],
    ids=["wrong_password", "unknown_user", "both_empty", "missing_password"],
)
def test_login_with_invalid_input_shows_error(driver, username, password, expected_error):
    page = LoginPage(driver).open().login(username, password)

    assert page.error_message() == expected_error
    assert "login.html" in driver.current_url, "User must stay on the login page"

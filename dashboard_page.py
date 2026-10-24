"""Page object for /dashboard.html (also owns the shared navigation bar)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    path = "/dashboard.html"

    WELCOME = (By.ID, "welcome-message")
    NAV_PRODUCTS = (By.ID, "nav-products")
    NAV_CONTACT = (By.ID, "nav-contact")
    NAV_DASHBOARD = (By.ID, "nav-dashboard")
    LOGOUT = (By.ID, "logout-button")

    def welcome_text(self) -> str:
        return self.text_of(self.WELCOME)

    def go_to_products(self):
        self.click(self.NAV_PRODUCTS)
        self.wait_for_url_contains("products.html")

    def go_to_contact(self):
        self.click(self.NAV_CONTACT)
        self.wait_for_url_contains("contact.html")

    def go_to_dashboard(self):
        self.click(self.NAV_DASHBOARD)
        self.wait_for_url_contains("dashboard.html")

    def logout(self):
        self.click(self.LOGOUT)
        self.wait_for_url_contains("login.html")

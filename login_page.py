"""Page object for /login.html."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login.html"

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-button")
    ERROR = (By.ID, "login-error")

    def login(self, username: str, password: str):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

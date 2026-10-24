"""Page object for /contact.html."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    path = "/contact.html"

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    MESSAGE = (By.ID, "message")
    SUBMIT = (By.ID, "submit-button")
    SUCCESS = (By.ID, "success-message")
    NAME_ERROR = (By.ID, "name-error")
    EMAIL_ERROR = (By.ID, "email-error")
    MESSAGE_ERROR = (By.ID, "message-error")

    def fill_and_submit(self, name: str, email: str, message: str):
        self.type_text(self.NAME, name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.MESSAGE, message)
        self.click(self.SUBMIT)
        return self

    def error_text(self, locator) -> str:
        """Error divs are always in the DOM, so read text without waiting for visibility."""
        return self.driver.find_element(*locator).text.strip()

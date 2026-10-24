"""Page object for /products.html."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductsPage(BasePage):
    path = "/products.html"

    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    CARDS = (By.CSS_SELECTOR, ".product-card")
    NO_RESULTS = (By.ID, "no-results")

    def search(self, term: str):
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        return self

    def product_names(self) -> list:
        return [c.text for c in self.driver.find_elements(*self.CARDS)]

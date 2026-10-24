"""Workflow 4 - Product search: filtering results and the empty state."""
import pytest

from pages.products_page import ProductsPage


def test_product_list_shows_all_products_by_default(logged_in_driver):
    page = ProductsPage(logged_in_driver).open()
    assert len(page.product_names()) == 5


@pytest.mark.parametrize(
    "term, expected",
    [
        ("laptop", ["Laptop Stand", "Laptop Sleeve"]),
        ("KEYBOARD", ["Mechanical Keyboard"]),   # search must be case-insensitive
        ("usb", ["USB-C Hub"]),
    ],
)
def test_search_filters_results(logged_in_driver, term, expected):
    page = ProductsPage(logged_in_driver).open().search(term)
    assert page.product_names() == expected


@pytest.mark.negative
def test_search_with_no_match_shows_empty_message(logged_in_driver):
    page = ProductsPage(logged_in_driver).open().search("zzz-nonexistent")

    assert page.product_names() == []
    assert page.is_visible(page.NO_RESULTS)
    assert page.text_of(page.NO_RESULTS) == "No products found"

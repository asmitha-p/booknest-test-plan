"""Workflow 3 - Navigation: menu links route to the right pages."""
from pages.dashboard_page import DashboardPage
from pages.products_page import ProductsPage


def test_dashboard_navigates_to_products(logged_in_driver):
    DashboardPage(logged_in_driver).go_to_products()

    assert "products.html" in logged_in_driver.current_url
    assert logged_in_driver.title == "Products - DemoShop"


def test_dashboard_navigates_to_contact(logged_in_driver):
    DashboardPage(logged_in_driver).go_to_contact()

    assert "contact.html" in logged_in_driver.current_url
    assert logged_in_driver.title == "Contact - DemoShop"


def test_nav_bar_returns_to_dashboard_from_other_pages(logged_in_driver):
    ProductsPage(logged_in_driver).open()
    DashboardPage(logged_in_driver).go_to_dashboard()

    assert logged_in_driver.title == "Dashboard - DemoShop"


def test_browser_back_button_returns_to_previous_page(logged_in_driver):
    DashboardPage(logged_in_driver).go_to_contact()
    logged_in_driver.back()

    DashboardPage(logged_in_driver).wait_for_url_contains("dashboard.html")
    assert "dashboard.html" in logged_in_driver.current_url

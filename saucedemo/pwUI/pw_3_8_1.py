import pytest
from playwright.sync_api import sync_playwright
from saucedemo.pwUI.pages.login_page import LoginPage
from saucedemo.pwUI.pages.inventory_page import InventoryPage
from saucedemo.pwUI.pages.checkout_page import CheckoutPage


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=400)
    yield browser
    browser.close()
    playwright.stop()


def test_checkout_order(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckoutPage(page)

    login_page.login('standard_user', 'secret_sauce')
    inventory_page.add_first_item_to_cart()
    checkout_page.start_checkout()
    checkout_page.fill_checkout_form('John', 'Doe', '12345')
    checkout_page.finish_checkout()

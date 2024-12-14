#playwright, monolith code example
from playwright.sync_api import sync_playwright
import time

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000)
page = browser.new_page()
page.goto('https://www.saucedemo.com/')
page.type(selector='[id="user-name"]', text='standard_user', delay=50)
page.fill(selector='#password', value='secret_sauce')       # [id="password"]
page.click(selector='[data-test="login-button"]')         # [class='submit-button'] or ['.submit-button'] class="submit-button btn_action"
# page.click(selector='[class="submit-button btn_action"]')
# page.click(selector='.submit-button.btn_action')

page.wait_for_url('https://www.saucedemo.com/inventory.html', timeout=10000)
page.wait_for_selector('#inventory_container')

button_add_cart = '[data-test="add-to-cart-sauce-labs-backpack"]'
alt_locator_for_card = '.inventory_item a:has-text("Sauce Labs Backpack")'
card_button = '.inventory_item_description:has-text("Sauce Labs Backpack") button:has-text("Add to cart")'

page.is_visible(selector=button_add_cart)
page.is_enabled(selector=button_add_cart)
# page.click(selector=button_add_cart)
# page.click(selector=alt_locator_for_card)
page.click(card_button)
page.click('[data-test="shopping-cart-link"]')

page.wait_for_url('https://www.saucedemo.com/cart.html', timeout=10000)
button_checkout = '#checkout'

page.wait_for_selector(button_checkout)
page.is_visible(button_checkout)
page.is_enabled(button_checkout)
page.click(button_checkout)

page.wait_for_url('https://www.saucedemo.com/checkout-step-one.html')

page.fill(selector='#first-name', value='FirstName')
page.fill(selector='#last-name', value='LastName')
page.fill(selector='#postal-code', value='95462578')

page.click('[id="continue"][type="submit"]')

page.wait_for_url('https://www.saucedemo.com/checkout-step-two.html')
page.wait_for_selector('button:has-text("Finish")')
page.click('button:has-text("Finish")')

page.wait_for_url('https://www.saucedemo.com/checkout-complete.html')

# page.check('')    #TODO look for examples of check
time.sleep(5)

browser.close()
playwright.stop()

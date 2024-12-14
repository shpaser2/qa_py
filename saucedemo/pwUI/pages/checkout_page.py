from saucedemo.pwUI.pages.base_page import BasePage

class CheckoutPage(BasePage):
    _CHECKOUT_BUTTON_SELECTOR = '[id="checkout"]'
    _CONTINUE_BUTTON_SELECTOR = '[id="continue"][type="submit"]'
    _FINISH_BUTTON_SELECTOR = 'button:has-text("Finish")'
    _COMPLETE_CHECKOUT_SELECTOR = '[data-test="complete-header"]'
    _FIRST_NAME_SELECTOR = '#first-name'
    _LAST_NAME_SELECTOR = '#last-name'
    _POSTAL_CODE_SELECTOR = 'input[name="postalCode"]'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/checkout-step-one.html'

    def start_checkout(self):
        self.wait_for_selector_and_click(self._CHECKOUT_BUTTON_SELECTOR)
        self.assert_element_is_visible(self._FIRST_NAME_SELECTOR)

    def fill_checkout_form(self, first_name, last_name, postal_code):
        self.wait_for_selector_and_type(self._FIRST_NAME_SELECTOR, first_name)
        self.wait_for_selector_and_type(self._LAST_NAME_SELECTOR, last_name)
        self.wait_for_selector_and_type(self._POSTAL_CODE_SELECTOR, postal_code)
        self.assert_input_value(self._POSTAL_CODE_SELECTOR, postal_code)

    def finish_checkout(self):
        self.wait_for_selector_and_click(self._CONTINUE_BUTTON_SELECTOR)
        self.wait_for_selector_and_click(self._FINISH_BUTTON_SELECTOR)
        self.assert_element_is_visible(self._COMPLETE_CHECKOUT_SELECTOR)
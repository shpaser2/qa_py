from saucedemo.pwUI.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = ''

    USERNAME_SELECTOR = '#user-name'
    PASSWORD_SELECTOR = '#password'
    LOGIN_BUTTON_SELECTOR = '#login-button'

    def login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_text_present_on_page('Products')

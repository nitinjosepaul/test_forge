import time
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class LoginPage(BasePage):
    #Locators
    SIGN_IN_LINK_XPATH = "//a[@href='/login']"
    EMAIL_FIELD_ID = "email"
    PASSWORD_FIELD_ID = 'login-password'
    LOGIN_BUTTON_ID = 'login'
    INCORRECT_DETAILS_SPAN_ID = 'incorrectdetails'
    INCORRECT_DETAILS_SPAN_TEXT = "Incorrect login details"

    def click_sign_in_link(self):
        self.click_element(By.XPATH, self.SIGN_IN_LINK_XPATH)

    def enter_email(self, email):
        self.input_keys(By.ID, self.EMAIL_FIELD_ID, email)

    def enter_password(self, password):
        self.input_keys(By.ID, self.PASSWORD_FIELD_ID, password)

    def click_login_button(self):
        self.click_element(By.ID, self.LOGIN_BUTTON_ID)

    def login(self, email, password):
        self.click_sign_in_link()
        self.enter_email(email)
        self.enter_password(password)
        time.sleep(1)
        self.click_login_button()

    def is_incorrect_login_message_displayed(self, timeout=10):
        element = self.wait_for_element(By.ID, self.INCORRECT_DETAILS_SPAN_ID, timeout=timeout)
        return element.is_displayed() and element.text.strip() == self.INCORRECT_DETAILS_SPAN_TEXT

    def is_page_title_valid(self, expected_title):
        return self.verify_page_title(expected_title)
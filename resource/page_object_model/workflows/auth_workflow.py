from pages.home.dashboard_page import DashboardPage
from pages.home.login_page import LoginPage


class AuthWorkflow:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)

    def verify_login_successful(self, email, password):
        self.login_page.login(email, password)
        return self.dashboard_page.is_user_dropdown_present()

    def verify_login_failure(self, email, password):
        self.login_page.login(email, password)
        return self.login_page.is_incorrect_login_message_displayed()

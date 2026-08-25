from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    USER_DROPDOWN = "dropdownMenu1"

    def is_user_dropdown_present(self, timeout=10):
        dropdown_element = self.wait_for_element(By.ID, self.USER_DROPDOWN, timeout=timeout)
        return dropdown_element is not None

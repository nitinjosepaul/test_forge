import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utilities.logger import LogManager
from base.selenium_driver import SeleniumDriver


class BasePage():

    def __init__(self, driver):
        self.driver = driver
        self.logger = LogManager.get_logger()

    def get_element(self, by, locator):
        return self.driver.find_element(by, locator)

    def get_elements(self, by, locator):
        return self.driver.find_elements(by, locator)

    def get_element_if_present(self, by, locator):
        try:
            element_obj = self.get_element(by, locator)
            self.logger.debug(f"Element present with [by:{by}, locator:{locator}]")
            return True, element_obj
        except NoSuchElementException:
            self.logger.debug(f"Element not present with [by:{by}, locator:{locator}]")
            return False, None

    def check_element_presence(self, by, locator):
        present, _ = self.get_element_if_present(by, locator)
        return present

    def get_elements_if_present(self, by, locator):
        element_list = self.get_elements(by, locator)
        if element_list:
            self.logger.debug(
                f"{len(element_list)} elements present with [by:{by}, locator:{locator}]"
            )
            return True, element_list

        self.logger.debug(f"No element present with [by:{by}, locator:{locator}]")
        return False, None

    def check_elements_presence(self, by, locator):
        present, _ = self.get_elements_if_present(by, locator)
        return present

    def click_element(self, by, locator):
        element_obj = self.get_element(by, locator)
        element_obj.click()
        self.logger.debug(f"Clicked on element with [by:{by}, locator:{locator}]")
        time.sleep(1)

    def input_keys(self, by, locator, value):
        element_obj = self.get_element(by, locator)
        element_obj.send_keys(value)
        self.logger.debug(f"Sent {value} to element with [by:{by}, locator:{locator}]")
        time.sleep(1)

    def clear_input(self, by, locator):
        element_obj = self.get_element(by, locator)
        element_obj.clear()
        self.logger.debug(f"Cleared input field with [by:{by}, locator:{locator}]")
        time.sleep(1)

    def scroll_element_into_view(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

    def wait_for_element(self, by, locator, timeout=10, poll_frequency=1):
        element_obj = None

        try:
            self.driver.implicitly_wait(0)
            self.logger.debug(
                f"Waiting up to {timeout} seconds for element [by:{by}, locator:{locator}]"
            )
            wait = WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=poll_frequency,
                ignored_exceptions=[NoSuchElementException],
            )
            element_obj = wait.until(EC.visibility_of_element_located((by, locator)))
            self.logger.debug(f"Element became visible [by:{by}, locator:{locator}]")
        except TimeoutException:
            self.logger.debug(f"Element did not become visible [by:{by}, locator:{locator}]")
            raise
        finally:
            self.driver.implicitly_wait(10)

        return element_obj

    def verify_page_title(self, expected_title):
        actual_title = self.driver.title
        is_match = actual_title == expected_title
        self.logger.debug(
            f"Page title validation: expected='{expected_title}', actual='{actual_title}'"
        )
        return is_match

    def verifyPageTitle(self, expected_title):
        return self.verify_page_title(expected_title)

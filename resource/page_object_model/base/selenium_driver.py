import logging
import time
from selenium import webdriver

from tests.conftest import SESSION_DIR_ENV
from utilities.logger import LogManager
from utilities.screenshot import take_screenshot as _take_screenshot


class SeleniumDriver():

    def __init__(self, browser, base_url='https://www.letskodeit.com/practice', implicit_wait_time=10):

        self.logger: logging.Logger = LogManager.get_logger()
        self.base_url = base_url
        
        self.logger.debug(f"Initializing webdriver with {browser.capitalize()}")
        self.driver = self._initialize_driver(browser)

        self.driver.maximize_window()

        self.logger.debug(f"Setting implicit wait to {implicit_wait_time} seconds")
        self.driver.implicitly_wait(implicit_wait_time)

        if goto_practice_url:
            self.driver.get(base_url)

    def _initialize_driver(self, browser):
        browser = browser.lower()
        if browser == "chrome":
            return webdriver.Chrome()
        elif browser == "firefox":
            return webdriver.Firefox()
        elif browser == "edge":
            return webdriver.Edge()
        elif browser == "safari":
            return webdriver.Safari()
        else:
            self.logger.warning(f"Unknown browser: {browser}. Defaulting to Chrome")
            return webdriver.Chrome()

    def teardown(self):
        time.sleep(1)
        print("Quitting the launched browser")
        self.driver.quit()

    def get_driver(self):
        return self.driver

    def take_screenshot(self, test_name):
        filepath = _take_screenshot(self.driver, test_name)
        self.logger.debug(f"Screenshot saved as : {filepath}")
        return filepath
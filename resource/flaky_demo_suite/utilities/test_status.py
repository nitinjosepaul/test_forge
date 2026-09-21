"""
TestStatus — soft assertion utility for multi-step test verification.

Usage in a test:
    def test_something(self, test_status):
        test_status.mark(page.check_a(), "Check A")
        test_status.mark(page.check_b(), "Check B")
        test_status.mark_final("test_something", page.check_c(), "Check C")
"""
from traceback import print_stack

from utilities.logger import LogManager
from utilities.screenshot import take_screenshot


class TestStatus:

    def __init__(self, driver):
        """
        :param driver: Raw Selenium WebDriver instance (injected via fixture).
        """
        self.driver = driver
        self.logger = LogManager.get_logger()
        self._results: list[str] = []

    def mark(self, result, message: str):
        """
        Record a non-fatal verification checkpoint.
        Does NOT fail the test immediately — use mark_final to evaluate all results.
        """
        self._set_result(result, message)

    def mark_final(self, test_name: str, result, message: str):
        """
        Record the final verification checkpoint and evaluate the overall test result.
        Raises AssertionError if any previous mark() or this call recorded a FAIL.
        Must be called at least once per test.
        """
        self._set_result(result, message)

        if "FAIL" in self._results:
            self.logger.error(f"{test_name} ### TEST FAILED")
            self._results.clear()
            assert False, f"{test_name} failed one or more verifications"
        else:
            self.logger.info(f"{test_name} ### TEST SUCCESSFUL")
            self._results.clear()

    def _set_result(self, result, message: str):
        try:
            if result:
                self._results.append("PASS")
                self.logger.info(f"### VERIFICATION SUCCESSFUL: {message}")
            else:
                self._results.append("FAIL")
                self.logger.error(f"### VERIFICATION FAILED: {message}")
                self._capture_screenshot(message)
        except Exception:
            self._results.append("FAIL")
            self.logger.error("### Exception occurred during verification")
            self._capture_screenshot(message)
            print_stack()

    def _capture_screenshot(self, name: str):
        try:
            filepath = take_screenshot(self.driver, name)
            self.logger.debug(f"Failure screenshot saved: {filepath}")
        except Exception as e:
            self.logger.warning(f"Could not save screenshot: {e}")

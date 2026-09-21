import pytest


@pytest.mark.usefixtures("class_logger")
class BaseTest:

    @pytest.fixture(autouse=True)
    def setup_test_context(self, driver, test_status):
        self.driver = driver
        self.ts = test_status

import pytest

from tests.base_test import BaseTest
from workflows.auth_workflow import AuthWorkflow


class TestLogin(BaseTest):

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.auth_workflow = AuthWorkflow(driver)

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        login_failed = self.auth_workflow.verify_login_failure("wrong@email.com", "wrongpass")
        self.ts.mark_final("test_invalid_login", login_failed, "Incorrect login message displayed")

    @pytest.mark.run(order=2)
    def test_valid_login(self):
        login_successful = self.auth_workflow.verify_login_successful('test@email.com', 'abcabc')
        dashboard_present = self.auth_workflow.dashboard_page.is_user_dropdown_present()
        title_valid = self.auth_workflow.login_page.is_page_title_valid("Google")

        self.ts.mark(login_successful, "Login attempt succeeded")
        self.ts.mark(title_valid, "Page title is correct after login")
        self.ts.mark_final(
            "test_valid_login",
            dashboard_present,
            "Dashboard dropdown visible after login"
        )

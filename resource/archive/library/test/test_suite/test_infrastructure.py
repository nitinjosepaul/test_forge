from library.test.test_suite.base_test import BaseTest


class TestInfrastructure(BaseTest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        super().setup()

    def test_verify_dcdiag(self):
        pass

    def test_verify_pdc(self):
        pass

    def test_verify_maxofflinetimeindays(self):
        pass

    def test_verify_secure_channel(self):
        pass
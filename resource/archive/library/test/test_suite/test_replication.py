from library.test.test_suite.base_test import BaseTest


class TestReplication(BaseTest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        super().setup()

    def test_verify_replication_status(self):
        pass

    def test_verify_ou_replication(self):
        pass

    def test_verify_user_replication(self):
        pass

    def test_verify_gpo_replication(self):
        pass

    def test_verify_sysvol_folder_replication(self):
        pass

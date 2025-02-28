from library.test.test_suite.base_test import BaseTest


class TestDomainController(BaseTest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        super().setup()

    def test_verify_domain_admin_login(self):
        pass

    def test_verify_ad_services_running(self):
        pass
        # dc1_actual_root_domain = ADCommand.get_ad_root_domain_name()
        # expected_root_domain = self.adinstall_dict['Config']['Park']['ActiveDirectory']['DomainName']
        # assert dc1_actual_root_domain == expected_root_domain,\
        #     f"Expected RootDomain to be {expected_root_domain}, but got {dc1_actual_root_domain.get('RootDomain')}"
        #

    # To implement
    def test_verify_domain_name(self):
        pass
        # expected_root_domain = xmlparser.get_root_domain_name()
        # primary_dc_root_domain = self.primary_dc.ad_query.get_ad_root_domain_name()
        # assert primary_dc_root_domain == expected_root_domain, \
        #     f"Expected Primary DC RootDomain to be {expected_root_domain}, but got {primary_dc_root_domain.get('RootDomain')}"
        # dc2_root_domain = dc2.adcommands.get_ad_root_domain_name()
        # assert dc2_root_domain == expected_root_domain, \
        #     f"Expected DC1 RootDomain to be {expected_root_domain}, but got {dc2_root_domain.get('RootDomain')}"

    def test_verify_domain_controllers(self):
        raise AssertionError('Expected domain controller name is not matching with actual domain controller name')

    def test_verify_connectivity(self):
        raise ValueError('Invalid AD XML value for root OU')

    def test_verify_user_creation(self):
        pass

    def test_verify_ou_creation(self):
        pass

    def test_verify_group_creation(self):
        pass

    def test_verify_gpo_creation(self):
        pass
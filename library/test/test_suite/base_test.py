import logging

import config
from library.util.parser import read_xml_to_dict


class BaseTest:

    def __init__(self, **kwargs):
        self.primary_dc = kwargs['primary_domain_controller']
        self.secondary_dc = kwargs['secondary_domain_controller']
        self.ca = kwargs['certificate_authority']
        self.ms = kwargs['member_server']

    def setup(self):
        logging.info('Running setup')
        self.adinstall_dict = read_xml_to_dict(config.adinstall_xml_file_path)

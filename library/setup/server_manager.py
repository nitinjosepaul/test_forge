from library.util.parser import ServerINIParser
from library.setup.device.domain_controller import DomainController
from library.setup.device.certificate_authority import CertificateAuthority
from library.setup.device.member import MemberServer

from library.util.exception import InvalidADSetup


class ServerManager:

    def __init__(self):
        self.server_ini_parser = ServerINIParser()
        self.DC1 = self.DC2 = self.CA = self.MS = None
        self._initialize_servers()

    def _initialize_servers(self):
        self.DC1 = DomainController(**self.server_ini_parser.get_server_details(ServerINIParser.DC1_section_name))
        self.DC2 = DomainController(**self.server_ini_parser.get_server_details(ServerINIParser.DC2_section_name))
        self.CA = CertificateAuthority(**self.server_ini_parser.get_server_details(ServerINIParser.CA_section_name))
        self.MS = MemberServer(**self.server_ini_parser.get_server_details(ServerINIParser.MS_section_name))

    def get_execution_host(self):
        for dc in [self.DC1, self.DC2]:
            if dc.is_execution_host():
                return dc
        else:
            raise InvalidADSetup("Execution host is not set in Server INI file")

    def get_primary_domain_controller(self):
        for dc in [self.DC1, self.DC2]:
            if dc.is_primary():
                return dc
        else:
            raise InvalidADSetup("None of DCs set as primary in Server INI file")

    def get_secondary_domain_controller(self):
        domain_controllers = [self.DC1, self.DC2]
        domain_controllers.remove(self.get_primary_domain_controller())
        dc = domain_controllers[0]
        if not dc.is_primary():
            return dc
        else:
            raise InvalidADSetup("Both DCs are set as primary in Server INI file")

    def get_certificate_authority(self):
        return self.CA

    def get_member_server(self):
        return self.MS

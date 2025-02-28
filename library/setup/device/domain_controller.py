from library.setup.device.ad_server import ADServer
from library.setup.interface.dc_interface import DCInterface


class DomainController(ADServer):

    def __init__(self, execution_host, primary, **kwargs):
        self.execution_host = execution_host
        self.primary = primary
        super().__init__(**kwargs)
        self.dc_interface = DCInterface(self.powershell)

    def is_execution_host(self):
        return self.execution_host

    def is_primary(self):
        return self.primary

    #TODO : If primary is configured in ini file, no need to keep this method
    def set_as_primary(self):
        if self.is_primary():
            print(f"{self.hostname} is already the primary Domain Controller, continuing")
        else:
            self._primary = True
            print(f"{self.hostname} is set as the primary Domain Controller")
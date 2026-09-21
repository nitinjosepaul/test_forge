from library.util.powershell import PowerShell, PowershellRemote
from library.setup.interface.ad_interface import ADInterface


class ADServer:

    def __init__(self, hostname, ip, **kwargs):
        self.hostname = hostname
        self.ip = ip

        try:
            if self.execution_host:
                self.powershell = PowerShell()
            else:
                self.powershell = PowershellRemote(computer_name=hostname)
        except AttributeError:
            self.powershell = PowershellRemote(computer_name=hostname)

        self.ad_interface = ADInterface(self.powershell)

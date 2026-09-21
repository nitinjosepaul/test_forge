class ADCommand:

    # AD COMMANDS
    GET_AD_FOREST = "Get-ADForest"

    def __init__(self, powershell_obj):
        self.powershell_obj = powershell_obj

    def get_adforest(self):
        """
        Run the powershell command 'Get-ADForest'

        Returns:
        dict: The dictionary representation for 'Get-ADForest' output.
        """
        return self.powershell_obj.run_command(cls.GET_AD_FOREST)


class ADInterface(ADCommand):

    def get_ad_root_domain_name(self):
        return self.get_adforest().get('RootDomain')
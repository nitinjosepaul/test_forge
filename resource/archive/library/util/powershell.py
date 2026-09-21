import json
import subprocess
import logging


class PowerShell:

    def run_command(self, command, json_format=True, parse_output=True):
        """
        Executes a PowerShell command and returns the output

        Parameters:
        command (str): The PowerShell command to execute.
        json_format (bool): If True, add 'ConvertTo-Json' cmdlet to command
        parse_output (bool): If True, output returned will be a parsed dictionary, else string

        Returns:
        str|dict: Output of PowerShell command based on parse_output flag
        """
        if json_format:
            command = f'{command} | ConvertTo-Json'
        logging.debug(f'Run Powershell command : {command}')
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Command failed with error: {result.stderr}")
        logging.debug(f'Command Output : {result.stdout}')
        if parse_output:
            return self._parse_output(result.stdout, json_format)
        else:
            return result.stdout.strip()

    def _parse_output(self, output, json_format):
        """
        Converts the output of PowerShell command to a dictionary.

        Parameters:
        output (str): The output of the PowerShell command.

        Returns:
        dict: The dictionary representation of the output.
        """
        if json_format:
            try:
                json_output = json.loads(output)
            except json.JSONDecodeError as e:
                raise ValueError(f"Output is not valid JSON : {e})")
            return json_output
        else:
            try:
                # Removing extraneous characters and splitting lines
                output_lines = output.strip().split('\n')

                # Parsing the output to dictionary
                result_dict = {}
                for line in output_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        result_dict[key.strip()] = value.strip()
            except Exception as e:
                raise ValueError(f"Error processing output: {e}")
            return result_dict

    # #TODO Need to update the flags in above code
    # def run_powershell_command(command):
    #     try:
    #         ad_install.update_log("\nRunning command : " + command)
    #         result = subprocess.run(["powershell", "-Command", command],
    #                                 capture_output=True,
    #                                 text=True,
    #                                 check=True)
    #         ad_install.update_log(result.stdout)
    #     except subprocess.CalledProcessError as e:
    #         ad_install.update_log("An error Occured : " + str(e))


class PowershellRemote(PowerShell):

    def __init__(self, computer_name):
        self.computer_name = computer_name

    def run_command(self, command, json_format=True, parse_output=True):
        remote_command = "Invoke-Command " +\
                         "-ComputerName " + self.computer_name +\
                         "-ScriptBlock {" + command

        if json_format:
            remote_command += " | ConvertTo-Json}"
        else:
            remote_command += "}"

        return super().run_command(remote_command, json_format=False, parse_output=parse_output)


# def run_powershell_script():
#     ps_script = r"""
#     $username = 'Administrator'
#     $password = 'Testing@12345678'
#     $secpasswd = ConvertTo-SecureString $password -AsPlainText -Force
#     $cred = New-Object System.Management.Automation.PSCredential ($username, $secpasswd)
#
#     $computername = 'BDPK5DOMCTRL02'
#     $localscriptpath = "D:\PythonGUI\scripts\script1.ps1"
#     Invoke-Command -ComputerName $computername -Credential $cred -FilePath $localscriptpath"""
#
#     # Use subprocess to run the PowerShell script
#     process = subprocess.Popen(
#         ["powershell", "-Command", ps_script],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         bufsize=1,  # Line-buffered
#     )
#
#     # Print the output as it is generated
#     for line in iter(process.stdout.readline, ''):
#         ad_install.update_log(line)
#
#     # Capture the output and error (if any)
#     output, error = process.communicate()
#
#     # Check if there was an error
#     if process.returncode != 0:
#         raise PSExecutionException(f"Script Execution Failed\n"
#                                    f"Returncode : {process.returncode}\n"
#                                    f"Error: {error.strip()}")

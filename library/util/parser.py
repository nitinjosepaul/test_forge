import xmltodict
import configparser

import config
from library.util.exception import InvalidINIFile


def read_xml_to_dict(file_path):
    """
    Reads an XML file and converts it into a dictionary.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        dict: A dictionary representation of the XML content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
            data_dict = xmltodict.parse(xml_content)
        return data_dict
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class ServerINIParser:

    DC1_section_name = 'Domain Controller 1'
    DC2_section_name = 'Domain Controller 2'
    CA_section_name = 'Certificate Authority'
    MS_section_name = 'Member Server'

    def __init__(self):
        self.ini_file = config.server_ini_file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)

    def get_server_details(self, section_name):
        if section_name not in self.config.sections():
            raise ValueError(f'Section {section_name} not found in INI file')
        return self._parse_server_details(section_name)

    def _parse_server_details(self, section_name):
        details = {}
        for key, value in self.config[section_name].items():
            if key in ['execution_host', 'primary']:
                try:
                    details[key] = self.config.getboolean(section_name, key)
                except ValueError as e:
                    raise InvalidINIFile(f'Invalid value for {key} in {section_name} in INI file')
            else:
                details[key] = value
        return details




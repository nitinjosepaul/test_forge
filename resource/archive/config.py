import os

# Directory Paths
project_root_dir = os.getcwd()
log_dir = os.path.join(project_root_dir, 'log')
test_suite_dir = os.path.join(project_root_dir, 'library', 'test', 'test_suite')

#Configuration file paths
server_ini_file_path = os.path.join(project_root_dir, 'server.ini')
adinstall_xml_file_path = os.path.join(project_root_dir, 'resource', 'ActiveDirectory_BDPK5.xml')

# Execution status
EXECUTION_STATUS_IDLE = 'IDLE'
EXECUTION_STATUS_RUNNING = 'RUNNING'
EXECUTION_STATUS_COMPLETED = 'COMPLETED'

APPLICATION_NAME = 'ADTest Framework'
APPLICATION_VERSION = 'v0.1'



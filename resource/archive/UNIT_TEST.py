import logging
from library.util.log import Log
Log(console_logging=False)

###########################################################
# Testing TestExecutor
###########################################################
from library.test.test_executor import TestExecutor
te = TestExecutor()
suite_names = te.get_test_suite_names()
te.execute_test_suite(suite_names[0])
te.execute_test_suite(suite_names[1])

###########################################################
# Testing ServerManager
###########################################################
# from library.setup.server_manager import ServerManager
# sm = ServerManager()
# # logging.debug(sm.get_execution_host().hostname)
# logging.debug(sm.get_primary_domain_controller().hostname)
# logging.debug(sm.get_secondary_domain_controller().hostname)
# logging.debug(sm.get_certificate_authority().hostname)
# logging.debug(sm.get_member_server().hostname)

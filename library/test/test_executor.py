import os
import sys
import time
import logging
import inspect
import importlib

import config
from library.test.test_suite.base_test import BaseTest
from library.setup.server_manager import ServerManager
from library.util.exception import InvalidTestSuite


class TestExecutor:

    def __init__(self):
        self.server_manager = ServerManager()
        self.test_suites = {}
        self.test_result_counter = {}
        self._discover_test_suites()

    def _reset_test_result_counter(self):
        self.test_result_counter = {'PASS': 0,
                                    'FAIL': 0,
                                    'ERROR': 0}

    def _discover_test_suites(self):
        """
        Discover all test suites in 'test_suite' module and store details in a dictionary.
        A test suite is valid if:
        - It is inside a Python file starting with 'test_'
        - It is a class that starts with 'Test'
        - It inherits from 'BaseTest'
        """
        # Add test suite directory to system path
        sys.path.append(config.test_suite_dir)

        for suite_file in os.listdir(config.test_suite_dir):
            if suite_file.startswith("test_") and suite_file.endswith(".py"):
                module_name = suite_file[:-3]  # Remove '.py'

                # Import module using import_module()
                suite_module = importlib.import_module(module_name)

                # Find all valid test suite classes
                for suite_class_name, cls in inspect.getmembers(suite_module, inspect.isclass):
                    if suite_class_name.startswith("Test") and issubclass(cls, BaseTest):
                        suite_name = suite_class_name[4:]  # Extract suite name by removing 'Test' prefix
                        if suite_name:  # Ensure suite name is not empty
                            logging.debug(f'Identified test suite : {suite_name}')
                            self.test_suites[suite_name] = cls
                        else:
                            raise InvalidTestSuite("Please follow correct naming convention for Test Suite class.")

    def get_test_suite_names(self):
        return list(self.test_suites.keys())

    def get_test_suite_class(self, suite_name):
        suite_class = self.test_suites.get(suite_name)
        if not suite_class:
            raise InvalidTestSuite(f"Test suite '{suite_name}' not found.")
        return suite_class

    def get_test_cases(self, suite_name):
        """
        Get all test cases from a test suite by suite name.

        Args:
            suite_name (str): The name of the test suite.

        Returns:
            List of test methods.
        """
        return [func for name, func in inspect.getmembers(self.get_test_suite_class(suite_name), inspect.isfunction)
                if name.startswith("test_")]

    def get_test_case_count(self, suite_name):
        """
        Count the number of test cases in a test suite by suite name.

        Args:
            suite_name (str): The name of the test suite.

        Returns:
            int: Number of test cases in the suite.
        """
        return len(self.get_test_cases(suite_name))

    def execute_test_suite(self, suite_name, update_callback):
        """
        Execute all test cases in a test suite by suite name.

        Args:
            suite_name (str): The name of the test suite.
        """
        suite_class = self.get_test_suite_class(suite_name)

        # Reset test result counter
        self._reset_test_result_counter()

        # Record start time
        start_time = time.time()

        # Create an instance of the test suite class
        logging.info('*' * 40)
        update_callback(config.EXECUTION_STATUS_RUNNING, suite_name)
        logging.info(f'Running test suite : {suite_name}')
        suite_obj = suite_class(
            **{'primary_domain_controller': self.server_manager.get_primary_domain_controller(),
               'secondary_domain_controller': self.server_manager.get_secondary_domain_controller(),
               'certificate_authority': self.server_manager.get_certificate_authority(),
               'member_server': self.server_manager.get_member_server()}
        )

        # Call setup for test suite
        if hasattr(suite_obj, "setup"):
            try:
                logging.info(f"{suite_name}:setup")
                suite_obj.setup()
                logging.info(f"{suite_name}:setup completed successfully")
            except Exception as e:
                logging.error(f"{suite_name}:setup failed with error {str(e)}")
                return
            finally:
                logging.info('*' * 40)

        for test in self.get_test_cases(suite_name):
            update_callback(config.EXECUTION_STATUS_RUNNING, f"{suite_name}.{test.__name__}")
            time.sleep(2)  # TODO need to be removed
            try:
                test(suite_obj)  # Run the test case
                logging.info(f"{test.__name__}:PASS")
                self.test_result_counter['PASS'] += 1
            except AssertionError as e:
                logging.warning(f"{test.__name__}:FAIL")
                logging.debug(f"{type(e).__name__}:{e}")
                self.test_result_counter['FAIL'] += 1
            except Exception as e:
                logging.error(f"{test.__name__}:ERROR")
                logging.debug('', exc_info=True)
                self.test_result_counter['ERROR'] += 1

        # Calculate total execution time
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        logging.info('*' * 40)
        logging.info(f"Execution Summary")
        logging.info(f"Pass : {self.test_result_counter['PASS']}")
        logging.info(f"Fail : {self.test_result_counter['FAIL']}")
        logging.info(f"Error: {self.test_result_counter['ERROR']}")
        logging.info('*' * 40)

        update_callback(config.EXECUTION_STATUS_COMPLETED, execution_time=formatted_time)

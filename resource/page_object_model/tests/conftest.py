import os
import pytest
from pathlib import Path
from datetime import datetime

from utilities.logger import LogManager
from utilities.test_status import TestStatus
from base.selenium_driver import SeleniumDriver

SESSION_DIR_ENV = "POM_SESSION_DIR"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge, safari (default: chrome)"
    )

@pytest.fixture(scope="session", autouse=True)
def bootstrap_run_logger():
    #Create a session folder for all logs and screenshots
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path(__file__).resolve().parents[1] / "logs" / timestamp
    session_dir.mkdir(parents=True, exist_ok=True)
    os.environ[SESSION_DIR_ENV] = str(session_dir)

    run_log_path = session_dir / "main.log"

    LogManager(name="MAIN", main_log_file_path=str(run_log_path))
    logger = LogManager.get_logger()
    logger.info("*" * 50)
    logger.info("[SESSION START]")
    logger.info("*" * 50)
    logger.info("Session output folder: %s", session_dir)
    logger.info("Main run log file: %s", run_log_path)
    yield
    os.environ.pop(SESSION_DIR_ENV, None)
    logger.info("*" * 50)
    logger.info("[SESSION END]")
    logger.info("*" * 50)

@pytest.fixture(scope="session")
def logger():
    return LogManager.get_logger()

@pytest.fixture(scope="class")
def class_logger(request):
    request.cls.logger = LogManager.get_logger()


@pytest.fixture(scope="session")
def driver(request):
    base_url = "https://www.letskodeit.com/home"
    browser = request.config.getoption("--browser")
    selenium_driver = SeleniumDriver(browser=browser, base_url=base_url,implicit_wait_time=10)
    yield selenium_driver.get_driver()
    selenium_driver.teardown()


@pytest.fixture
def test_status(driver):
    """Function-scoped soft-assertion helper. Each test gets a fresh instance."""
    return TestStatus(driver)

import os
import re
from datetime import datetime
from pathlib import Path

from tests.conftest import SESSION_DIR_ENV


def take_screenshot(driver, name: str) -> str:
    """
    Save a screenshot of the current browser state.

    :param driver: Raw Selenium WebDriver instance.
    :param name: Label used in the filename (unsafe characters are sanitised).
    :return: Absolute path of the saved screenshot file.
    """
    session_dir_raw = os.environ.get(SESSION_DIR_ENV)
    if not session_dir_raw:
        raise RuntimeError(f"Environment variable '{SESSION_DIR_ENV}' is not set")

    session_dir = Path(session_dir_raw)
    if not session_dir.exists() or not session_dir.is_dir():
        raise FileNotFoundError(f"Session directory does not exist: {session_dir}")

    screenshots_dir = session_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(name)).strip("_")
    if not safe_name:
        raise ValueError("name must contain at least one valid character")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filepath = screenshots_dir / f"{safe_name}_{timestamp}.png"

    driver.save_screenshot(str(filepath))
    return str(filepath)

import re
from datetime import datetime
from pathlib import Path

from config.settings import ROOT_DIR

SCREENSHOT_DIR = ROOT_DIR / "screenshots"


def capture_screenshot(driver, name: str) -> Path:
    """Save a PNG of the current page as screenshots/<name>_<timestamp>.png."""
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^\w.-]", "_", name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = SCREENSHOT_DIR / f"{safe_name}_{timestamp}.png"
    driver.save_screenshot(str(path))
    return path

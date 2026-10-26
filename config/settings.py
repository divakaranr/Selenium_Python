"""Load run settings.

Precedence (highest first): CLI option -> environment variable -> config.yaml.
"""
import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "config.yaml"

SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    browser: str
    headless: bool
    window_size: tuple[int, int]
    explicit_wait: int
    page_load_timeout: int


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _parse_window_size(value: str) -> tuple[int, int]:
    width, height = str(value).lower().split("x")
    return int(width), int(height)


def load_settings(env=None, browser=None, headless=None, base_url=None) -> Settings:
    load_dotenv(ROOT_DIR / ".env")
    data = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))

    env = env or os.getenv("ENV") or data["default_env"]
    if env not in data["environments"]:
        raise ValueError(f"Unknown env '{env}'. Options: {list(data['environments'])}")
    cfg = {**data.get("defaults", {}), **data["environments"][env]}

    browser = (browser or os.getenv("BROWSER") or cfg["browser"]).lower()
    if browser not in SUPPORTED_BROWSERS:
        raise ValueError(f"Unsupported browser '{browser}'. Options: {SUPPORTED_BROWSERS}")

    if headless is None:
        headless = os.getenv("HEADLESS", cfg["headless"])

    return Settings(
        env=env,
        base_url=(base_url or os.getenv("BASE_URL") or cfg["base_url"]).rstrip("/"),
        browser=browser,
        headless=_to_bool(headless),
        window_size=_parse_window_size(cfg["window_size"]),
        explicit_wait=int(cfg["explicit_wait"]),
        page_load_timeout=int(cfg["page_load_timeout"]),
    )

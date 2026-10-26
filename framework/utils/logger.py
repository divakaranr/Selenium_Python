"""Logging setup.

Every framework logger writes to logs/run[-<worker>].log and propagates to the root
logger, so pytest's live logging (log_cli) shows the same messages on the console.
"""
import logging
import os

from config.settings import ROOT_DIR

LOG_DIR = ROOT_DIR / "logs"
_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_BASE_NAME = "ui"


def _configure_base_logger() -> logging.Logger:
    base = logging.getLogger(_BASE_NAME)
    if base.handlers:
        return base

    LOG_DIR.mkdir(exist_ok=True)
    # Separate file per pytest-xdist worker so parallel runs don't interleave writes.
    worker = os.getenv("PYTEST_XDIST_WORKER")
    log_file = LOG_DIR / (f"run-{worker}.log" if worker else "run.log")

    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter(_FORMAT))
    base.addHandler(handler)
    base.setLevel(logging.INFO)
    return base


def get_logger(name: str) -> logging.Logger:
    _configure_base_logger()
    return logging.getLogger(f"{_BASE_NAME}.{name}")

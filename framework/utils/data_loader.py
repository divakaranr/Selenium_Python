"""Read test data files from test_data/ (JSON, YAML or CSV), cached per file."""
import csv
import json
from functools import lru_cache

import yaml

from config.settings import ROOT_DIR

TEST_DATA_DIR = ROOT_DIR / "test_data"


@lru_cache(maxsize=None)
def load_data(filename: str):
    path = TEST_DATA_DIR / filename
    suffix = path.suffix.lower()
    with path.open(encoding="utf-8", newline="") as f:
        if suffix == ".json":
            return json.load(f)
        if suffix in (".yaml", ".yml"):
            return yaml.safe_load(f)
        if suffix == ".csv":
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported test data format: {filename}")

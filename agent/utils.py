import json
from datetime import datetime, date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_json(filename: str):
    """
    Load a JSON file from the data directory.
    """
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_date(iso_str: str) -> date:
    """
    Parse YYYY-MM-DD string into date object.
    """
    return datetime.strptime(iso_str, "%Y-%m-%d").date()

def days_between(d1: date, d2: date) -> int:
    """
    Number of days between two dates.
    """
    return (d2 - d1).days

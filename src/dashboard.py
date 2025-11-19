# dashboard.py

import json
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "remembrance_log.json"


def get_recent_events(limit: int = 20):
    """Return the most recent logged events for use in a dashboard."""
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r", encoding="utf-8") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return []

    # sort newest first
    events.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return events[:limit]

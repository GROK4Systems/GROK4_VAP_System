# remembrance_ledger.py

import json
from datetime import datetime
from pathlib import Path

# log file will live at: GROK4_VAP_System/remembrance_log.json
LOG_FILE = Path(__file__).resolve().parent.parent / "remembrance_log.json"


def _load_log():
    if LOG_FILE.exists():
        try:
            with LOG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def _save_log(entries):
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def log_event(status, input_text, output_text, model_id, details):
    """Append a new event to the remembrance log."""
    entries = _load_log()
    entries.append({
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "model_id": model_id,
        "input_text": input_text,
        "output_text": output_text,
        "details": details,
    })
    _save_log(entries)

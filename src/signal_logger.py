import os
import json
from datetime import datetime, UTC

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
signal_log_file = os.path.join(LOG_PATH, 'signal_log.json')

def save_signals(signal_summary):
    try:
        with open(signal_log_file, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    for symbol, signal in signal_summary.items():
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "symbol": symbol,
            "signal": signal["signal"],
            "confidence": signal["confidence"],
            "reason": signal["reason"],
            "action": "WAIT FOR CONFIRMATION"
        }
        logs.append(entry)

    with open(signal_log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"✅ {len(signal_summary)} signals saved to signal_log.json")
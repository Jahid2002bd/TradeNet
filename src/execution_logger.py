import os
import json
from datetime import datetime
from typing import Dict

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
EXEC_LOG_FILE = os.path.join(LOG_PATH, 'execution_log.json')

def log_execution(symbol: str, signal_data: Dict, mode: str = "auto") -> None:
    record = {
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "signal": str(signal_data.get("signal", "")),
        "confidence": int(signal_data.get("confidence", 0)),
        "reason": str(signal_data.get("reason", "")),
        "mode": mode,
        "outcome": "pending"  # Future hook: can be updated to "win"/"loss"
    }

    # Load previous logs
    if os.path.exists(EXEC_LOG_FILE):
        try:
            with open(EXEC_LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    else:
        logs = []

    logs.append(record)

    with open(EXEC_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"📝 Trade logged: {symbol} → {record['signal']} ({record['confidence']}%) | Mode: {mode}")
import os
import json
from typing import Dict, Any
from time import strftime

LOG_FILE: str = os.path.join(os.path.dirname(__file__), '..', 'logs', 'execution_log.json')

def track_outcome(symbol: str, result: str, trade: Dict[str, Any]) -> None:
    """
    Saves outcome of a trade into execution_log.json
    :param symbol: e.g. 'BTCUSDT'
    :param result: 'win' or 'loss' or 'neutral'
    :param trade: full trade dict with signal, confidence, reason
    """
    log_data: Dict[str, Any] = {}

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠️ Failed to read existing log file. Starting fresh.")

    timestamp: str = strftime("%Y-%m-%dT%H:%M:%S")

    log_data[timestamp] = {
        symbol: {
            "signal": trade.get("signal", "UNKNOWN"),
            "confidence": int(trade.get("confidence", 0)),
            "reason": trade.get("reason", ""),
            "mode": trade.get("mode", "DRY-RUN"),
            "outcome": result
        }
    }

    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=2)
        print(f"📍 Outcome tracked → {symbol} [{result}] @ {timestamp}")
    except Exception as e:
        print(f"❌ Failed to write outcome log: {e}")
import os
import json
from typing import Dict, Any, List

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
EXEC_LOG_FILE = os.path.join(LOG_PATH, 'execution_log.json')
WEIGHT_OUTPUT_FILE = os.path.join(LOG_PATH, 'signal_weights.json')

def calculate_success_weights() -> Dict[str, float]:
    """
    Reads execution log and calculates win ratio per symbol.
    Saves weight table for booster logic.
    """
    if not os.path.exists(EXEC_LOG_FILE):
        print("❌ Execution log not found.")
        return {}

    try:
        with open(EXEC_LOG_FILE, 'r') as f:
            trades: List[Dict[str, Any]] = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Failed to load execution log.")
        return {}

    tally: Dict[str, Dict[str, int]] = {}

    for trade in trades:
        symbol: str = str(trade.get("symbol", "")).upper()
        outcome: str = str(trade.get("outcome", "")).lower()

        if symbol not in tally:
            tally[symbol] = {"win": 0, "loss": 0}

        if outcome == "win":
            tally[symbol]["win"] += 1
        elif outcome == "loss":
            tally[symbol]["loss"] += 1

    weights: Dict[str, float] = {}
    for symbol, stats in tally.items():
        total = stats["win"] + stats["loss"]
        weights[symbol] = round(stats["win"] / total, 2) if total > 0 else 0.0

    with open(WEIGHT_OUTPUT_FILE, 'w') as f:
        json.dump(weights, f, indent=2)

    print(f"🧠 Strategy weights saved for {len(weights)} symbol(s).")
    return weights
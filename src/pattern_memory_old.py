import os
import json
from collections import Counter
from typing import List, Dict, Any

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
EXEC_LOG_FILE = os.path.join(LOG_PATH, 'execution_log.json')
PATTERN_OUTPUT_FILE = os.path.join(LOG_PATH, 'pattern_memory.json')

def load_trades() -> List[Dict[str, Any]]:
    if not os.path.exists(EXEC_LOG_FILE):
        return []

    try:
        with open(EXEC_LOG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def identify_patterns(trades: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Extracts frequent winning patterns based on signal, confidence band, reason keywords.
    Returns pattern frequency map.
    """
    patterns: Counter = Counter()

    for trade in trades:
        outcome = str(trade.get("outcome", "")).lower()
        if outcome != "win":
            continue

        symbol = str(trade.get("symbol", "")).upper()
        signal = str(trade.get("signal", "")).upper()
        conf_val = trade.get("confidence", 0)
        confidence = int(conf_val) if isinstance(conf_val, (int, float, str)) else 0
        reason_text = str(trade.get("reason", "")).lower()

        band = "80+" if confidence >= 80 else "60+" if confidence >= 60 else "low"
        reason_tag = reason_text.split(" ")[0] if reason_text else "generic"

        pattern_key = f"{symbol}_{signal}_{band}_{reason_tag}"
        patterns[pattern_key] += 1

    return dict(patterns)

def save_pattern_memory(patterns: Dict[str, int]) -> None:
    with open(PATTERN_OUTPUT_FILE, 'w') as f:
        json.dump(patterns, f, indent=2)
    print(f"🧠 Pattern memory saved with {len(patterns)} entries.")

def generate_pattern_memory() -> None:
    trades = load_trades()
    patterns = identify_patterns(trades)
    save_pattern_memory(patterns)
import os
import json
from typing import Dict, Any

# 📁 Pattern memory file location
PATTERN_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'pattern_memory.json')

def load_pattern_memory() -> Dict[str, int]:
    """
    Loads pattern memory from JSON file.
    Each key maps to a count ➤ how often pattern succeeded.
    """
    if not os.path.exists(PATTERN_FILE):
        return {}
    try:
        with open(PATTERN_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def boost_with_patterns(signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Pattern-based boosting engine ➤ adds bonus confidence
    if memory shows pattern has repeated success.

    Key format: BTCUSDT_BUY_80+_breakout
    """
    patterns = load_pattern_memory()
    boosted = {}

    for symbol, data in signals.items():
        base_conf = int(data.get("confidence", 0))
        signal = str(data.get("signal", "")).upper()
        reason_tag = str(data.get("reason", "")).split(" ")[0].lower()
        band = "80+" if base_conf >= 80 else "60+" if base_conf >= 60 else "low"
        pattern_key = f"{symbol}_{signal}_{band}_{reason_tag}"

        # 🎯 Boost logic
        bonus = 5 if patterns.get(pattern_key, 0) >= 3 else 0
        new_conf = min(base_conf + bonus, 100)

        boosted[symbol] = {
            **data,
            "confidence": new_conf,
            "reason": f"{data.get('reason', '')} | PatternBoost {bonus}%"
        }

    print(f"🧠 Pattern boost applied to {len(boosted)} signals.")
    return boosted

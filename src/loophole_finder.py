import os
import json
from collections import defaultdict
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
SIGNAL_LOG_FILE = os.path.join(LOG_PATH, 'signal_log.json')
PATTERN_LOG_FILE = os.path.join(LOG_PATH, 'loophole_patterns.json')

def detect_loopholes():
    try:
        with open(SIGNAL_LOG_FILE, 'r') as f:
            signals = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No signal data found.")
        return

    pattern_count = defaultdict(int)
    symbol_reason_combo = defaultdict(list)

    for entry in signals:
        key = f"{entry['symbol']} | {entry['reason']}"
        pattern_count[key] += 1
        symbol_reason_combo[entry['symbol']].append(entry['reason'])

    patterns = []
    for key, count in pattern_count.items():
        if count >= 3:  # Repeat threshold
            symbol, reason = key.split(' | ')
            patterns.append({
                "symbol": symbol,
                "reason": reason,
                "repeat_count": count,
                "timestamp": datetime.now().isoformat(),
                "insight": "🔁 Signal pattern repeated multiple times — potentially exploitable."
            })

    with open(PATTERN_LOG_FILE, 'w') as f:
        json.dump(patterns, f, indent=2)

    print(f"✅ {len(patterns)} repeatable patterns saved to loophole_patterns.json")
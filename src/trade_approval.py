import os
import json
from typing import List, Dict

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
QUEUE_FILE = os.path.join(LOG_PATH, 'approval_queue.json')
APPROVED_FILE = os.path.join(LOG_PATH, 'approved_signals.json')

def queue_signals(signals: Dict[str, Dict]) -> None:
    pending: List[Dict] = []
    for symbol, data in signals.items():
        pending.append({
            "symbol": symbol,
            "signal": data.get("signal", ""),
            "confidence": data.get("confidence", 0),
            "reason": data.get("reason", "")
        })

    with open(QUEUE_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

    print(f"📥 {len(pending)} signals queued for manual approval.")

def approve_symbol(symbol: str) -> None:
    try:
        with open(QUEUE_FILE, 'r') as f:
            queue: List[Dict] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No approval queue found.")
        return

    approved = [item for item in queue if item["symbol"].lower() == symbol.lower()]
    remaining = [item for item in queue if item["symbol"].lower() != symbol.lower()]

    with open(APPROVED_FILE, 'w') as f:
        json.dump(approved, f, indent=2)

    with open(QUEUE_FILE, 'w') as f:
        json.dump(remaining, f, indent=2)

    print(f"✅ {symbol.upper()} approved for execution.")

def reject_symbol(symbol: str) -> None:
    try:
        with open(QUEUE_FILE, 'r') as f:
            queue: List[Dict] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No approval queue found.")
        return

    remaining = [item for item in queue if item["symbol"].lower() != symbol.lower()]

    with open(QUEUE_FILE, 'w') as f:
        json.dump(remaining, f, indent=2)

    print(f"🚫 {symbol.upper()} rejected and removed from queue.")

def get_queue() -> List[Dict]:
    if not os.path.exists(QUEUE_FILE):
        return []

    try:
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_approved() -> List[Dict]:
    if not os.path.exists(APPROVED_FILE):
        return []

    try:
        with open(APPROVED_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
import os
import json
from typing import Dict, Any

MEMORY_FILE: str = os.path.join(os.path.dirname(__file__), '..', 'logs', 'pattern_memory.json')

def learn_pattern_from_execution(executed_trades: Dict[str, Dict[str, Any]]) -> None:
    """
    Updates pattern memory based on executed trades.
    Each pattern key is formed as: symbol + signal + confidence band + reason tag
    """
    memory: Dict[str, int] = {}

    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                memory = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠️ Failed to read pattern memory. Starting fresh.")

    for symbol, data in executed_trades.items():
        conf: int = int(data.get("confidence", 0))
        band: str = "80+" if conf >= 80 else "60+" if conf >= 60 else "low"
        tag: str = str(data.get("reason", "generic")).split(" ")[0].lower()
        signal: str = str(data.get("signal", "UNKNOWN")).upper()
        key: str = f"{symbol}_{signal}_{band}_{tag}"

        memory[key] = memory.get(key, 0) + 1

    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=2)
        print("🧠 Pattern memory updated.")
    except Exception as e:
        print(f"❌ Failed to write pattern memory: {e}")
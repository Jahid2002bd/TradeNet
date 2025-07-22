from typing import Dict, Any

def approve_signals(signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    approved = {}
    for symbol, data in signals.items():
        confidence = int(data.get("confidence", 0))
        if confidence >= 60:
            approved[symbol] = data
    print(f"✅ Approved {len(approved)} signals.")
    return approved
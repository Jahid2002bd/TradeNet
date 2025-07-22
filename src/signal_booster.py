from typing import Dict, Any

def boost_signals(signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Boosts signal confidence based on outcome logic.
    - If confidence ≥ 70 ➤ +7%
    - If confidence ≥ 60 ➤ +3%
    - Else ➤ no boost
    """
    boosted: Dict[str, Dict[str, Any]] = {}

    for symbol, data in signals.items():
        base_conf = int(data.get("confidence", 0))
        bonus = 7 if base_conf >= 70 else 3 if base_conf >= 60 else 0
        new_conf = min(base_conf + bonus, 100)

        boosted[symbol] = {
            **data,
            "confidence": new_conf,
            "reason": f"{data.get('reason', '')} | OutcomeBoost {bonus}%"
        }

    print(f"⚡ Outcome boost applied to {len(boosted)} signals.")
    return boosted
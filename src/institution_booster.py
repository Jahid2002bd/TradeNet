from typing import Dict, Any

def boost_institutional_behavior(signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Boosts signal confidence if it matches institutional behavior:
    - RSI oversold
    - MACD bullish crossover
    - Volume spike
    """
    boosted: Dict[str, Dict[str, Any]] = {}

    for symbol, data in signals.items():
        base_conf = int(data.get("confidence", 0))
        reason_text = str(data.get("reason", "")).lower()

        is_rsi_oversold = "rsi oversold" in reason_text
        is_macd_bullish = "macd bullish" in reason_text
        is_volume_spike = "volume spike" in reason_text

        match_count = sum([is_rsi_oversold, is_macd_bullish, is_volume_spike])
        bonus = 10 if match_count == 3 else 5 if match_count == 2 else 0
        new_conf = min(base_conf + bonus, 100)

        boosted[symbol] = {
            **data,
            "confidence": new_conf,
            "reason": f"{data.get('reason', '')} | InstBoost {bonus}%",
        }

    print(f"🏦 Institutional boost applied to {len(boosted)} signals.")
    return boosted
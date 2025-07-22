from typing import Dict, Any

def generate_trade_signal(indicators: Dict[str, Any], sentiment: str, auto_mode: bool = False) -> Dict[str, Any]:
    reasons = []
    confidence = 0
    decision = "AVOID"

    if indicators.get('rsi', 50) < 30:
        reasons.append("RSI oversold")
        confidence += 30

    if indicators.get('macd_signal') == 'bullish':
        reasons.append("MACD bullish crossover")
        confidence += 25

    if indicators.get('volume_spike', False):
        reasons.append("Volume spike detected")
        confidence += 15

    if sentiment == 'positive':
        reasons.append("Positive news sentiment")
        confidence += 25
    elif sentiment == 'negative':
        reasons.append("Negative sentiment detected")
        confidence -= 20

    confidence = max(0, min(confidence, 100))

    if confidence >= 90:
        decision = "BUY"
    elif confidence >= 70:
        decision = "HOLD"

    action = "✅ Auto-executed" if auto_mode and decision == "BUY" else "🤖 Awaiting approval"

    return {
        "signal": decision,
        "confidence": confidence,
        "reason": ', '.join(reasons),
        "action": action
    }

def generate_signals() -> Dict[str, Dict[str, Any]]:
    sample_data = {
        "BTCUSDT": {
            "indicators": {"rsi": 28, "macd_signal": "bullish", "volume_spike": True},
            "sentiment": "positive"
        },
        "ETHUSDT": {
            "indicators": {"rsi": 45, "macd_signal": "bearish", "volume_spike": False},
            "sentiment": "negative"
        }
    }

    output = {}
    for symbol, data in sample_data.items():
        signal = generate_trade_signal(data["indicators"], data["sentiment"])
        signal["symbol"] = symbol
        output[symbol] = signal

    print(f"🧠 Signals generated for {len(output)} symbols.")
    return output
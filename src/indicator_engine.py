import random

def analyze_indicators(snapshot):
    result = {}

    for symbol in snapshot.get("crypto", {}):
        try:
            # Dummy analysis for RSI, MACD, Volume
            rsi = random.randint(10, 90)
            macd_signal = random.choice(["bullish", "bearish", "neutral"])
            volume_spike = random.choice([True, False])

            signal = None
            reason = []

            if rsi < 30 and macd_signal == "bullish" and volume_spike:
                signal = "BUY"
                reason = ["RSI oversold", "MACD bullish crossover", "Volume spike"]
            elif rsi > 70 and macd_signal == "bearish":
                signal = "SELL"
                reason = ["RSI overbought", "MACD bearish crossover"]
            else:
                signal = "HOLD"
                reason = ["No clear setup"]

            result[symbol] = {
                "rsi": rsi,
                "macd": macd_signal,
                "volume_spike": volume_spike,
                "signal": signal,
                "confidence": random.randint(70, 95),
                "reason": " + ".join(reason)
            }

        except Exception as e:
            print(f"❌ Indicator analysis failed for {symbol}: {e}")
            result[symbol] = {}

    return result
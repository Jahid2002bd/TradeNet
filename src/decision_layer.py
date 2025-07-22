import random

def generate_trade_decisions(snapshot, signal_summary):
    decisions = {}

    for symbol, signal in signal_summary.items():
        try:
            price = snapshot['crypto'][symbol]['price']
            entry = round(price, 2)
            tp = round(entry * 1.03, 2)  # 3% gain target
            sl = round(entry * 0.97, 2)  # 3% risk buffer

            text_summary = f"{symbol} → {signal['signal']} | Entry: ${entry} | TP: ${tp} | SL: ${sl} | Reason: {signal['reason']} | Confidence: {signal['confidence']}%"

            decisions[symbol] = {
                "entry": entry,
                "tp": tp,
                "sl": sl,
                "summary": text_summary
            }
        except Exception as e:
            print(f"❌ Decision creation failed for {symbol}: {e}")
            decisions[symbol] = {}

    return decisions
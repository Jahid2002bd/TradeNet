from typing import Dict
from src.telegram_controller import get_config
from src.trade_approval import get_approved
from src.execution_logger import log_execution
from src.auto_trader import notify_commander

# ✅ ট্রিগার ফাংশন বসানো হয়েছে নিচে
def trigger_trade(signal: Dict) -> None:
    symbol = signal.get("symbol", "—")
    side = signal.get("signal", "—")
    entry = signal.get("entry_price", "—")
    tp = signal.get("tp", "—")
    sl = signal.get("sl", "—")

    print(f"\n🚀 Executing {side} trade for {symbol}")
    print(f"🎯 Entry: ${entry} | 📈 TP: ${tp} | 🛑 SL: ${sl}")
    print("✅ Trade Executed (Simulated)")  # 🔁 Future: API call here

def execute_signals(signal_summary: Dict[str, Dict]) -> None:
    config = get_config()
    mode = str(config.get("TRADE_MODE", "auto")).lower()
    threshold_raw = config.get("BIG_TRADE_CONFIDENCE", 85)
    threshold = int(threshold_raw) if isinstance(threshold_raw, (int, float, str)) else 85
    commander = config.get("COMMANDER_NAME", "Commander")

    if mode == "manual":
        approved_list = get_approved()
        approved_symbols = {str(item.get("symbol", "")).upper() for item in approved_list}
        print(f"\n🔒 Manual Mode ➤ Executing {len(approved_symbols)} approved trades:\n")

        for symbol in approved_symbols:
            signal = signal_summary.get(symbol)
            if not signal:
                print(f"⚠️ Skipped: {symbol} → Not found in current signal batch.")
                continue

            signal_type = str(signal.get("signal", "—")).upper()
            reason = str(signal.get("reason", "—"))
            confidence = int(signal.get("confidence", 0))

            print(f"✅ [MANUAL] Executing {symbol} → {signal_type} ({confidence}%) | Reason: {reason}")
            trigger_trade(signal)  # ✅ Trigger function called here
            notify_commander(signal, is_auto=False, commander=commander)
            log_execution(symbol, signal, mode=mode)
        return

    print(f"\n⚡ Auto Mode ➤ Executing signals above {threshold}% confidence:\n")
    for symbol, signal in signal_summary.items():
        confidence = int(signal.get("confidence", 0))
        if confidence >= threshold:
            signal_type = str(signal.get("signal", "—")).upper()
            reason = str(signal.get("reason", "—"))

            print(f"✅ [AUTO] Executing {symbol} → {signal_type} ({confidence}%) | Reason: {reason}")
            trigger_trade(signal)  # ✅ Trigger function called here
            notify_commander(signal, is_auto=True, commander=commander)
            log_execution(symbol, signal, mode=mode)
        else:
            print(f"⏩ Skipped: {symbol} → Confidence {confidence}% below threshold.")

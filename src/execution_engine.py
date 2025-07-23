from typing import Dict, List
from src.telegram_controller import get_config
from src.trade_approval import get_approved
from src.execution_logger import log_execution
from src.auto_trader import notify_commander

def trigger_trade(signal: Dict) -> None:
    symbol = signal.get("symbol", "—")
    side = signal.get("signal", "—").upper()
    entry = signal.get("entry_price", "—")
    tp = signal.get("tp", "—")
    sl = signal.get("sl", "—")

    print(f"\n🚀 Executing {side} trade for {symbol}")
    print(f"🎯 Entry: ${entry} | 📈 TP: ${tp} | 🛑 SL: ${sl}")
    print("✅ Trade Executed (Simulated)")

def execute_signals(signal_summary: Dict[str, Dict]) -> None:
    config = get_config()
    mode = str(config.get("TRADE_MODE", "auto")).lower()
    commander = str(config.get("COMMANDER_NAME", "Commander"))
    plan = str(config.get("USER_PLAN", "lite")).lower()

    # 🎯 Plan-based threshold
    plan_thresholds = {
        "free": None,
        "lite": 70,
        "pro": 85,
        "enterprise": 90
    }
    raw_threshold = config.get("BIG_TRADE_CONFIDENCE", 85)
    try:
        config_threshold = int(float(raw_threshold))
    except (ValueError, TypeError):
        config_threshold = 85

    threshold = plan_thresholds.get(plan, config_threshold)
    if threshold is None:
        print(f"\n⛔ Plan '{plan}' blocked trade execution. Upgrade required.")
        return

    if mode == "manual":
        approved: List[Dict] = get_approved()
        approved_symbols = {str(item.get("symbol", "")).upper() for item in approved}
        print(f"\n🔒 Manual Mode ➤ Executing {len(approved_symbols)} approved trades (Plan: {plan}, Threshold: {threshold}%):\n")

        for symbol in approved_symbols:
            signal = signal_summary.get(symbol)
            if not signal:
                print(f"⚠️ Skipped: {symbol} → Not found in current signal batch.")
                continue

            confidence = int(signal.get("confidence", 0))
            if confidence < threshold:
                print(f"⏩ Skipped {symbol} → {confidence}% below plan threshold {threshold}%")
                continue

            print(f"✅ [MANUAL] {symbol} → {signal.get('signal', '—')} ({confidence}%) | Reason: {signal.get('reason', '—')}")
            trigger_trade(signal)
            notify_commander(signal, is_auto=False, commander=commander)
            log_execution(symbol, signal, mode="manual")
        return

    print(f"\n⚡ AUTO Mode ➤ Executing signals above {threshold}% (Plan: {plan})\n")
    for symbol, signal in signal_summary.items():
        confidence = int(signal.get("confidence", 0))
        if confidence >= threshold:
            print(f"✅ [AUTO] {symbol} → {signal.get('signal', '—')} ({confidence}%) | Reason: {signal.get('reason', '—')}")
            trigger_trade(signal)
            notify_commander(signal, is_auto=True, commander=commander)
            log_execution(symbol, signal, mode="auto")
        else:
            print(f"⏩ Skipped: {symbol} → Confidence {confidence}% below threshold.")

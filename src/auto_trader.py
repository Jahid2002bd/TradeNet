from utils.execution_engine import send_order
from utils.pattern_booster import is_big_trade_booster_combo
from utils.telegram_notify import notify
from utils.outcome_logger import save_trade_log

TRADE_MODE = "auto"
BIG_TRADE_THRESHOLD = 90
COMMANDER_NAME = "Jahid"

def execute_signal(signal: dict):
    if signal.get("approved") and TRADE_MODE == "auto":
        is_big = (
            signal.get("confidence", 0) >= BIG_TRADE_THRESHOLD and
            is_big_trade_booster_combo(signal)
        )

        send_order(signal)

        message = f"{COMMANDER_NAME}, {'বড়' if is_big else 'normal'} ট্রেড complete ✅\n"
        message += f"📈 {signal['symbol']} {signal['signal']} @ {signal['confidence']}%\n"
        message += f"🎯 Tag: {signal.get('tag', '—')}\n"
        boosters = signal.get("booster", {})
        message += f"⚡ Boosters: {', '.join(boosters.keys()) if boosters else '—'}"

        notify(message)
        save_trade_log(signal, is_big)

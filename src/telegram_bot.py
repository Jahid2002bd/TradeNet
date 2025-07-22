import os
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ✅ Modular Commands from controller
from src.telegram_controller import (
    set_mode,
    set_threshold,
    toggle_boost,
    show_summary,
)

# 🗂️ File paths & configuration
LOG_PATH: str = os.path.join(os.path.dirname(__file__), '..', 'logs')
SIGNAL_LOG: str = os.path.join(LOG_PATH, 'signal_log.json')

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "7597308355:AAGevLTQSQnxP_6WDVNO6_Ks81lrCzYefcc")
CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "7295931540")
LANGUAGE: str = os.getenv("TELEGRAM_LANG", "bangla").lower()  # or "english"

# 🟢 /start ➤ Bot greet message
async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ TradeNet AI Telegram এর সাথে সফলভাবে যুক্ত!")

# 🟢 /latest ➤ Show most recent signal summary
async def latest(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open(SIGNAL_LOG, 'r') as f:
            logs = json.load(f)
            last = logs[-1]

        symbol: str = str(last.get("symbol", "❓"))
        signal: str = str(last.get("signal", "❓"))
        confidence: str = str(last.get("confidence", "N/A"))
        reason: str = str(last.get("reason", "N/A"))
        action: str = str(last.get("action", "N/A"))
        note: str = str(last.get("note", ""))

        if LANGUAGE == "bangla":
            msg: str = (
                f"📊 {symbol} → {signal}\n"
                f"কারণ: {reason}\n"
                f"নিশ্চয়তা: {confidence}%\n"
                f"অ্যাকশন: {action}"
            )
            if note:
                msg += f"\n📌 নোট: {note}"
        else:
            msg: str = (
                f"📊 {symbol} → {signal} ({confidence}%)\n"
                f"Reason: {reason}\n"
                f"Action: {action}"
            )
            if note:
                msg += f"\n📌 Note: {note}"

        await update.message.reply_text(msg)

    except (FileNotFoundError, json.JSONDecodeError, IndexError):
        await update.message.reply_text("❌ কোনো signal পাওয়া যায়নি।")

# 🟣 /unknown ➤ Invalid command fallback
async def echo(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 আমি বুঝিনি। কমান্ড ব্যবহার করুন:\n/start /latest /mode /threshold /boost /summary"
    )

# 🚀 Launch Telegram Bot
def run_telegram_bot() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ✅ Core command routes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("status", echo))
    app.add_handler(CommandHandler("help", echo))

    # ✅ Controller commands
    app.add_handler(CommandHandler("mode", set_mode))
    app.add_handler(CommandHandler("threshold", set_threshold))
    app.add_handler(CommandHandler("boost", toggle_boost))
    app.add_handler(CommandHandler("summary", show_summary))

    print("✅ Telegram Bot is running with Command Center...")
    app.run_polling(stop_signals=None)

# 🟢 Entry Point
if __name__ == "__main__":
    run_telegram_bot()
from telegram import Update
from telegram.ext import ContextTypes
from typing import Dict

# Runtime config state
BOT_CONFIG: Dict[str, object] = {
    "mode": "auto",
    "threshold": 85,
    "boost": True
}

# 🟢 /mode auto | /mode manual
async def set_mode(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if "manual" in text:
        BOT_CONFIG["mode"] = "manual"
        await update.message.reply_text("🛠️ Execution mode set to: Manual")
    elif "auto" in text:
        BOT_CONFIG["mode"] = "auto"
        await update.message.reply_text("⚡ Execution mode set to: Auto")
    else:
        await update.message.reply_text("❌ Invalid mode. Use /mode auto or /mode manual.")

# 🟢 /threshold 90
async def set_threshold(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split(" ")
    if len(parts) < 2 or not parts[1].isdigit():
        await update.message.reply_text("❌ Invalid format. Use like: /threshold 90")
        return

    value = int(parts[1])
    if 50 <= value <= 100:
        BOT_CONFIG["threshold"] = value
        await update.message.reply_text(f"📊 Confidence threshold set to: {value}%")
    else:
        await update.message.reply_text("⚠️ Please choose a threshold between 50 and 100.")

# 🟢 /boost on | /boost off
async def toggle_boost(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if "on" in text:
        BOT_CONFIG["boost"] = True
        await update.message.reply_text("✅ Booster enabled (confidence bonus ON).")
    elif "off" in text:
        BOT_CONFIG["boost"] = False
        await update.message.reply_text("🚫 Booster disabled (bonus OFF).")
    else:
        await update.message.reply_text("❌ Invalid option. Use /boost on or /boost off.")

# 🟢 /summary
async def show_summary(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    config = BOT_CONFIG
    msg = (
        f"📋 Current Config:\n"
        f"Mode: {config['mode']}\n"
        f"Threshold: {config['threshold']}%\n"
        f"Booster: {'Enabled' if config['boost'] else 'Disabled'}"
    )
    await update.message.reply_text(msg)

# 🟢 import json (used by other modules)
def get_config() -> dict:
    with open("config/config.json") as f:
        return json.load(f)




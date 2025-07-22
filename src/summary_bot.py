import os
import json
from typing import Dict, List, Any

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
EXEC_LOG_FILE = os.path.join(LOG_PATH, 'execution_log.json')

def load_executed_trades() -> List[Dict[str, Any]]:
    if not os.path.exists(EXEC_LOG_FILE):
        return []

    try:
        with open(EXEC_LOG_FILE, 'r') as f:
            trades = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        trades = []

    return trades

def generate_summary(limit: int = 10) -> str:
    trades = load_executed_trades()[-limit:]
    lines: List[str] = []

    for trade in trades:
        symbol = str(trade.get("symbol", "")).upper()
        signal = str(trade.get("signal", "")).upper()
        confidence = int(trade.get("confidence", 0)) if isinstance(trade.get("confidence", 0), (int, float, str)) else 0
        reason = str(trade.get("reason", ""))
        outcome = str(trade.get("outcome", "")).lower()
        mode = str(trade.get("mode", ""))
        timestamp = str(trade.get("timestamp", ""))

        line = f"📈 {symbol} → {signal} ({confidence}%) | Mode: {mode} | Outcome: {outcome} | 🕒 {timestamp}"
        if reason:
            line += f"\n🔍 Reason: {reason}"
        lines.append(line)

    return "\n\n".join(lines) if lines else "⚠️ No executed trades found."

def get_symbol_report(symbol: str) -> str:
    trades = load_executed_trades()
    symbol = symbol.upper()
    filtered = [t for t in trades if str(t.get("symbol", "")).upper() == symbol]
    wins = sum(1 for t in filtered if str(t.get("outcome", "")).lower() == "win")
    losses = sum(1 for t in filtered if str(t.get("outcome", "")).lower() == "loss")
    pending = sum(1 for t in filtered if str(t.get("outcome", "")).lower() == "pending")
    total = len(filtered)

    return (
        f"📊 Summary for {symbol}:\n"
        f"✅ Wins: {wins}\n❌ Losses: {losses}\n⏳ Pending: {pending}\n📦 Total Trades: {total}"
        if total else f"⚠️ No trades found for {symbol}."
    )
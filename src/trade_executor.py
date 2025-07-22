import time
from typing import Dict, Any

def send_order(trade: Dict[str, Any], dry_run: bool = True) -> None:
    """
    Simulates or triggers real trade execution.
    Dry-run mode prints only. Real mode should connect to broker API.
    """

    symbol_raw = trade.get("symbol", "")
    signal_raw = trade.get("signal", "")
    confidence_raw = trade.get("confidence", 0)
    reason_raw = trade.get("reason", "")
    source_raw = trade.get("source", "booster+approval")
    timestamp_raw = trade.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%S"))

    symbol: str = str(symbol_raw).upper()
    signal: str = str(signal_raw).upper()
    confidence: int = int(confidence_raw) if isinstance(confidence_raw, (int, float, str)) else 0
    reason: str = str(reason_raw)
    source: str = str(source_raw)
    timestamp: str = str(timestamp_raw)

    print(f"\n🚀 Executing Trade Trigger:")
    print(f"➡️ Symbol: {symbol}")
    print(f"📊 Signal: {signal} ({confidence}%)")
    print(f"🧠 Reason: {reason}")
    print(f"🔗 Source: {source}")
    print(f"🕒 Timestamp: {timestamp}")
    print(f"🧪 Mode: {'DRY-RUN' if dry_run else 'LIVE'}")

    if dry_run:
        print(f"✅ [SIMULATED] Trade for {symbol} has been staged.\n")
    else:
        # TODO: Implement actual broker API call here
        # e.g., binance_client.place_order(symbol=symbol, side=signal, amount=amount)
        print(f"🔥 [LIVE] Trade triggered → {symbol} [{signal}]\n")
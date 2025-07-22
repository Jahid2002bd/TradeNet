import os
import json
from datetime import datetime, UTC

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_PATH, exist_ok=True)

def save_signal_log(signal_data, symbol='BTCUSDT'):
    """
    Save signal to logs/signal_log.json
    """
    log_file = os.path.join(LOG_PATH, 'signal_log.json')
    data = {
        'timestamp': datetime.now(UTC).isoformat(),  # ✅ updated for timezone-aware UTC
        'symbol': symbol,
        'signal': signal_data.get('signal'),
        'confidence': signal_data.get('confidence'),
        'reason': signal_data.get('reason'),
        'action': signal_data.get('action')
    }

    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(data)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def save_trade_log(trade_data, symbol='BTCUSDT'):
    """
    Save executed trade log to logs/trade_log.json
    """
    log_file = os.path.join(LOG_PATH, 'trade_log.json')
    data = {
        'timestamp': datetime.now(UTC).isoformat(),  # ✅ updated for timezone-aware UTC
        'symbol': symbol,
        'side': trade_data.get('side'),
        'entry': trade_data.get('entry_price'),
        'tp': trade_data.get('tp'),
        'sl': trade_data.get('sl'),
        'mode': 'auto' if trade_data.get('auto_mode') else 'manual'
    }

    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(data)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
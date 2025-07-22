import os
import json
from datetime import datetime, UTC
from utils.fetcher.stock import fetch_stock_data
from utils.fetcher.forex import fetch_forex_data
from utils.fetcher.crypto import fetch_crypto_data
from utils.fetcher.commodity import fetch_commodity_data

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_PATH, exist_ok=True)

def fuse_market_data():
    timestamp = datetime.now(UTC).isoformat()

    fused = {
        'timestamp': timestamp,
        'stock': fetch_stock_data(['AAPL', 'TSLA']),
        'forex': fetch_forex_data(['EURUSD', 'GBPUSD']),
        'crypto': fetch_crypto_data(['BTCUSDT', 'ETHUSDT']),
        'commodities': fetch_commodity_data(['GOLD', 'OIL'])
    }

    # ✅ Save log
    log_file = os.path.join(LOG_PATH, 'fusion_log.json')
    try:
        do_something()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("❌ Error:", e)

    logs.append(fused)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    return fused
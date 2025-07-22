# src/utils/market_api_connector.py

"""
market_api_connector.py

Provides REST connectors to fetch market data (OHLC and latest price)
from Binance and Coinbase Pro public APIs.
"""

import requests
from datetime import datetime, timezone
from typing import List, Dict


def get_binance_klines(
    symbol: str,
    interval: str = "1m",
    limit: int = 100
) -> List[Dict]:
    """
    Fetch OHLC candlesticks from Binance REST API.

    Returns list of dicts with:
      {
        "open_time": datetime (UTC, timezone-aware),
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
      }
    """
    endpoint = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

    try:
        resp = requests.get(endpoint, params=params, timeout=5)
        resp.raise_for_status()
        raw_klines = resp.json()
    except requests.RequestException:
        return []
    except ValueError:
        return []

    ohlc_list: List[Dict] = []
    for entry in raw_klines:
        # Binance returns [openTime, open, high, low, close, volume, ...]
        try:
            open_time_ms = int(entry[0])
            ohlc_item = {
                # Use timezone-aware UTC datetime
                "open_time": datetime.fromtimestamp(open_time_ms / 1000, timezone.utc),
                "open": float(entry[1]),
                "high": float(entry[2]),
                "low": float(entry[3]),
                "close": float(entry[4]),
                "volume": float(entry[5])
            }
        except (IndexError, ValueError):
            continue
        ohlc_list.append(ohlc_item)

    return ohlc_list


def get_binance_price(symbol: str) -> float:
    """
    Fetch the latest price for a symbol from Binance.

    Returns 0.0 on failure.
    """
    endpoint = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol.upper()}

    try:
        resp = requests.get(endpoint, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return float(data.get("price", 0.0))
    except requests.RequestException:
        return 0.0
    except (ValueError, TypeError):
        return 0.0


def get_coinbase_ohlc(
    symbol: str,
    granularity: int = 60
) -> List[Dict]:
    """
    Fetch OHLC candles from Coinbase Pro REST API.

    granularity in seconds (60, 300, 900, 3600, 21600, 86400).
    """
    endpoint = f"https://api.pro.coinbase.com/products/{symbol.upper()}/candles"
    params = {"granularity": granularity}

    try:
        resp = requests.get(endpoint, params=params, timeout=5)
        resp.raise_for_status()
        raw_data = resp.json()
    except requests.RequestException:
        return []
    except ValueError:
        return []

    ohlc_list: List[Dict] = []
    for candle in raw_data:
        # Coinbase returns [time, low, high, open, close, volume]
        try:
            timestamp = int(candle[0])
            ohlc_entry = {
                # Use timezone-aware UTC datetime
                "open_time": datetime.fromtimestamp(timestamp, timezone.utc),
                "open": float(candle[3]),
                "high": float(candle[2]),
                "low": float(candle[1]),
                "close": float(candle[4]),
                "volume": float(candle[5])
            }
        except (IndexError, ValueError):
            continue
        ohlc_list.append(ohlc_entry)

    # Sort ascending by time
    return sorted(ohlc_list, key=lambda item: item["open_time"])


def get_coinbase_price(symbol: str) -> float:
    """
    Fetch the current spot price for a symbol from Coinbase Pro.

    Returns 0.0 on failure.
    """
    endpoint = f"https://api.pro.coinbase.com/products/{symbol.upper()}/ticker"
    try:
        resp = requests.get(endpoint, timeout=5)
        resp.raise_for_status()
        result = resp.json()
        return float(result.get("price", 0.0))
    except requests.RequestException:
        return 0.0
    except (ValueError, TypeError):
        return 0.0


class MarketAPIConnector:
    """
    Unified interface for market data across supported exchanges.
    """

    def __init__(self, exchange: str) -> None:
        exch = exchange.lower()
        if exch not in ("binance", "coinbase"):
            raise ValueError(f"Unsupported exchange '{exchange}'")
        self.exchange = exch

    def get_klines(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch OHLC candles for the configured exchange.
        """
        if self.exchange == "binance":
            return get_binance_klines(symbol, interval, limit)
        # Convert "5m" → 5*60 seconds
        gran = int(interval.rstrip("m")) * 60
        return get_coinbase_ohlc(symbol, gran)

    def get_current_price(self, symbol: str) -> float:
        """
        Fetch the latest price for the configured exchange.
        """
        if self.exchange == "binance":
            return get_binance_price(symbol)
        return get_coinbase_price(symbol)


if __name__ == "__main__":
    # Demo usage
    binance_connector = MarketAPIConnector("binance")
    cb_connector = MarketAPIConnector("coinbase")

    sample_symbol = "BTCUSDT"
    klines_b = binance_connector.get_klines(sample_symbol, interval="1m", limit=5)
    price_b = binance_connector.get_current_price(sample_symbol)

    sample_pair = "BTC-USD"
    klines_c = cb_connector.get_klines(sample_pair, interval="5m", limit=5)
    price_c = cb_connector.get_current_price(sample_pair)

    print("Binance 1m klines:", klines_b)
    print(f"Binance price for {sample_symbol}: {price_b}")

    print("Coinbase 5m candles:", klines_c)
    print(f"Coinbase price for {sample_pair}: {price_c}")

"""
timezone_filter.py

Utility to check if a market is open based on current UTC time and instrument symbol.
"""

from datetime import datetime, time
import pytz


# Optional: map known trading symbols to timezone
SYMBOL_TIMEZONE_MAP = {
    "BTCUSDT": "Asia/Dhaka",         # For crypto traders in Bangladesh
    "ETHUSDT": "Asia/Dhaka",
    "EURUSD": "Europe/London",       # Forex
    "XAUUSD": "America/New_York",    # Commodities
    "AAPL": "America/New_York",      # Stocks
    "TSLA": "America/New_York",
    "NIKKEI": "Asia/Tokyo",
}


def get_timezone_from_symbol(symbol: str) -> str:
    """
    Returns the market timezone for a given symbol.
    Defaults to 'Asia/Dhaka' if unknown.
    """
    return SYMBOL_TIMEZONE_MAP.get(symbol.upper(), "Asia/Dhaka")


def is_market_open(current_utc: datetime, symbol: str) -> bool:
    ...
    """
    Checks if market is open now based on symbol's timezone.
    Assumes standard open hours: 09:00–17:00 local time.

    Parameters:
        current_utc (datetime): Optional UTC time (default: now)
        symbol (str): Ticker symbol

    Returns:
        bool: True if market is open, else False
    """
    tz_name = get_timezone_from_symbol(symbol)
    tz = pytz.timezone(tz_name)

    utc_now = current_utc or datetime.utcnow()
    local_time = utc_now.astimezone(tz)
    local_hour = local_time.time()

    return time(9, 0) <= local_hour < time(17, 0)

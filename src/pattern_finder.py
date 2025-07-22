import pandas as pd
import numpy as np

def find_time_pattern(df, symbol='AAPL'):
    """
    Detects repeatable time-based patterns (e.g. Monday 10:30AM spikes)
    :param df: DataFrame with datetime index and OHLCV
    :param symbol: str - ticker name
    :return: dict - pattern summary
    """

    df = df.copy()
    df['day'] = df.index.day_name()
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['weekday_time'] = df['day'] + ' ' + df['hour'].astype(str) + ':' + df['minute'].astype(str).str.zfill(2)

    # Calculate % change
    df['pct_change'] = df['Close'].pct_change() * 100

    # Group by weekday_time
    pattern = df.groupby('weekday_time')['pct_change'].mean().sort_values(ascending=False)

    # Top 3 patterns
    top_patterns = pattern.head(3).to_dict()

    return {
        'symbol': symbol,
        'top_patterns': top_patterns,
        'message': f"📊 {symbol} shows repeatable spikes at: {list(top_patterns.keys())}"
    }
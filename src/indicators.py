import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice

# --- RSI ---
def get_rsi(data, period=14):
    close = data['Close'].squeeze()
    rsi = RSIIndicator(close=close, window=period).rsi()
    return pd.DataFrame({'RSI': rsi})

# --- MACD ---
def get_macd(data):
    close = data['Close'].squeeze()
    macd = MACD(close=close)
    return pd.DataFrame({
        'MACD': macd.macd(),
        'MACD_Signal': macd.macd_signal()
    })

# --- Bollinger Bands ---
def get_bollinger_bands(data, period=20):
    close = data['Close'].squeeze()
    bb = BollingerBands(close=close, window=period)
    return pd.DataFrame({
        'BB_Upper': bb.bollinger_hband(),
        'BB_Lower': bb.bollinger_lband()
    })

# --- Moving Averages ---
def get_moving_averages(data, sma_period=20, ema_period=20):
    close = data['Close'].squeeze()
    sma = SMAIndicator(close=close, window=sma_period).sma_indicator()
    ema = EMAIndicator(close=close, window=ema_period).ema_indicator()
    return pd.DataFrame({
        'SMA': sma,
        'EMA': ema
    })

# --- VWAP ---
def get_vwap(data):
    df = data.copy()
    vwap = VolumeWeightedAveragePrice(
        high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume']
    ).volume_weighted_average_price()
    return pd.DataFrame({'VWAP': vwap})

# --- Fibonacci Placeholder ---
def get_fibonacci_levels(data):
    high = data['High'].max()
    low = data['Low'].min()
    diff = high - low
    levels = {
        'Fib_0%': low,
        'Fib_23.6%': low + diff * 0.236,
        'Fib_38.2%': low + diff * 0.382,
        'Fib_50%': low + diff * 0.5,
        'Fib_61.8%': low + diff * 0.618,
        'Fib_100%': high
    }
    return pd.DataFrame([levels])

# --- Multi-Timeframe Placeholder ---
def multi_timeframe_analysis(data_dict):
    # data_dict = {'1h': df1, '4h': df4, '1d': df_daily}
    result = {}
    for tf, df in data_dict.items():
        rsi = get_rsi(df)['RSI'].iloc[-1]
        result[tf] = {'RSI': rsi}
    return result
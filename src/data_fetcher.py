import yfinance as yf
import requests
import pandas as pd

# --- STOCK DATA ---
def get_stock_data(ticker='AAPL', interval='15m', period='5d'):
    print(f"📈 Fetching Stock Data for {ticker}")
    data = yf.download(ticker, period=period, interval=interval)
    return data

# --- COMMODITY DATA (Gold, Oil etc. via YFinance) ---
def get_commodity_data(ticker='GC=F', interval='1h', period='5d'):
    print(f"🛢️ Fetching Commodity Data for {ticker}")
    data = yf.download(ticker, period=period, interval=interval)
    return data

# --- FOREX DATA (TwelveData API) ---
def get_forex_data(symbol='EUR/USD', interval='15min', apikey='YOUR_API_KEY'):
    print(f"💱 Fetching Forex Data for {symbol}")
    base, quote = symbol.split('/')
    url = f"https://api.twelvedata.com/time_series?symbol={base}/{quote}&interval={interval}&apikey={apikey}"
    response = requests.get(url)
    json_data = response.json()
    df = pd.DataFrame(json_data['values'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df.set_index('datetime')

# --- CRYPTO DATA (Binance API) ---
def get_crypto_data(symbol='BTCUSDT', interval='15m', limit=100):
    print(f"🪙 Fetching Crypto Data for {symbol}")
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    raw = response.json()
    columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame([x[:6] for x in raw], columns=columns)
    df['OpenTime'] = pd.to_datetime(df['OpenTime'], unit='ms')
    df.set_index('OpenTime', inplace=True)
    df = df.astype(float)
    return df
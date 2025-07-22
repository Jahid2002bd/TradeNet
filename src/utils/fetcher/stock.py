import yfinance as yf

def fetch_stock_data(tickers):
    result = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).info
            result[ticker] = {
                'price': round(data.get('currentPrice', 0), 2),
                'change': round(data.get('regularMarketChangePercent', 0), 2)
            }
        except (KeyError, ValueError, Exception) as e:
            print(f"❌ Stock fetch error for {ticker}: {e}")
            result[ticker] = {'price': None, 'change': None}
    return result
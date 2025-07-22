import yfinance as yf

def fetch_commodity_data(assets):
    mapping = {'GOLD': 'GC=F', 'OIL': 'CL=F'}
    result = {}
    for asset in assets:
        ticker = mapping.get(asset)
        try:
            data = yf.Ticker(ticker).info
            result[asset] = {'price': round(data.get('currentPrice', 0), 2)}
        except (KeyError, ValueError, Exception) as e:
            print(f"❌ Commodity fetch error for {asset}: {e}")
            result[asset] = {'price': None}
    return result
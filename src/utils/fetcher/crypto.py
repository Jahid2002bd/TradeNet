import requests

def fetch_crypto_data(pairs):
    result = {}
    for pair in pairs:
        try:
            url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            result[pair] = {'price': float(data['price'])}
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print(f"❌ Crypto fetch error for {pair}: {e}")
            result[pair] = {'price': None}
    return result
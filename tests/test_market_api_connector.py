import pytest
from src.utils.market_api_connector import MarketAPIConnector

def test_price_fetching(dummy_market):
    m1 = MarketAPIConnector("binance")
    assert m1.get_current_price("BTCUSDT") == 1234.5
    m2 = MarketAPIConnector("coinbase")
    assert m2.get_current_price("BTC-USD") == 1234.5

def test_invalid_exchange_raises():
    with pytest.raises(ValueError):
        MarketAPIConnector("unknown")

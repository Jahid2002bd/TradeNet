from src.utils.timezone_filter import is_market_open

def test_is_market_open_return_type():
    # Just check the return type is boolean
    result = is_market_open()
    assert isinstance(result, bool)

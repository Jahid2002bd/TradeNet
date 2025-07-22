import time
from src.utils.data_cache import DataCache

def test_cache_ttl_and_length():
    cache = DataCache(ttl_seconds=1)
    cache.set("key", "value")
    assert cache.get("key") == "value"
    time.sleep(1.1)
    assert cache.get("key") is None
    assert len(cache) == 0

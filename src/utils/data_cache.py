# src/utils/data_cache.py

"""
data_cache.py

Simple in-memory cache with per-key time-to-live (TTL).
"""

import threading
from datetime import datetime, timedelta, timezone
from typing import Any, Optional


class DataCache:
    """
    Stores values with timestamps and evicts them after TTL expires.
    """

    def __init__(self, ttl_seconds: int = 60):
        """
        Parameters:
            ttl_seconds (int): Time-to-live for cache entries, in seconds.
        """
        self.ttl = timedelta(seconds=ttl_seconds)
        self._store: dict[str, Any] = {}
        self._timestamps: dict[str, datetime] = {}
        self._lock = threading.Lock()

    def set(self, key: str, value: Any) -> None:
        """
        Store value under key with current UTC timestamp.
        """
        now = datetime.now(timezone.utc)
        with self._lock:
            self._store[key] = value
            self._timestamps[key] = now

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value if present and not expired; otherwise returns None.
        """
        now = datetime.now(timezone.utc)
        with self._lock:
            ts = self._timestamps.get(key)
            if ts is None:
                return None
            if now - ts > self.ttl:
                # Expired
                del self._store[key]
                del self._timestamps[key]
                return None
            return self._store.get(key)

    def cleanup(self) -> None:
        """
        Remove all expired entries from the cache.
        """
        now = datetime.now(timezone.utc)
        with self._lock:
            keys = list(self._timestamps.keys())
            for key in keys:
                if now - self._timestamps[key] > self.ttl:
                    del self._store[key]
                    del self._timestamps[key]

    def __len__(self) -> int:
        """
        Number of unexpired entries.
        """
        self.cleanup()
        with self._lock:
            return len(self._store)


if __name__ == "__main__":
    # Demo usage
    cache = DataCache(ttl_seconds=2)
    cache.set("foo", 123)
    print("foo:", cache.get("foo"))
    import time
    time.sleep(3)
    print("foo after expiry:", cache.get("foo"))
    cache.set("bar", "baz")
    print("Cache size:", len(cache))

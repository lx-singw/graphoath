import time
from typing import Dict, Any, Optional

class EvidenceCacheEngine:
    """
    In-Memory Evidence Graph LRU TTL Cache.
    
    Caches resolved evidence graph URN sets for 300 seconds to eliminate redundant
    DataHub GMS GraphQL calls during high-frequency agent evaluation loops.
    """
    def __init__(self, ttl_seconds: int = 300, maxsize: int = 10000):
        self.ttl = ttl_seconds
        self.maxsize = maxsize
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        entry = self._cache[key]
        if time.time() - entry["created_at"] > self.ttl:
            del self._cache[key]
            return None
        return entry["value"]

    def set(self, key: str, value: Any) -> None:
        if len(self._cache) >= self.maxsize:
            # Remove oldest entry
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]["created_at"])
            del self._cache[oldest_key]
        self._cache[key] = {
            "value": value,
            "created_at": time.time()
        }

    def clear(self) -> None:
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

_global_evidence_cache = EvidenceCacheEngine()

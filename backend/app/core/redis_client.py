import json
import logging
import time
from typing import Any, Optional
import redis

from ..database import settings

logger = logging.getLogger("redis_cache")

# Local in-memory fallback cache when Redis server is offline
_in_memory_cache: dict[str, tuple[Any, float]] = {}


class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self._client: Optional[redis.Redis] = None
        self._is_available = False
        self._connect()

    def _connect(self):
        try:
            self._client = redis.from_url(
                self.url,
                decode_responses=True,
                socket_connect_timeout=1.5,
                socket_timeout=1.5,
            )
            self._client.ping()
            self._is_available = True
            logger.info("Connected to Redis at %s", self.url)
        except Exception as exc:
            self._is_available = False
            logger.warning("Redis is not available (%s). Using in-memory fallback cache.", exc)

    @property
    def is_available(self) -> bool:
        if not self._is_available:
            # Periodic retry check
            try:
                if self._client and self._client.ping():
                    self._is_available = True
            except Exception:
                self._is_available = False
        return self._is_available

    def get(self, key: str) -> Optional[Any]:
        if self.is_available and self._client:
            try:
                raw = self._client.get(key)
                if raw is not None:
                    return json.loads(raw)
            except Exception as e:
                logger.error("Redis get error for %s: %s", key, e)

        # In-memory fallback
        if key in _in_memory_cache:
            val, expiry = _in_memory_cache[key]
            if expiry > time.time():
                return val
            del _in_memory_cache[key]
        return None

    def set(self, key: str, value: Any, expire_seconds: int = 300) -> bool:
        serialized = json.dumps(value)
        if self.is_available and self._client:
            try:
                self._client.setex(key, expire_seconds, serialized)
                return True
            except Exception as e:
                logger.error("Redis set error for %s: %s", key, e)

        # In-memory fallback
        _in_memory_cache[key] = (value, time.time() + expire_seconds)
        return True

    def delete(self, key: str) -> bool:
        if self.is_available and self._client:
            try:
                self._client.delete(key)
            except Exception:
                pass
        _in_memory_cache.pop(key, None)
        return True

    def delete_pattern(self, pattern: str) -> int:
        count = 0
        if self.is_available and self._client:
            try:
                keys = self._client.keys(pattern)
                if keys:
                    count = self._client.delete(*keys)
            except Exception:
                pass

        # In-memory pattern clear
        prefix = pattern.replace("*", "")
        keys_to_del = [k for k in _in_memory_cache if prefix in k]
        for k in keys_to_del:
            del _in_memory_cache[k]
            count += 1
        return count


redis_client = RedisClient(settings.redis_url)

import time
from typing import Any

_cache: dict[int, tuple[float, Any]] = {}

TTL_SECONDS = 300  # 5 minutes


def get_from_cache(key: int):
    if key not in _cache:
        return None

    expires_at, value = _cache[key]

    if time.time() > expires_at:
        del _cache[key]
        return None

    return value


def set_cache(key: int, value: Any):
    _cache[key] = (time.time() + TTL_SECONDS, value)


def clear_cache():
    _cache.clear()

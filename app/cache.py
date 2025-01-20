import redis

from app.schemas.url import URLResponseOut

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def get_cached_url(short_url: str) -> str | None:
    """Retrieve the long URL associated with the short URL from the cache."""
    return redis_client.get(short_url)


def cache_url(short_url: str, long_url: str):
    """Cache the mapping of short URL to long URL."""
    if isinstance(short_url, bytes):
        short_url = short_url.decode()
    if isinstance(long_url, bytes):
        long_url = long_url.decode()

    redis_client.setex(short_url, 3600, long_url)  # Cache for 1 hour

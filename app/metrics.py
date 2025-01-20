from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['endpoint'])
CACHE_HITS = Counter('cache_hits', 'Number of cache hits')
CACHE_MISSES = Counter('cache_misses', 'Number of cache misses')
RESPONSE_TIME = Histogram('response_time_seconds', 'Response time in seconds', ['endpoint'])
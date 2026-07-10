import json
from extensions import redis_client


def cache_get(key):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def cache_set(key, value, ttl=60):
    redis_client.setex(key, ttl, json.dumps(value))


def cache_delete(key):
    redis_client.delete(key)


def cache_delete_pattern(pattern):
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
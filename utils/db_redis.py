# utils/db_redis.py
# import redis, json
# r = redis.Redis(host="localhost", port=6379)
# def cache_departure(key, value):
#     r.set(key, json.dumps(value), ex=60)
# def get_cached_departure(key):
#     val = r.get(key)
#     return json.loads(val) if val else None
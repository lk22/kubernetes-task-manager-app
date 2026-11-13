import os
import json
import redis

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

redis_client = redis.from_url(REDIS_URL)

def get_cached_tasks():
  try:
      cached = redis_client.get("tasks:all")

      if cached:
        return json.loads(cached)
  except redis.RedisError:
      pass

  return None

def set_cached_tasks(tasks):
  try:
      redis_client.setex("tasks:all", 60, json.dumps(tasks))
  except redis.RedisError:
      pass

def invalidate_tasks_cache():
  try:
      redis_client.delete("tasks:all")
  except redis.RedisError:
      pass
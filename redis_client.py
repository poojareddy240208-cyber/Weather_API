import os
from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")

r = Redis.from_url(
    REDIS_URL,
    decode_responses=True
)
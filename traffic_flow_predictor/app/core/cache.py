import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings


async def get_redis_client() -> Redis:
    return redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

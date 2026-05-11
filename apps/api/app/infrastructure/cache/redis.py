import json
from redis.asyncio import Redis
from app.core.config import get_settings
class RedisCache:
    def __init__(self) -> None: self.client = Redis.from_url(get_settings().redis_url, decode_responses=True)
    async def get_json(self, key: str) -> dict | None:
        value = await self.client.get(key)
        return json.loads(value) if value else None
    async def set_json(self, key: str, value: dict, ttl: int = 300) -> None:
        await self.client.setex(key, ttl, json.dumps(value))

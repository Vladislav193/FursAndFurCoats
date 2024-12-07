import aioredis


class RedisMiddleware:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None

    async def on_start(self):
        self.redis = await aioredis.from_url(
            self.redis_url,
            decode_responses=True
        )


    async def on_stop(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()


    async def get_redis(self):
        return self.redis


    async def set_cache(self, key, value, expire: int = 3600):
        await self.redis.set(key, value, expire=expire)

from typing import Optional, Tuple
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger

from src.api.config import redis_config

from redis.asyncio import Redis as AsyncRedis

redis_client = AsyncRedis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    db=redis_config.db.cache
)


class QRRedisBackend(RedisBackend):

    # async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
    #     async with self.redis.pipeline(transaction=not self.is_cluster) as pipe:
    #         result = await pipe.ttl(key).get(key).execute()
    #         logger.info(f"Redis GET key: {key}, result: {result}")
    #         return result[0], result[1]

    async def get(self, key: str) -> Optional[bytes]:
        result = await self.redis.get(key)
        logger.info(f"Redis GET key: {key}, result: {result}")
        return result

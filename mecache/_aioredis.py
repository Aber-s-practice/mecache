import time
import pickle

import aioredis
from .core import AioBaseCache


class AioRedis(AioBaseCache):

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self, address, **kwargs):
        self.redis = await aioredis.create_redis_pool(address, **kwargs)

    async def get_cache(self, func, key, max_time):
        qual = func.__qualname__
        r = await self.redis.get(qual+":"+key)
        if r is None:
            return None
        return pickle.loads(r)

    async def set_cache(self, result, func, key, max_time):
        qual = func.__qualname__
        await self.redis.set(qual+":"+key, pickle.dumps(result), ex=time.time()+max_time)

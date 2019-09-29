import time
import pickle

from redis import Redis as RedisConnection
from .core import BaseCache


class Redis(BaseCache, RedisConnection):

    def get_cache(self, func, key, max_time):
        qual = func.__qualname__
        r = self.get(qual+":"+key)
        if r is None:
            return None
        return pickle.loads(r)

    def set_cache(self, result, func, key, max_time):
        qual = func.__qualname__
        self.set(qual+":"+key, pickle.dumps(result), ex=time.time()+max_time)

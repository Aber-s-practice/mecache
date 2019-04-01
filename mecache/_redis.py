import time
import pickle

from redis import Redis as RedisConnection
from .core import BaseCache


class Redis(BaseCache, RedisConnection):

    def get_cache(self, func, key, max_time):
        qual = func.__qualname__
        return self.get(qual+":"+key)

    def set_cache(self, result, func, key, max_time):
        qual = func.__qualname__
        self.set(qual+":"+key, result, ex=time.time()+max_time)

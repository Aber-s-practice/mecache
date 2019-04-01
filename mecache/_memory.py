import time

from .core import BaseCache


class Memory(BaseCache):

    def __init__(self):
        self.__pool = {}

    def get_cache(self, func, key, max_time):
        qual = func.__qualname__

        if self.__pool.get(qual) is not None:
            cache = self.__pool[qual].get(key)
            if cache['expired'] > time.time():
                return cache['value']
        return None

    def set_cache(self, result, func, key, max_time):
        qual = func.__qualname__

        if self.__pool.get(qual) is None:
            self.__pool[qual] = {}
        self.__pool[qual][key] = {"value": result, 'expired': time.time()+max_time}

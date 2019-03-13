import os
import pickle
import atexit
import time
from functools import wraps


class Memory:
    def __init__(self, path):
        self.__path = path
        _path = os.path.dirname(path)
        if not os.path.exists(_path):
            os.makedirs(_path)
        self.load()

    @property
    def path(self):
        return self.__path

    def dump(self):
        with open(self.__path, 'wb') as file:
            pickle.dump(self.__pool, file)

    def load(self):
        if os.path.exists(self.__path):
            with open(self.__path, "rb") as file:
                self.__pool = pickle.load(file)
        else:
            self.__pool = {}

    def get_cache(self, func, *args, **kwargs):
        if self.__pool.get(func.__qualname__) is None:
            self.__pool[func.__qualname__] = {}
            return None
        return self.__pool[func.__qualname__].get(pickle.dumps([args, kwargs]))

    def set_cache(self, result, func, *args, **kwargs):
        if self.__pool.get(func.__qualname__) is None:
            self.__pool[func.__qualname__] = {}
        self.__pool[func.__qualname__][pickle.dumps([args, kwargs])] = result
        self.dump()

    def cache(self, max_time):
        def timeout(func):
            @wraps(func)
            def warpper(*args, **kwargs):
                result = self.get_cache(func, *args, **kwargs)
                if result is None or result["expired"] < time.time():
                    _result = func(*args, **kwargs)
                    self.set_cache({"value": _result, "expired": time.time() + max_time}, func, *args, **kwargs)
                    return _result
                else:
                    return result['value']
            return warpper
        return timeout

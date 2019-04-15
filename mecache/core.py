import time
import pickle
import hmac
from hashlib import sha1
from functools import wraps


class Aboriginal:

    @staticmethod
    def keyf(*args, **kwargs):
        key = pickle.dumps([args, kwargs])
        mac = hmac.new(b'mecache', msg=key, digestmod=sha1)
        return str(mac.hexdigest())


class BaseCache(Aboriginal):

    def get_cache(self, func, key, max_time):
        raise NotImplementedError("You must overwrite 'get_cache'!")

    def set_cache(self, result, func, key, max_time):
        raise NotImplementedError("You must overwrite 'set_cache'!")

    def cache(self, max_time, keyf=None):
        """
        if *args or **kwargs can't be pickle.dumps, use keyf to transform them

        example:

            def calc(*args, **kwargs):
                return str(args)+str(kwargs)

            c = Cache()
            @c.cache(max_time=10, keyf=calc)
            def add(x, y):
                return x + y

        """
        def timeout(func):
            @wraps(func)
            def warpper(*args, **kwargs):
                if keyf is None:
                    key = self.keyf(*args, **kwargs)
                else:
                    key = keyf(*args, **kwargs)
                # get result from cache
                result = self.get_cache(func, key, max_time)

                if result is None:  # cache invalid
                    result = func(*args, **kwargs)
                    # set new cache
                    self.set_cache(result, func, key, max_time)
                return result
            return warpper
        return timeout


class AioBaseCache(Aboriginal):

    async def get_cache(self, func, key, max_time):
        raise NotImplementedError("You must overwrite 'get_cache'!")

    async def set_cache(self, result, func, key, max_time):
        raise NotImplementedError("You must overwrite 'set_cache'!")

    def cache(self, max_time, keyf=None):
        """
        if *args or **kwargs can't be pickle.dumps, use keyf to transform them

        example:

            def calc(*args, **kwargs):
                return str(args)+str(kwargs)

            c = Cache()
            @c.cache(max_time=10, keyf=calc)
            async def add(x, y):
                return await do.something

        """
        def timeout(func):
            @wraps(func)
            async def warpper(*args, **kwargs):
                if keyf is None:
                    key = self.keyf(*args, **kwargs)
                else:
                    key = keyf(*args, **kwargs)
                # get result from cache
                result = await self.get_cache(func, key, max_time)

                if result is None:  # cache invalid
                    result = await func(*args, **kwargs)
                    # set new cache
                    await self.set_cache(result, func, key, max_time)
                return result
            return warpper
        return timeout

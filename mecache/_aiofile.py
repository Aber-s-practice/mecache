import os
import time
import pickle

import aiofiles

from .core import AioBaseCache


class AioFile(AioBaseCache):

    def __init__(self, path):
        self.__path = path
        os.makedirs(path, exist_ok=True)

    @property
    def path(self):
        return self.__path

    def _get_path(self, qual, key):
        path = os.path.join(os.path.join(self.path, qual), key)
        if os.path.exists(path):
            return path, True
        return path, False

    def _get_modifiy_time(self, filepath):
        """获取文件修改时间"""
        return os.stat(filepath).st_mtime

    async def get_cache(self, func, key, max_time):
        qual = func.__qualname__

        path, exist = self._get_path(qual, key)
        if exist and self._get_modifiy_time(path) >= time.time() - max_time:
            async with aiofiles.open(path, 'rb') as file:
                return pickle.loads(await file.read())
        return None

    async def set_cache(self, result, func, key, max_time):
        qual = func.__qualname__

        path, exist = self._get_path(qual, key)
        if not exist:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        async with aiofiles.open(path, 'wb') as f:
            await f.write(pickle.dumps(result))

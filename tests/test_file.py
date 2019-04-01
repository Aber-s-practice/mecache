import os
import time
import shutil
import atexit

from mecache import File

from . import SELF_PATH

TEMP = os.path.join(SELF_PATH, '.cache')

file = File(TEMP)

atexit.register(lambda: shutil.rmtree(TEMP))


@file.cache(5)
def add(x, y):
    time.sleep(3)
    return x + y


s = time.time()
assert add(1, 2) == 3                                               # 3s
assert time.time()-s < 3.1, 'Some error in first calculate'         # <0.001s
assert add(1, 2) == 3                                               # <0.01s
assert time.time()-s < 3.2, 'Some error in second calculate'        # <0.001s
time.sleep(5)                                                       # 5s
assert add(1, 2) == 3                                               # 3s
assert 11 < time.time() - s < 11.3, 'Some error in second calculate'

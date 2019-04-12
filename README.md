# mecache

An easy-to-use cache module

## How to use

Run `pip install mecache` or `pipenv install mecache` to install.

Built-in three cache modes, memory cache mode, file cache mode, redis cache mode.

You can control the time of cache failure by using the cache parameters.

### memory modes

```python
from mecache import Memory

memory = Memory()

# Cache failure after 60 seconds
@memory.cache(60)
def do(x, y):
    import time
    time.sleep(2)
    return x+y
```

### redis modes

```python
from mecache import Redis

# Refer to https://redis-py.readthedocs.io/en/latest/ for all parameters
redis = Redis(host="127.0.0.1", port='6379', db=0, password="password")

# Cache failure after 60 seconds
@redis.cache(60)
def do(x, y):
    import time
    time.sleep(2)
    return x+y
```

### file modes

```python
from mecache import File

# CACHE_PATH like '/var/tmp/test-cache'
file = File("CACHE_PATH")

# Cache failure after 60 seconds
@file.cache(60)
def do(x, y):
    import time
    time.sleep(2)
    return x+y
```

### asynchronous file modes

```python
from mecache import AioFile

# CACHE_PATH like '/var/tmp/test-cache'
file = AioFile("CACHE_PATH")

# Cache failure after 60 seconds
@file.cache(60)
async def do(x, y):
    return await do.something
```

## Advanced usage

If the parameters of a function are difficult to serialize using pickle, you can specify the rules that generate key by customizing `keyf`. The return value of the function `keyf`  must be a string.

```python
# a example in django view function

def key_by_user(request):
    return request.user.username

@memory.cache(60*60, keyf=key_by_user)
def home(request):
    return render(request, 'home.html')
```

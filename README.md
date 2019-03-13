# mecache
A memory-based, durable single-file cache

## How to use

It's easy to use, just introduce it and specify the absolute path to the cached file.

You can control the time of cache failure by using the cache parameters.

### Example:

```python
from mecache import Memory

memory = Memory("CACHE_PATH")

# Cache failure after 60 seconds
@memory.cache(60)
def do(x, y):
    import time
    time.sleep(2)
    return x+y
```

Then test it

```python
import time
time.clock()
do(1, 2)
print(time.clock())
do(1, 2)
print(time.clock())
do(2, 3)
print(time.clock())
```

import functools
import requests
from collections import OrderedDict
import psutil


def cache(max_limit=64):

    def internal(f):

        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            deco._count[cache_key] += 1

            if cache_key in deco._cache:
                deco._cache.move_to_end(cache_key, last=True)
                return deco._cache[cache_key]

            result = f(*args, **kwargs)

            if len(deco._cache) >= max_limit:
                least_used_key = min(deco._count, key=deco._count.get)
                deco._cache.pop(least_used_key)
                del deco._count[least_used_key]

            deco._cache[cache_key] = result
            deco._count[cache_key] = 0

            return result

        deco._cache = OrderedDict()
        deco._count = OrderedDict()
        return deco

    return internal


def memory(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        result = f(*args, **kwargs)
        end_memory = process.memory_info().rss
        print(f'Memory usage of {f.__name__}: {end_memory - start_memory} bytes')

        return result

    return wrapper


@memory
@cache
def fetch_url(url, first_n=100):
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


# TEST


fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
fetch_url('https://reddit.com')

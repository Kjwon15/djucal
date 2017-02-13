import functools
import time


def cache(seconds):
    def decorator(function):
        cached_values = {}

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = (args, frozenset(kwargs.items()))
            if key in cached_values:
                timestamp, value = cached_values[key]
                if now <= timestamp + seconds:
                    return value

            value = function(*args, **kwargs)
            cached_values[key] = (now, value)
            return value

        return wrapper
    return decorator

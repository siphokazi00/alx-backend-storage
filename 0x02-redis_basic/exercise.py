#!/usr/bin/env python3
"""
Takes a data argument and returns a string
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """Initialize Cache with Redis client and flush DB"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """Decorator to count how many times a method is called"""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """Decorator to store input and output history for a method"""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            input_key = f"{key}:inputs"
            output_key = f"{key}:outputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(output))
            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a unique key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn:
            Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and apply optional conversion func"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis"""
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis"""
        return self.get(key, int)


def replay(method: Callable) -> None:
    """Replay the history of calls for a given method"""
    r = method.__self__._redis
    method_name = method.__qualname__

    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for inp, out in zip(inputs, outputs):
        inp_str = inp.decode('utf-8')
        out_str = out.decode('utf-8')
        print(f"{method_name}(*{inp_str}) -> {out_str}")


# Example Usage:
if __name__ == "__main__":
    cache = Cache()

    # Store different types of data
    key1 = cache.store("foo")
    key2 = cache.store("bar")
    key3 = cache.store(42)

    # Replay the history of store calls
    replay(cache.store)

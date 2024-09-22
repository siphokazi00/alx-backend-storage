#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable


class Cache:
    def __init__(self):
        """Initialize Cache with Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(self, method: Callable) -> Callable:
        """Decorator to count how many times a URL is accessed."""
        @wraps(method)
        def wrapper(url: str, *args, **kwargs):
            self._redis.incr(f"count:{url}")
            return method(url, *args, **kwargs)
        return wrapper

    def cache_page(self, method: Callable) -> Callable:
        """Decorator to cache the page content for 10 seconds."""
        @wraps(method)
        def wrapper(url: str, *args, **kwargs):
            cached_content = self._redis.get(f"cache:{url}")
            if cached_content:
                return cached_content.decode('utf-8')

            # Fetch page content if not cached
            page_content = method(url, *args, **kwargs)
            # Store the page content in cache with expiration time of 10s
            self._redis.setex(f"cache:{url}", 10, page_content)
            return page_content
        return wrapper


cache = Cache()


@cache.count_calls
@cache.cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache the result."""
    response = requests.get(url)
    return response.text


# Example Usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"

    # Fetch the page and display the access count and content
    page_content = get_page(url)
    print(f"Page content: {page_content[:200]}...")
    access_count = cache._redis.get(f"count:{url}").decode('utf-8')
    print(f"URL {url} was accessed {access_count} times.")

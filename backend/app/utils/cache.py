"""
Caching utilities for faster response times
"""
from cachetools import TTLCache
import functools


# Cache for warehouse queries (TTL: 1 hour = 3600 seconds)
warehouse_cache = TTLCache(maxsize=100, ttl=3600)

# Cache for shipping charge queries (TTL: 30 minutes = 1800 seconds)
shipping_cache = TTLCache(maxsize=500, ttl=1800)


def cache_warehouse_query(func):
    """
    Decorator to cache warehouse query results
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Create cache key from arguments
        cache_key = f"{func.__name__}:{args}:{kwargs}"
        
        if cache_key in warehouse_cache:
            return warehouse_cache[cache_key]
        
        result = await func(*args, **kwargs)
        warehouse_cache[cache_key] = result
        return result
    
    return wrapper


def cache_shipping_query(func):
    """
    Decorator to cache shipping charge query results
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Create cache key from arguments
        cache_key = f"{func.__name__}:{args}:{kwargs}"
        
        if cache_key in shipping_cache:
            return shipping_cache[cache_key]
        
        result = await func(*args, **kwargs)
        shipping_cache[cache_key] = result
        return result
    
    return wrapper


def clear_warehouse_cache():
    """Clear warehouse cache"""
    warehouse_cache.clear()


def clear_shipping_cache():
    """Clear shipping cache"""
    shipping_cache.clear()


def clear_all_cache():
    """Clear all caches"""
    clear_warehouse_cache()
    clear_shipping_cache()

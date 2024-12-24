
from functools import lru_cache, wraps
import time

def timed_lru_cache(maxsize=128, ttl=10):
    def decorator(func):
        func = lru_cache(maxsize=maxsize)(func)
        cache_info = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            
            if cache_key in cache_info:
                cached_result, timestamp = cache_info[cache_key]
                if time.time() - timestamp < ttl:  # If cache is still valid
                    print("Returning cached result")
                    return cached_result
            
            print("Fetching data from backend...")
            result = func(*args, **kwargs)
            cache_info[cache_key] = (result, time.time())  # Update cache with the current time
            return result
        
        wrapper.cache_clear = func.cache_clear
        return wrapper
    
    return decorator


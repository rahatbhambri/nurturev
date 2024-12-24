import time
from functools import wraps


WINDOW_SIZE = 60 
RATE_LIMIT = 5  

client_requests = {}

def sliding_window_rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_ip = kwargs.get('client_ip')  

        if client_ip not in client_requests:
            client_requests[client_ip] = []

        current_time = time.time()
        request_times = client_requests[client_ip]
        
        while request_times and request_times[0] < current_time - WINDOW_SIZE:
            request_times.pop(0)
        
        if len(request_times) < RATE_LIMIT:
            request_times.append(current_time)
            return func(*args, **kwargs)  
        else:
            return "Rate limit exceeded", 429 

    return wrapper

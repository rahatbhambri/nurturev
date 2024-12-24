import pytest
from limiter import *

def test_limiter():
    mockIp = "192.168.1.1"
    
    for i in range(5):
       assert sliding_window_rate_limiter(mockIp) == True
        
    assert sliding_window_rate_limiter(mockIp) == False

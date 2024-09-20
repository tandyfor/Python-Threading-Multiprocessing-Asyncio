import time
from threading import Lock

class Throttle:
    def __init__(self, rate):
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0
        self.last = 0

    def consume(self, amount=1):
        with self._consume_lock:
            now = time.time()
            if self.last == 0:
                self.last = now
            
            elapsed = now - self.last
            
            if int(elapsed * self.rate):
                self.tokens += int(elapsed * self.rate)
                self.last = now

            self.tokens = (self.rate 
                           if self.tokens > self.rate 
                           else self.tokens)
            
            if self.tokens >= amount:
                self.tokens -= amount
            else:
                amount = 0

            return amount

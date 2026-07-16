#!/usr/bin/env python3
"""
Microservices Connection status and circuit breaker validation lab.
"""

import time
import sys

class CircuitBreaker:
    def __init__(self, failure_threshold=3):
        self.failure_threshold = failure_threshold
        self.failure_count = 0
        self.state = "CLOSED" # CLOSED, OPEN

    def execute_call(self):
        if self.state == "OPEN":
            print("Warning: Circuit is OPEN. Blocking connection request.")
            return False
            
        print("Attempting connection to backend service...")
        # Simulate a connection failure
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            print("Error: Failure limit exceeded. Tripping circuit to OPEN.")
        return True

def main():
    print("=== Starting Microservices Circuit Breaker Lab ===")
    breaker = CircuitBreaker()
    
    # Run test iterations
    for i in range(4):
        breaker.execute_call()
        time.sleep(0.1)
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Asynchronous Kafka Consumer/Producer event simulation script.
"""

import json
import time

def run_event_stream():
    print("=== Starting Event Stream Simulator ===")
    
    # 1. Simulate publishing an event message to topic
    topic = "user-transactions"
    event_message = {
        "event": "UserPaymentCompleted",
        "user_id": "usr_9981",
        "amount": 250.00,
        "timestamp": time.time()
    }
    
    print(f"Producer published message to topic [{topic}]:")
    print(json.dumps(event_message, indent=2))
    
    # 2. Simulate consumer processing event
    time.sleep(0.5)
    print(f"\nConsumer group 'billing-processors' consumed message from topic [{topic}]:")
    print(f"Action: Billing status updated for User: {event_message['user_id']}.")
    print("========================================")

if __name__ == "__main__":
    run_event_stream()

#!/usr/bin/env python3
"""
Project 4: Enterprise AI Copilot Backend (Authentication, Authorization, Rate Limiting)
Skills Focus: Redis-style Token Bucket Rate Limiting, Tenant Isolation, Audit Logs.

This script implements a secure gateway layer that runs token bucket rate limits,
verifies tenant permissions, and writes logs to audit registries.
"""

import json
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity=5, leak_rate_per_sec=1):
        self.capacity = capacity
        self.leak_rate = leak_rate_per_sec
        # Database tracking user bucket values: { user_id: {tokens, last_update} }
        self.buckets = {}

    def is_rate_limited(self, user_id) -> bool:
        now = time.time()
        
        if user_id not in self.buckets:
            self.buckets[user_id] = {"tokens": self.capacity, "last_update": now}
            
        bucket = self.buckets[user_id]
        
        # Calculate leaked tokens based on elapsed time
        elapsed = now - bucket["last_update"]
        added_tokens = elapsed * self.leak_rate
        
        # Update bucket tokens without exceeding capacity
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + added_tokens)
        bucket["last_update"] = now
        
        # Check token balance
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1 # Consume token
            return False # Access granted
        else:
            return True # Rate limited

class SecureCopilotGateway:
    def __init__(self):
        self.rate_limiter = TokenBucketRateLimiter(capacity=3, leak_rate_per_sec=0.5)
        # Mock database mapping API keys to user configurations
        self.api_keys_db = {
            "key_user_01": {"user_id": "user_alpha", "role": "Premium", "tenant_id": "tenant_a"},
            "key_user_02": {"user_id": "user_beta", "role": "Free", "tenant_id": "tenant_b"}
        }
        self.audit_log = []

    def log_audit_trail(self, user_id, action, status, detail):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "action": action,
            "status": status,
            "detail": detail
        }
        self.audit_log.append(log_entry)
        print(f"[AUDIT LOG] {json.dumps(log_entry)}")

    def process_request(self, api_key, action_payload):
        print(f"\n[GATEWAY] Processing request for API Key: '{api_key}'")
        
        # 1. Authenticate API Key
        if api_key not in self.api_keys_db:
            self.log_audit_trail("anonymous", "API_ACCESS", "DENIED", "Invalid API key.")
            return {"status_code": 401, "error": "Unauthorized API key"}
            
        user_info = self.api_keys_db[api_key]
        user_id = user_info["user_id"]
        
        # 2. Check Rate Limits
        if self.rate_limiter.is_rate_limited(user_id):
            self.log_audit_trail(user_id, "API_ACCESS", "RATE_LIMITED", "Token bucket empty.")
            return {"status_code": 429, "error": "Too Many Requests. Rate limit exceeded."}
            
        # 3. Check Tenant Authorization
        requested_tenant = action_payload.get("target_tenant")
        if user_info["tenant_id"] != requested_tenant:
            self.log_audit_trail(
                user_id, "RESOURCE_ACCESS", "DENIED", 
                f"Tenant mismatch. User: {user_info['tenant_id']}, Resource: {requested_tenant}"
            )
            return {"status_code": 403, "error": "Forbidden. Tenant access mismatch."}
            
        # 4. Action approved
        self.log_audit_trail(
            user_id, "RESOURCE_ACCESS", "APPROVED", 
            f"Successfully accessed resource on tenant: '{requested_tenant}'"
        )
        return {"status_code": 200, "data": "Access approved. Processing copilot calculations."}

def main():
    print("Project 4: Enterprise AI Copilot Backend (Access Security Gateway)")
    print("="*60)
    
    gateway = SecureCopilotGateway()
    
    # 1. Valid request (approved)
    res1 = gateway.process_request(
        api_key="key_user_01",
        action_payload={"target_tenant": "tenant_a"}
    )
    print(f"Gateway Response: {res1['status_code']}")
    
    # 2. Tenant mismatch request (denied)
    res2 = gateway.process_request(
        api_key="key_user_01",
        action_payload={"target_tenant": "tenant_b"} # User key_user_01 belongs to tenant_a
    )
    print(f"Gateway Response: {res2['status_code']}")
    
    # 3. Trigger rate limiting
    print("\n[TEST] Sending multiple requests rapidly to exhaust token bucket...")
    for i in range(4):
        res = gateway.process_request(
            api_key="key_user_02",
            action_payload={"target_tenant": "tenant_b"}
        )
        print(f"Request {i+1} Response: {res['status_code']}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Project 1: Enterprise AI API Platform (FastAPI, Authentication, Authorization)
Skills Focus: FastAPI Routing, Pydantic Schema Validation, JWT Claims, RBAC Auditing.

This script simulates a FastAPI microservice that handles user request models,
verifies JWT authorization headers, and runs RBAC (Role-Based Access Control) rules.
"""

import json
import time

class PydanticModelInferenceRequest:
    def __init__(self, prompt: str, max_tokens: int = 128):
        self.prompt = prompt
        self.max_tokens = max_tokens

    def validate(self):
        """Simulates Pydantic validation checks."""
        if not self.prompt or len(self.prompt) < 3:
            raise ValueError("[VALIDATION ERROR] Prompt must be at least 3 characters.")
        if self.max_tokens <= 0:
            raise ValueError("[VALIDATION ERROR] Max tokens must be greater than 0.")
        return {"prompt": self.prompt, "max_tokens": self.max_tokens}

class FastAPIAuthGate:
    def __init__(self):
        # Mock identity provider registration database
        self.public_keys = {"iss_server_01": "RSA_PUBLIC_KEY_KEYCLOAK_2026"}

    def decode_jwt(self, auth_header):
        """Simulates stateless decoding of asymmetric signed JWT tokens."""
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or malformed Authorization header."}
            
        token = auth_header.split(" ")[1]
        
        # Simulate decoding JWT payload claims
        if token == "valid_admin_token":
            return {
                "sub": "user_402",
                "role": "Admin",
                "tenant_id": "tenant_hr_01",
                "exp": time.time() + 3600,
                "iss": "iss_server_01"
            }
        elif token == "valid_reader_token":
            return {
                "sub": "user_109",
                "role": "Reader",
                "tenant_id": "tenant_finance_02",
                "exp": time.time() + 3600,
                "iss": "iss_server_01"
            }
        else:
            return {"error": "Signature verification failed. Invalid token."}

class EnterpriseAIAPIPlatform:
    def __init__(self):
        self.auth_gate = FastAPIAuthGate()

    def run_inference_endpoint(self, auth_header, prompt_text, tokens_limit):
        print(f"API Server: Received request on route: '/api/v1/inference'")
        print(f"Header: Authorization: '{auth_header}'")
        
        # 1. JWT validation middleware step
        claims = self.auth_gate.decode_jwt(auth_header)
        if "error" in claims:
            error_response = {"status_code": 401, "detail": claims["error"]}
            print(f"[FASTAPI MIDDLEWARE] {json.dumps(error_response)}")
            return error_response
            
        print(f"[FASTAPI MIDDLEWARE] Token validated. User: {claims['sub']} (Role: {claims['role']})")
        
        # 2. Pydantic request body validation step
        try:
            req = PydanticModelInferenceRequest(prompt=prompt_text, max_tokens=tokens_limit)
            validated_data = req.validate()
            print(f"[PYDANTIC] Request payload validated successfully: {json.dumps(validated_data)}")
        except ValueError as e:
            error_response = {"status_code": 422, "detail": str(e)}
            print(f"[FASTAPI GATEWAY] {json.dumps(error_response)}")
            return error_response

        # 3. RBAC authorization scope check step
        required_role = "Admin"
        if claims["role"] != required_role:
            forbidden_response = {
                "status_code": 403,
                "detail": f"RBAC Denied. Required role: {required_role}. User role: {claims['role']}"
            }
            print(f"[AUTHORIZATION GATE] {json.dumps(forbidden_response)}")
            return forbidden_response
            
        print("[AUTHORIZATION GATE] RBAC Audited. Access granted.")
        
        # 4. Process request
        response = {
            "status_code": 200,
            "data": {
                "model": "Llama-3-8B",
                "choices": [{"text": f"Simulated prediction text for prompt: '{prompt_text}'"}],
                "tenant_owner": claims["tenant_id"]
            }
        }
        print(f"[FASTAPI ENDPOINT] Returning response: {json.dumps(response, indent=2)}")
        return response

def main():
    print("Project 1: Enterprise AI API Platform (FastAPI Auth System)")
    print("="*60)
    
    platform = EnterpriseAIAPIPlatform()
    
    # Simulate valid Admin request (access granted)
    platform.run_inference_endpoint(
        auth_header="Bearer valid_admin_token",
        prompt_text="Audit contract clauses for liability limits.",
        tokens_limit=64
    )
    
    print("\n" + "-"*40 + "\n")
    
    # Simulate Reader request (denied by RBAC)
    platform.run_inference_endpoint(
        auth_header="Bearer valid_reader_token",
        prompt_text="Audit contract clauses for liability limits.",
        tokens_limit=64
    )

if __name__ == "__main__":
    main()

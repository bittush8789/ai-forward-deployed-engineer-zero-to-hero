#!/usr/bin/env python3
"""
Project 2: AI Model Serving Platform (Flask, FastAPI, API Gateway Routing)
Skills Focus: Application Factory Blueprint Routing, API Gateway Forwarding.

This script simulates an API Gateway load balancing calls between a fast
FastAPI LLM endpoint and a legacy Flask microservice serving Scikit-Learn classifiers.
"""

import json

class MockFlaskScikitService:
    """Simulates a legacy Flask microservice running a Scikit-Learn classifier."""
    def handle_legacy_classification(self, request_payload):
        print("[FLASK SERVER] Received request on blueprint: '/blueprints/classify'")
        # Simulate processing request
        features = request_payload.get("features", [])
        print(f"[FLASK SERVER] Running Scikit-Learn classifier over features: {features}")
        
        response = {
            "model_type": "Scikit-Learn Random Forest",
            "prediction": "LOW_RISK",
            "probability": 0.9412
        }
        print(f"[FLASK SERVER] Returning response: {json.dumps(response)}")
        return response

class MockFastAPILLMService:
    """Simulates a modern FastAPI service serving LLM models."""
    def handle_inference(self, request_payload):
        print("[FASTAPI SERVER] Received request on async route: '/v1/chat'")
        prompt = request_payload.get("prompt", "")
        print(f"[FASTAPI SERVER] Processing LLM prompt: '{prompt}'")
        
        response = {
            "model_type": "Llama-3-8B",
            "choices": [{"text": "Completed LLM text predictions."}]
        }
        print(f"[FASTAPI SERVER] Returning response: {json.dumps(response)}")
        return response

class APIEndpointGateway:
    def __init__(self):
        self.flask_service = MockFlaskScikitService()
        self.fastapi_service = MockFastAPILLMService()

    def route_request(self, path, payload):
        print(f"[GATEWAY] Incoming Request Path: '{path}'")
        
        # Route based on endpoint path
        if path.startswith("/api/v1/legacy"):
            print(" -> Gateway Routing Decision: Forward to Legacy Flask Service.")
            response = self.flask_service.handle_legacy_classification(payload)
        elif path.startswith("/api/v1/inference"):
            print(" -> Gateway Routing Decision: Forward to FastAPI Serving Service.")
            response = self.fastapi_service.handle_inference(payload)
        else:
            response = {"error": "404 Route Not Found"}
            print(f"[GATEWAY] Error: {response['error']}")
            
        return response

def main():
    print("Project 2: AI Model Serving Platform (API Gateway Routing)")
    print("="*60)
    
    gateway = APIEndpointGateway()
    
    # Route request to legacy Flask classifier
    gateway.route_request(
        path="/api/v1/legacy/classify",
        payload={"features": [0.44, 0.12, 0.95]}
    )
    
    print("\n" + "-"*40 + "\n")
    
    # Route request to FastAPI LLM endpoint
    gateway.route_request(
        path="/api/v1/inference/chat",
        payload={"prompt": "Draft contract summary lines."}
    )

if __name__ == "__main__":
    main()

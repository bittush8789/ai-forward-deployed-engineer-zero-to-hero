# Practice Tasks: Module 8 - FastAPI Server Implementations

This document outlines step-by-step tasks to configure API routing for model serving.

---

## Task 1: Create FastAPI Predictor Router
*   **Goal**: Write a Python script exposing prediction endpoints using FastAPI.
*   **Step-by-Step Instructions**:
    1. Create a script `fastapi_server.py`:
       ```python
       tee /tmp/fastapi_server.py << 'EOF'
       from fastapi import FastAPI
       from pydantic import BaseModel

       app = FastAPI()

       class PredictRequest(BaseModel):
           data: list

       @app.post("/predict")
       def predict(req: PredictRequest):
           return {"status": "success", "length": len(req.data)}
       EOF
       ```
*   **Verification**:
    Verify the script exists:
    ```bash
    cat /tmp/fastapi_server.py | grep "PredictRequest"
    ```

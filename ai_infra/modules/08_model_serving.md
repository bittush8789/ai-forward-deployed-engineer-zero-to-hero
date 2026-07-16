# Module 8: Multi-Model Serving Gateways & FastAPI Integrations

## 1. Theory (40%)
Model Serving involves exposing machine learning models as web APIs. Production serving platforms must support both real-time, low-latency online serving and high-throughput batch serving.

```
+-------------------------------------------------------------------------------------------------+
|                                        Model Serving Gateway                                    |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |   HTTP/gRPC API   | ---> |   FastAPI Router  | ---> |   Model Worker    |                   |
|   |   (Client query)  |      |   (Auth/Routing)  |      |   (Inference)     |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v (Trace Span)             v (Trace Span)             v (Trace Span)                |
|   +---------+--------------------------+--------------------------+-------------------------+   |
|   |                            Observability & Telemetry Service                            |   |
|   |   - Logs latency, throughput, and token count metrics                                   |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Online Serving**: Exposing models via HTTP or gRPC endpoints to serve real-time predictions with low latency.
*   **Batch Serving**: Processing large datasets offline, optimizing throughput.
*   **API Gateways**: Routing client queries, enforcing authorization, and managing request traffic.

---

## 2. Architecture Deep Dive

Production model serving architectures use a gateway pattern:
*   **FastAPI Router**: Handles request validation, authentication, and routing.
*   **Model Workers**: Host model instances and execute inference.
*   **Telemetry Collectors**: Log metrics and traces to monitoring systems.

---

## 3. Internal Working

### Request Processing Loop
1.  **Request Validation**: The API gateway validates inputs against defined schemas.
2.  **Inference Routing**: The gateway routes queries to the model worker instances.
3.  **Output Formatting**: The gateway formats responses before returning them to clients.

---

## 4. Tool Comparison

| Feature | FastAPI | Ray Serve | standalone KServe |
|---|---|---|---|
| **Primary Focus** | General-purpose Python web APIs | Distributed Python model serving | Kubernetes-native serving |
| **Routing** | Python-based async routing | Dynamic HTTP proxies | Istio VirtualServices |
| **Concurrency** | Async loop execution | Worker pool execution | Replica scaling |

---

## 5. Installation Guide
Install the core packages:
```bash
pip install fastapi uvicorn
```

---

## 6. Setup Guide
Create a basic FastAPI model serving script `app.py`:
```python
# /tmp/app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/predict")
def predict(query: Query):
    # Simulated model output
    return {"prediction": f"Processed: {query.text}"}
```
Write this script to disk:
```bash
mkdir -p /tmp/serving-lab
tee /tmp/serving-lab/app.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/predict")
def predict(query: Query):
    return {"prediction": f"Processed: {query.text}"}
EOF
```

---

## 7. Commands
```bash
# Start the FastAPI server using Uvicorn (simulated command)
# uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 8. Hands-On Labs
Verify the FastAPI configuration file exists:
```bash
cat /tmp/serving-lab/app.py | grep -i "fastapi"
```

---

## 9. Production Operations

### Scaling FastAPI Servers
Deploy FastAPI servers using ASGI containers (such as Gunicorn with Uvicorn workers) to utilize multiple CPU cores.

---

## 10. Monitoring
Expose Prometheus metrics (such as request rates, status codes, and latency) from your FastAPI application using middleware.

---

## 11. Security
Enforce TLS encryption on all endpoints, and use API keys or JWT tokens to secure access.

---

## 12. Cost Optimization
Configure connection pooling to reduce database and model worker connection overhead.

---

## 13. Troubleshooting

### Task 13.1: API Connection Timeouts
*   **Symptom**: Client requests fail with `504 Gateway Timeout`.
*   **Root Cause**: The model worker takes longer to execute inference than the gateway's timeout configuration.
*   **Resolution Strategy**:
    *   Increase the gateway timeout limit.
    *   Optimize model execution speeds using quantization or TensorRT engines.

---

## 14. Enterprise Case Studies

### Microservice Orchestration at Netflix
Netflix uses API gateways to manage model serving microservices. By implementing unified routing, rate limiting, and centralized monitoring, they coordinate traffic across recommendation models.

---

## 15. Interview Questions

### Q1: What is the difference between synchronous and asynchronous routers in Python?
*   **Answer**: Synchronous routers block the execution thread until a response is returned. Asynchronous routers (like FastAPI) release the thread while waiting for I/O operations, improving concurrency.

### Q2: Why do we use API gateways in model serving architectures?
*   **Answer**: API gateways centralize routing, authentication, rate limiting, and logging, decoupling client requests from backend model workers.

---

## 16. AI FDE Perspective

### Deploying High-Performance API Gateways
As an AI Forward Deployed Engineer (FDE), you often configure serving platforms:
*   **Concurrency Settings**: Adjust worker thread configurations to maximize CPU/GPU utilization without overloading nodes:
    ```bash
    # Run Uvicorn with multiple workers
    # uvicorn app:app --workers 4 --host 0.0.0.0 --port 8000
    ```
This ensures high-performance serving under concurrent traffic loads.

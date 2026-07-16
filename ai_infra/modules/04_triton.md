# Module 4: Triton Inference Server & Dynamic Batching Pipelines

## 1. Theory (40%)
NVIDIA Triton Inference Server is an enterprise-grade model serving platform. It simplifies model deployment by supporting multiple frameworks (such as PyTorch, ONNX, TensorRT, and TensorFlow) and optimizing GPU utilization.

```
+-------------------------------------------------------------------------------------------------+
|                                    Triton Inference Server                                      |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Inference Queue                                     |   |
|   |   - Collects incoming client requests asynchronously                                    |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Dynamic Batcher                                        |   |
|   |   - Combines multiple individual queries into a single batch within a time window       |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Execute Batch)                                     |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  GPU Core Engines                                       |   |
|   |   - TensorRT / ONNX models run inference at high throughput                             |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Model Repository**: A structured file directory containing model checkpoints and configuration files (`config.pbtxt`).
*   **Dynamic Batching**: Combining individual client requests into a single batch within a time window, maximizing GPU compute efficiency.
*   **Concurrent Model Execution**: Running multiple models (or multiple instances of the same model) concurrently on a single GPU.

---

## 2. Architecture Deep Dive

Triton is designed for high-performance serving:
*   **Model Pipelines**: Triton allows defining model pipelines (ensembles) to chain preprocessing, model inference, and postprocessing steps.
*   **Dynamic Schedulers**: Triton routes requests to the appropriate model instance queue based on framework and device configurations.

---

## 3. Internal Working

### Dynamic Batching Pipeline
1.  **Queue Request**: Client requests are added to the model's inference queue.
2.  **Batch Collection**: The dynamic batcher groups requests based on the configured maximum batch size and delay window.
3.  **Kernel Execution**: The batch is sent to the GPU core engine for inference, returning responses to the respective client connections.

---

## 4. Tool Comparison

| Feature | Triton Inference Server | FastAPI / Custom Python |
|---|---|---|
| **Primary Focus** | Production-grade multi-model serving | General-purpose API routing |
| **Dynamic Batching**| Native C++ implementation | Requires custom Python queue logic |
| **Concurreny** | Thread-isolated executions | Python async execution limits |

---

## 5. Installation Guide
Deploy Triton using the official NVIDIA container:
```bash
# Pull the latest Triton container image (simulated command)
# docker pull nvcr.io/nvidia/tritonserver:23.08-py3
```

---

## 6. Setup Guide
Configure the model repository directory structure:
```bash
mkdir -p /tmp/triton-repo/simple_model/1/
```
Create a configuration file `config.pbtxt` in `/tmp/triton-repo/simple_model/`:
```properties
# config.pbtxt definition config
name: "simple_model"
platform: "onnxruntime_onnx"
max_batch_size: 8
input [
  {
    name: "input_0"
    data_type: TYPE_FP32
    dims: [ 16 ]
  }
]
output [
  {
    name: "output_0"
    data_type: TYPE_FP32
    dims: [ 16 ]
  }
]
dynamic_batching {
  max_queue_delay_microseconds: 5000
}
```

---

## 7. Commands
```bash
# Run Triton server container pointing to the model repository (simulated command)
# docker run --gpus=1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
#   -v /tmp/triton-repo:/models nvcr.io/nvidia/tritonserver:23.08-py3 tritonserver --model-repository=/models
```

---

## 8. Hands-On Labs
Write a Python script to verify Triton service endpoints:
```python
# /tmp/triton_test.py
import socket

def check_triton_endpoints():
    ports = {"HTTP (8000)": 8000, "gRPC (8001)": 8001, "Metrics (8002)": 8002}
    print("=== Triton Port Status Checks ===")
    for name, port in ports.items():
        try:
            s = socket.create_connection(("localhost", port), timeout=1)
            s.close()
            print(f"{name}: ONLINE")
        except Exception:
            print(f"{name}: OFFLINE")

if __name__ == '__main__':
    check_triton_endpoints()
```
Run the status check:
```bash
python3 /tmp/triton_test.py
```

---

## 9. Production Operations

### Designing Model Pipelines
Chain preprocessing and postprocessing steps inside Triton using **Ensemble Models** to reduce data transfer overhead between the application server and GPU.

---

## 10. Monitoring
Triton exports Prometheus metrics at port 8002 (including queue latency, execution latency, and request counts), allowing you to monitor engine health.

---

## 11. Security
Use network policies and API gateways to restrict access to Triton's internal gRPC/HTTP ports.

---

## 12. Cost Optimization
Enable dynamic batching to maximize GPU utilization, reducing the number of active GPU instances required to serve traffic.

---

## 13. Troubleshooting

### Task 13.1: Model Loading Failures
*   **Symptom**: Triton logs show `Failed to load model: ... missing required file`.
*   **Root Cause**: The model repository directory structure does not follow Triton's naming conventions, or the configuration file (`config.pbtxt`) is missing.
*   **Resolution Strategy**:
    *   Verify the directory structure includes the version folder (e.g., `1/model.onnx`).
    *   Inspect logs for configuration parsing errors:
        ```bash
        # Review container logs
        ```

---

## 14. Enterprise Case Studies

### Multi-Model Serving at PayPal
PayPal uses Triton to serve fraud detection models. By running multiple model frameworks concurrently on shared GPUs and enabling dynamic batching, they optimized compute utilization, reducing latency and infrastructure costs.

---

## 15. Interview Questions

### Q1: What is dynamic batching, and how does it optimize GPU performance?
*   **Answer**: Dynamic batching combines individual client requests into a single batch within a time window, maximizing GPU compute efficiency and throughput.

### Q2: Explain the structure of Triton's Model Repository.
*   **Answer**: The repository is a structured directory containing model checkpoints (version folders, e.g., `1/model.onnx`) and configuration files (`config.pbtxt`) that declare input/output shapes and platform backends.

---

## 16. AI FDE Perspective

### Tuning Triton Concurrency for Low-Latency Serving
As an AI Forward Deployed Engineer (FDE), you often configure model serving layers:
*   **Model Instances**: Tune the instance count in `config.pbtxt` to match the target host's hardware capabilities:
    ```properties
    # Allocate multiple execution instances on the GPU
    instance_group [
      {
        count: 2
        kind: KIND_GPU
      }
    ]
    ```
This allows Triton to execute parallel inference requests concurrently, improving performance.

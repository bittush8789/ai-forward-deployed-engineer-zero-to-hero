# Module 9: Inference Optimization, TensorRT & ONNX Compiler Pipelines

## 1. Theory (40%)
Inference Optimization involves improving the performance, throughput, and memory utilization of machine learning models during serving.

```
+-------------------------------------------------------------------------------------------------+
|                                     Inference Optimization Pipeline                             |
|                                                                                                 |
|   +--------------------+      +--------------------+      +--------------------+                |
|   |  1. PyTorch Model  | ---> | 2. ONNX Export     | ---> | 3. TensorRT Engine |                |
|   |  (Checkpoints)     |      | (Graph definition) |      | (FP16/INT8 compilation)             |
|   +--------------------+      +--------------------+      +---------+----------+                |
|                                                                     |                           |
|                                                                     v                           |
|                                                           +---------+----------+                |
|                                                           | 4. Optimized Engine|                |
|                                                           | (Run on GPU cores) |                |
|                                                           +--------------------+                |
+-------------------------------------------------------------------------------------------------+
```

### Optimization Techniques
*   **Quantization**: Converting model weights from high precision (like FP32) to lower precision (like FP16, INT8, or FP8) to reduce memory usage and accelerate execution.
*   **Pruning**: Removing redundant parameters or connections, reducing model complexity.
*   **Tensor Parallelism**: Splitting model layers horizontally across multiple GPUs within a node to parallelize matrix multiplications.
*   **Pipeline Parallelism**: Splitting model layers vertically across multiple GPUs, running execution steps in pipeline stages.

---

## 2. Architecture Deep Dive

Optimization pipelines translate dynamic graphs into high-performance engines:
*   **ONNX (Open Neural Network Exchange)**: An open format built to represent machine learning models, enabling model transfer across frameworks.
*   **TensorRT**: NVIDIA's high-performance inference compiler that optimizes model graphs and compiles execution engines for specific GPU architectures.

---

## 3. Internal Working

### TensorRT Optimization Passes
1.  **Layer Fusion**: Combining operations (such as convolution, bias, and activation) into single execution kernels.
2.  **Kernel Selection**: Selecting the fastest execution kernels based on the target GPU hardware.
3.  **Quantization Calibration**: Running calibration steps on representative datasets to minimize accuracy loss during INT8 compilation.

---

## 4. Tool Comparison

| Feature | TensorRT | ONNX Runtime | PyTorch (Standard) |
|---|---|---|---|
| **Primary Focus** | NVIDIA-specific GPU optimization | Multi-hardware inference engine | Development and training |
| **Quantization** | FP16, INT8, FP8 | FP16, INT8 | FP16, INT8, INT4 |
| **Portability** | NVIDIA GPUs only | Cross-platform (CPU, GPU, Edge) | Python runtime environments |

---

## 5. Installation Guide
Install the TensorRT compiler on Ubuntu:
```bash
# Install TensorRT dependencies via apt
sudo apt-get install -y tensorrt || echo "TensorRT package not found on host"
```

---

## 6. Setup Guide
Verify ONNX and TensorRT CLI compilation tools:
```bash
# Check if trtexec is available (simulated command)
# trtexec --help
```

---

## 7. Commands
```bash
# Compile an ONNX model into a TensorRT engine (simulated command)
# trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# Run performance benchmarking on an ONNX model (simulated command)
# onnxruntime_perf_test model.onnx
```

---

## 8. Hands-On Labs
Verify the ONNX runtime library can be imported in Python:
```python
# /tmp/onnx_test.py
def check_onnx_imports():
    try:
        import onnxruntime
        print("Success: ONNX Runtime library available.")
    except ImportError:
        print("ONNX Runtime not installed. Run: pip install onnxruntime")

if __name__ == '__main__':
    check_onnx_imports()
```
Run the import validation:
```bash
python3 /tmp/onnx_test.py
```

---

## 9. Production Operations

### Designing Optimization Pipelines
Export models to ONNX and compile them into TensorRT engines during build phases, ensuring only optimized models are deployed to production.

---

## 10. Monitoring
Monitor GPU kernel execution times and memory latency using profiling tools like **NVIDIA Nsight Systems**.

---

## 11. Security
Secure compiled engine files to prevent unauthorized extraction of model weights.

---

## 12. Cost Optimization
Enable model quantization (such as FP16) to reduce memory usage, allowing larger models to run on cheaper GPU instances.

---

## 13. Troubleshooting

### Task 13.1: TensorRT Compilation Errors
*   **Symptom**: `trtexec` fails during compilation with `Unsupported ONNX operator`.
*   **Root Cause**: The model uses operations or custom layers that are not supported by the TensorRT compiler version.
*   **Resolution Strategy**:
    *   Implement custom plugins in C++ or Python to handle unsupported operations.
    *   Verify operator compatibility using ONNX validation tools before compiling.

---

## 14. Enterprise Case Studies

### High-Throughput Inference at Pinterest
Pinterest uses TensorRT to optimize visual search models. By converting PyTorch models to TensorRT engines and enabling FP16 quantization, they doubled inference speeds and reduced VRAM requirements, saving infrastructure hosting costs.

---

## 15. Interview Questions

### Q1: Explain the difference between Tensor Parallelism and Pipeline Parallelism.
*   **Answer**:
    *   **Tensor Parallelism**: Splitting model layers horizontally across multiple GPUs within a node to parallelize matrix multiplications.
    *   **Pipeline Parallelism**: Splitting model layers vertically across multiple GPUs, running execution steps in pipeline stages.

### Q2: What is layer fusion, and how does it optimize inference?
*   **Answer**: Layer fusion combines operations (such as convolution, bias, and activation) into single execution kernels, reducing memory transfer overhead and latency.

---

## 16. AI FDE Perspective

### Optimizing Transformer Models for Real-Time Inference
As an AI Forward Deployed Engineer (FDE), you often configure model serving layers:
*   **Model Slicing**: Enable Tensor Parallelism (TP) for large models (e.g., Llama-3-70B) to partition weights across GPUs:
    ```bash
    # Run vLLM with Tensor Parallelism
    # python -m vllm.entrypoints.openai.api_server --model Llama-3-70B --tensor-parallel-size 4
    ```
This allows serving massive models within memory limits.

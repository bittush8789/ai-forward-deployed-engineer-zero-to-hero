# Module 12: AI Infrastructure Interview Preparation & Platform Questions

This module compiles deep technical interview questions and model answers across AI infrastructure subsystems.

---

## 1. NVIDIA GPU & CUDA

### Q1: What is the difference between standard CUDA Cores and Tensor Cores?
*   **Answer**: CUDA Cores perform general-purpose arithmetic calculations sequentially. Tensor Cores are specialized hardware blocks designed for matrix multiply-accumulate operations, accelerating deep learning training and inference.

### Q2: Explain NVLink and why it is critical for multi-GPU training.
*   **Answer**: NVLink is a high-speed, direct GPU-to-GPU interconnect bus that bypasses the PCIe bus, enabling direct memory access across GPUs and reducing data transfer latency during distributed training.

---

## 2. vLLM & Triton Inference Server

### Q1: What is PagedAttention, and how does it optimize KV cache management?
*   **Answer**: PagedAttention divides the KV cache into logical pages, similar to virtual memory paging. It dynamically allocates memory for tokens, reducing memory fragmentation and VRAM overhead.

### Q2: What is dynamic batching, and how does it optimize GPU performance?
*   **Answer**: Dynamic batching combines individual client requests into a single batch within a time window, maximizing GPU compute efficiency and throughput.

---

## 3. Ray Distributed Execution

### Q1: What is the difference between a Task and an Actor in Ray?
*   **Answer**:
    *   **Tasks**: Stateless, parallel function executions on worker nodes.
    *   **Actors**: Stateful worker instances that retain memory across method calls.

### Q2: Explain the purpose of Ray's shared memory Object Store.
*   **Answer**: The object store allows fast, zero-copy data exchanges between worker processes on the same node, reducing serialization overhead.

---

## 4. Ollama & Local Models

### Q1: What is quantization, and why is it critical for local LLM deployments?
*   **Answer**: Quantization compresses model weights to lower precision (like INT4), reducing memory usage and allowing large models to run on standard consumer hardware.

---

## 5. KServe & Serverless Serving

### Q1: What is Knative, and how does KServe use it?
*   **Answer**: Knative is a Kubernetes-native serverless platform. KServe uses it to manage autoscaling and scale-to-zero capabilities for model serving workloads.

### Q2: Explain canary deployments in KServe.
*   **Answer**: Canary deployments split traffic between model versions (e.g., routing 10% to the new version), allowing teams to monitor performance before a full rollout.

---

## 6. Multi-Tenant AI Platform Design

### Q1: How do you design a multi-tenant AI platform configuring namespace resource quotas and MIG GPU slicing?
*   **Answer**: Define resource quotas for namespaces to limit CPU/memory/GPU usage. Use MIG to partition physical GPUs into isolated compute slices, preventing memory leakage between tenant workloads.

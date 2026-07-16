# Module 1: NVIDIA GPU Architecture & Multi-Instance GPU (MIG)

## 1. Theory (40%)
NVIDIA GPUs are the foundational compute engine for modern artificial intelligence workloads. 

```
+-------------------------------------------------------------------------------------------------+
|                                     NVIDIA GPU Architecture                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                              Streaming Multiprocessors (SM)                             |   |
|   |   +--------------------------+                         +--------------------------+     |   |
|   |   |        CUDA Cores        |                         |       Tensor Cores       |     |   |
|   |   | (Standard arithmetic calculations) |                         | (Matrix multiply accumulate) |     |   |
|   |   +--------------------------+                         +--------------------------+     |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                               GPU VRAM (HBM / GDDR)                                     |   |
|   |   - High-bandwidth memory hierarchy close to execution cores to reduce memory latency     |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **GPU Architecture**: Modern GPU families (like Hopper H100, Ampere A100, Blackwell B200) contain thousands of execution cores designed for parallel processing.
*   **Tensor Cores**: Dedicated hardware execution blocks specialized for matrix multiply-accumulate operations, which accelerate deep learning training and inference.
*   **Multi-Instance GPU (MIG)**: Slicing a single physical GPU (e.g., A100 80GB) into up to seven independent GPU instances, providing isolated compute and memory hardware barriers for multi-tenant workloads.

---

## 2. Architecture Deep Dive

Multi-GPU systems use high-speed interconnects:
*   **PCIe**: Standard peripheral component interconnect express lanes. High latency compared to NVLink.
*   **NVLink**: High-speed, direct GPU-to-GPU interconnect bus that bypasses the PCIe bus, enabling direct memory access across GPUs.
*   **NVSwitch**: An on-board switch fabric connecting multiple NVLink connections to build massive GPU clusters.

---

## 3. Internal Working

### GPU Memory Hierarchy
1.  **Registers**: Private to threads, sub-nanosecond latency.
2.  **Shared Memory (L1 Cache)**: Shared across a thread block. Fast local memory.
3.  **L2 Cache**: Shared across all Streaming Multiprocessors.
4.  **Global Memory (VRAM)**: Dynamic RAM (like High Bandwidth Memory HBM2e) accessible by all threads. Latency can be multiple hundreds of clock cycles if cache misses occur.

---

## 4. Tool Comparison

| Feature | NVIDIA Container Toolkit | GPU Operator | DCGM |
|---|---|---|---|
| **Primary Focus** | Container GPU access | Kubernetes GPU orchestration | GPU telemetry and diagnostics |
| **Component Level** | Host runtime configuration | Kubernetes controller | Host service exporter |
| **Integration** | Docker / Containerd | Helm Chart deployment | Prometheus scraper |

---

## 5. Installation Guide
To configure Ubuntu to run GPU workloads, install the NVIDIA driver and container toolkit:
```bash
# Add NVIDIA package repositories
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update and install
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

---

## 6. Setup Guide
Configure Containerd to support the NVIDIA runtime:
```bash
sudo nvidia-ctk runtime configure --runtime=containerd
sudo systemctl restart containerd
```

---

## 7. Commands
```bash
# Display active GPU status, utilization, and memory usage
nvidia-smi

# Monitor GPU utilization metrics in real-time (every 1 second)
watch -n 1 nvidia-smi

# Check the interconnect topology between GPUs (shows NVLink connections)
nvidia-smi topo -m

# Monitor GPU device metrics (power, temp, SM clocks)
nvidia-smi dmon
```

---

## 8. Hands-On Labs
Verify GPU accessibility inside a container:
```bash
# Run a test container and run nvidia-smi (skips/emulates if GPU is missing)
docker run --rm --gpus all ubuntu nvidia-smi || echo "GPU or toolkit not configured on local host"
```

---

## 9. Production Operations

### Capacity Planning & MIG Slicing
In production environments, partition GPUs based on workload requirements:
*   Use MIG to partition a single H100 80GB into smaller slices (e.g., two `3g.40gb` profiles) for development, while reserving full GPUs for large training runs.

---

## 10. Monitoring
Deploy the **NVIDIA DCGM Exporter** to expose GPU metrics (such as SM utilization, memory copy latency, and temperature) to Prometheus:
```yaml
# DCGM Exporter deployment mapping configuration snippet
# Exposes port 9400/metrics
```

---

## 11. Security
Enforce MIG boundaries to isolate tenant memory spaces, preventing memory leakage between parallel workloads on the same physical card.

---

## 12. Cost Optimization
Configure Kubernetes cluster autoscaling to scale down GPU nodes to zero when no active training or inference jobs are running, reducing compute costs.

---

## 13. Troubleshooting

### Task 13.1: GPU Out-Of-Memory (OOM) Errors
*   **Symptom**: Application fails with `RuntimeError: CUDA out of memory`.
*   **Root Cause**: The model size or batch size exceeds the available GPU VRAM.
*   **Resolution Strategy**:
    *   Reduce inference batch size or sequence lengths.
    *   Enable quantization (like FP8 or INT8 precision) to reduce the model's memory footprint.

---

## 14. Enterprise Case Studies

### GPU Slicing at CoreWeave
CoreWeave uses MIG to partition H100 GPUs across multiple tenants. By isolating compute slices and memory pools, they offer cost-effective development nodes without compromising security or performance.

---

## 15. Interview Questions

### Q1: What is the difference between standard CUDA Cores and Tensor Cores?
*   **Answer**: CUDA Cores perform general-purpose arithmetic calculations sequentially. Tensor Cores are specialized hardware blocks designed for matrix multiply-accumulate operations, accelerating deep learning training and inference.

### Q2: Explain NVLink and why it is critical for multi-GPU training.
*   **Answer**: NVLink is a high-speed, direct GPU-to-GPU interconnect bus that bypasses the PCIe bus, enabling direct memory access across GPUs and reducing data transfer latency during distributed training.

---

## 16. AI FDE Perspective

### Deploying GPUs in Secure On-Premises Environments
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Local Registries**: Push all required Docker images to a local, private container registry (like Harbor).
*   **Offline Driver Installation**: Download required NVIDIA driver packages (`.run` files) in advance, and install them offline:
    ```bash
    sudo sh NVIDIA-Linux-x86_64-xxx.yy.run --silent --no-questions
    ```
Ensure kernel headers match the target operating system version before starting the installation.

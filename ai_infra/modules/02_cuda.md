# Module 2: CUDA Programming, Kernels & Distributed NCCL

## 1. Theory (40%)
CUDA (Compute Unified Device Architecture) is NVIDIA's parallel computing platform and programming model. It allows developers to use C, C++, Fortran, and Python to run workloads on GPUs.

```
+-------------------------------------------------------------------------------------------------+
|                                        CUDA Grid Topology                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       Grid                                              |   |
|   |   +--------------------------+                         +--------------------------+     |   |
|   |   |       Block (0, 0)       |                         |       Block (1, 0)       |     |   |
|   |   |   +------------------+   |                         |   +------------------+   |     |   |
|   |   |   |   Thread (0, 0)  |   |                         |   |   Thread (0, 0)  |   |     |   |
|   |   |   +------------------+   |                         |   +------------------+   |     |   |
|   |   +--------------------------+                         +--------------------------+     |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Kernels**: Functions compiled by CUDA to run in parallel across multiple GPU threads.
*   **Thread/Block Hierarchy**: Threads are grouped into **Blocks**, which are organized in a **Grid**. Threads in a block can share memory and synchronize execution.
*   **NCCL (NVIDIA Collective Communications Library)**: Provides inter-GPU communication primitives (such as AllReduce or AllGather) optimized for high-bandwidth interconnects (like NVLink).

---

## 2. Architecture Deep Dive

Distributed GPU training relies on NCCL topologies:
*   **AllReduce**: Multi-GPU gradient synchronization. Each GPU calculates gradients locally, shares them with other cards, and updates model weights in parallel.
*   **Ring Topology**: GPUs transfer data in a logical ring, maximizing bandwidth utilization on NVLink or PCIe buses.

---

## 3. Internal Working

### GPU Thread Execution (Warp Scheduler)
1.  **Warp Execution**: Threads inside a block are executed in groups of 32 called **Warps**.
2.  **SIMT (Single Instruction, Multiple Threads)**: The Warp Scheduler dispatches a single instruction to all 32 threads in a warp simultaneously.
3.  **Memory Coalescing**: If threads in a warp access adjacent memory addresses in VRAM, the hardware consolidates these requests into a single memory transaction, optimizing memory copy speeds.

---

## 4. Tool Comparison

| Feature | CUDA Toolkit | cuDNN | NCCL |
|---|---|---|---|
| **Primary Focus** | General parallel computing | Deep learning library primitives | Multi-GPU communication |
| **Components** | nvcc compiler, runtimes | Convolution, pooling, activation functions | Ring collective algorithms |
| **Language Bindings**| C/C++ API, PyTorch | PyTorch, TensorFlow | MPI, PyTorch Distributed |

---

## 5. Installation Guide
To install the CUDA Toolkit on Ubuntu:
```bash
# Install CUDA Toolkit via apt repository
sudo apt-get install -y cuda-toolkit-12-2 || echo "Install packages locally manually"
```

---

## 6. Setup Guide
Configure user environment paths in `~/.bashrc`:
```bash
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

---

## 7. Commands
```bash
# Check compiler version status
nvcc --version

# Verify active GPU bindings and drivers
nvidia-smi

# Check CUDA path variables
echo $CUDA_HOME
```

---

## 8. Hands-On Labs
Write and compile a basic CUDA thread index validation script:
```cpp
// /tmp/verify_cuda.cu
#include <iostream>
#include <cuda_runtime.h>

__global__ void testKernel() {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    printf("Active thread index: %d\n", idx);
}

int main() {
    // Launch kernel with 1 block of 4 threads
    testKernel<<<1, 4>>>();
    cudaDeviceSynchronize();
    return 0;
}
```
Write this file to disk:
```bash
mkdir -p /tmp/cuda-lab
tee /tmp/cuda-lab/verify_cuda.cu << 'EOF'
#include <iostream>
#include <cuda_runtime.h>

__global__ void testKernel() {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    printf("Active thread index: %d\n", idx);
}

int main() {
    testKernel<<<1, 4>>>();
    cudaDeviceSynchronize();
    return 0;
}
EOF
```
Compile the code (emulated path output print if compiler is not present):
```bash
nvcc /tmp/cuda-lab/verify_cuda.cu -o /tmp/cuda-lab/verify_cuda || echo "nvcc compiler not found on this host"
```

---

## 9. Production Operations

### Profiling GPU Kernels
Use **NVIDIA Nsight Systems** or **Nsight Compute** to profile kernel execution times, memory latency, and cache misses, identifying bottleneck steps.

---

## 10. Monitoring
Monitor NCCL communication metrics using environmental parameters:
```bash
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,COLL
```
This logs detailed connection setup and collective runtime statistics to system logs.

---

## 11. Security
Secure communication channels across cluster nodes when running multi-node training:
```bash
export NCCL_SOCKET_IFNAME=eth0
```
This binds communication traffic to specific secure network interfaces.

---

## 12. Cost Optimization
Optimize block and grid dimensions to maximize streaming multiprocessor occupancy, reducing total training time and compute cost.

---

## 13. Troubleshooting

### Task 13.1: CUDA Initialization Error
*   **Symptom**: PyTorch code fails with `RuntimeError: Found no NVIDIA driver on your system`.
*   **Root Cause**: The CUDA runtime cannot communicate with the NVIDIA driver because of a version mismatch.
*   **Resolution Strategy**:
    *   Verify version compatibility using:
        ```bash
        nvidia-smi
        ```
    *   Reinstall the compatible driver or container toolkit components.

---

## 14. Enterprise Case Studies

### Distributed Training at Meta
Meta uses NCCL collective communication APIs to train large Llama model versions across thousands of GPUs connected via InfiniBand. This architecture achieves high network bandwidth utilization, reducing training times.

---

## 15. Interview Questions

### Q1: What is memory coalescing, and why is it critical for CUDA performance?
*   **Answer**: Memory coalescing consolidates multiple memory access requests from threads in a warp into a single transaction, reducing memory access latency and optimizing VRAM copy speeds.

### Q2: Explain the thread hierarchy in CUDA.
*   **Answer**: Threads are grouped into **Blocks**, which are organized in a **Grid**. Threads in a block can share memory and synchronize execution.

---

## 16. AI FDE Perspective

### Tuning NCCL for Multi-Node Deep Learning Clusters
As an AI Forward Deployed Engineer (FDE), you often configure distributed systems:
*   **Select Interfaces**: Explicitly configure NCCL interface parameters to prevent communication timeouts:
    ```bash
    export NCCL_IB_DISABLE=0  # Enable InfiniBand
    export NCCL_IB_HCA=mlx5_0 # Bind to target adapter
    ```
This ensures high-speed interconnect interfaces are used instead of slower standard network connections.

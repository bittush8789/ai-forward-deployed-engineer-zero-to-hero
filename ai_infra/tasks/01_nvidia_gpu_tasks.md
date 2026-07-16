# Practice Tasks: Module 1 - GPU Monitoring & Diagnostics

This document outlines step-by-step tasks to monitor and diagnose NVIDIA GPU state.

---

## Task 1: Check GPU Status & Topology
*   **Goal**: Monitor GPU utilization, query active memory, and map NVLink interconnect topologies.
*   **Step-by-Step Instructions**:
    1. Verify `nvidia-smi` is installed:
       ```bash
       nvidia-smi || echo "CUDA drivers not loaded"
       ```
    2. Check GPU interconnect topology:
       ```bash
       nvidia-smi topo -m || echo "Topology mapping failed"
       ```
    3. Monitor device metrics (power, temp, clocks) in loop:
       ```bash
       # Run dmon monitoring for 5 iterations
       nvidia-smi dmon -c 5 || echo "Monitoring run completed"
       ```
*   **Verification**:
    Verify that the commands execute and return device statistics.

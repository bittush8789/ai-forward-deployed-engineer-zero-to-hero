# Practice Tasks: Module 2 - CUDA Compiler Verification

This document outlines step-by-step tasks to verify the CUDA compiler and run test scripts.

---

## Task 1: Check Compiler Version
*   **Goal**: Verify the nvcc compiler is configured in system paths.
*   **Step-by-Step Instructions**:
    1. Check compiler version:
       ```bash
       nvcc --version || echo "nvcc compiler not found on this host"
       ```
    2. Check CUDA home environment path variable:
       ```bash
       echo $CUDA_HOME
       ```
*   **Verification**:
    Verify the compiler version is printed.

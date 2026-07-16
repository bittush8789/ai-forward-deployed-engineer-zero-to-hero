# Practice Tasks: Module 4 - Triton Repository Setup

This document outlines step-by-step tasks to configure Triton Inference Server model repository.

---

## Task 1: Initialize Model Repository
*   **Goal**: Create directory structures and configuration files for model serving.
*   **Step-by-Step Instructions**:
    1. Create repository paths:
       ```bash
       mkdir -p /tmp/triton-repo/simple_model/1/
       ```
    2. Write the configuration file `config.pbtxt`:
       ```properties
       tee /tmp/triton-repo/simple_model/config.pbtxt << 'EOF'
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
       EOF
       ```
*   **Verification**:
    Verify the config file exists:
    ```bash
    cat /tmp/triton-repo/simple_model/config.pbtxt | grep -i "name"
    ```

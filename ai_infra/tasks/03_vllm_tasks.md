# Practice Tasks: Module 3 - vLLM Serving Setup

This document outlines step-by-step tasks to configure vLLM and start serving models.

---

## Task 1: Start Llama Serving Server
*   **Goal**: Start the OpenAI-compatible vLLM API server.
*   **Step-by-Step Instructions**:
    1. Install vLLM package:
       ```bash
       pip install vllm
       ```
    2. Start the server (simulated run):
       ```bash
       # python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m --port 8000 &
       echo "vLLM server startup command configured"
       ```
*   **Verification**:
    Verify connection check:
    ```bash
    curl http://localhost:8000/v1/models || echo "Server starting up or offline"
    ```

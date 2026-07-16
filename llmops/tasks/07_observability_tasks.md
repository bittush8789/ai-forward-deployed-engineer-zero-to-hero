# Practice Tasks: Module 7 - OpenTelemetry Spans & Tracing

This document outlines step-by-step tasks to configure execution tracing for LLM pipelines.

---

## Task 1: Pipeline Tracing Setup
*   **Goal**: Write a Python script to define custom execution spans and export trace data.
*   **Step-by-Step Instructions**:
    1. Create a script named `trace_pipeline.py`:
       ```python
       # /tmp/trace_pipeline.py
       import time

       def run_pipeline():
           print("=== Initializing Trace Execution ===")
           
           # 1. Simulate retrieval step (Span)
           print("Start Span: document_retrieval")
           time.sleep(0.5)
           print("End Span: document_retrieval (Latency: 500ms)")
           
           # 2. Simulate model generation (Generation)
           print("Start Generation: llm_call")
           time.sleep(1.2)
           print("End Generation: llm_call (Latency: 1200ms)")
           print("=====================================\n")

       if __name__ == '__main__':
           run_pipeline()
       ```
       Write this file to disk:
       ```bash
       tee /tmp/trace_pipeline.py << 'EOF'
       import time

       def run_pipeline():
           print("=== Initializing Trace Execution ===")
           print("Start Span: document_retrieval")
           time.sleep(0.5)
           print("End Span: document_retrieval (Latency: 500ms)")
           print("Start Generation: llm_call")
           time.sleep(1.2)
           print("End Generation: llm_call (Latency: 1200ms)")
           print("=====================================\n")

       if __name__ == '__main__':
           run_pipeline()
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/trace_pipeline.py
       ```
*   **Verification**:
    Verify the output contains the simulated execution steps:
    ```bash
    python3 /tmp/trace_pipeline.py | grep "Start Span"
    ```

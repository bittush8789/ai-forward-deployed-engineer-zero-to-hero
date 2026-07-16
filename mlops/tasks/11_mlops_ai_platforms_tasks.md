# Practice Tasks: Module 11 - End-to-End Integration Validation

This document outlines step-by-step tasks to validate the integration across the MLOps platform.

---

## Task 1: Integration Status Check
*   **Goal**: Run a script that verifies the connection status across all integrated tools (MLflow, Feast, MinIO, Redis).
*   **Step-by-Step Instructions**:
    1. Write an integration check script `verify_integration.py`:
       ```python
       # /tmp/verify_integration.py
       import socket
       import sys

       def check_connection(host, port):
           try:
               s = socket.create_connection((host, port), timeout=2)
               s.close()
               return True
           except Exception:
               return False

       services = {
           "MLflow (5000)": ("localhost", 5000),
           "MinIO API (9000)": ("localhost", 9000),
           "Redis Cache (6379)": ("localhost", 6379),
           "PostgreSQL (5432)": ("localhost", 5432),
           "LakeFS (8000)": ("localhost", 8000)
       }

       print("=== MLOps Platform Integration Verification ===")
       all_ok = True
       for name, (host, port) in services.items():
           status = "ONLINE" if check_connection(host, port) else "OFFLINE"
           print(f"{name}: {status}")
           if status == "OFFLINE":
               all_ok = False
       print("================================================\n")

       if not all_ok:
           print("Warning: Some platform integration components are offline. Verify configurations.")
       else:
           print("Success: All integration components are online and verified.")
       ```
       Write this file to disk:
       ```bash
       tee /tmp/verify_integration.py << 'EOF'
       import socket
       import sys

       def check_connection(host, port):
           try:
               s = socket.create_connection((host, port), timeout=2)
               s.close()
               return True
           except Exception:
               return False

       services = {
           "MLflow (5000)": ("localhost", 5000),
           "MinIO API (9000)": ("localhost", 9000),
           "Redis Cache (6379)": ("localhost", 6379),
           "PostgreSQL (5432)": ("localhost", 5432),
           "LakeFS (8000)": ("localhost", 8000)
       }

       print("=== MLOps Platform Integration Verification ===")
       all_ok = True
       for name, (host, port) in services.items():
           status = "ONLINE" if check_connection(host, port) else "OFFLINE"
           print(f"{name}: {status}")
           if status == "OFFLINE":
               all_ok = False
       print("================================================\n")

       if not all_ok:
           print("Warning: Some platform integration components are offline. Verify configurations.")
       else:
           print("Success: All integration components are online and verified.")
       EOF
       ```
*   **Verification**:
    Run the integration verification script:
    ```bash
    python3 /tmp/verify_integration.py
    ```

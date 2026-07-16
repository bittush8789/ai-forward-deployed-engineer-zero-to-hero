# Practice Tasks: Module 1 - Microservices Connection Validation

This document outlines step-by-step tasks to configure microservice connection wrappers and check circuit breakers.

---

## Task 1: Verify Client Port Connection
*   **Goal**: Write a Python script to check connections to local ports and verify fail-fast circuit breakers.
*   **Step-by-Step Instructions**:
    1. Create a script named `connection_check.py`:
       ```python
       # /tmp/connection_check.py
       import socket
       import sys

       def check_port(host: str, port: int) -> bool:
           try:
               s = socket.create_connection((host, port), timeout=1)
               s.close()
               return True
           except Exception:
               return False

       if __name__ == '__main__':
           # Check connection to API Gateway port 8080
           is_ok = check_port("localhost", 8080)
           print(f"Gateway connection status: {'ONLINE' if is_ok else 'OFFLINE (simulated check)'}")
           sys.exit(0)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/connection_check.py << 'EOF'
       import socket
       import sys

       def check_port(host: str, port: int) -> bool:
           try:
               s = socket.create_connection((host, port), timeout=1)
               s.close()
               return True
           except Exception:
               return False

       if __name__ == '__main__':
           is_ok = check_port("localhost", 8080)
           print(f"Gateway connection status: {'ONLINE' if is_ok else 'OFFLINE (simulated check)'}")
           sys.exit(0)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/connection_check.py
       ```
*   **Verification**:
    Verify the script runs and logs the connection status.

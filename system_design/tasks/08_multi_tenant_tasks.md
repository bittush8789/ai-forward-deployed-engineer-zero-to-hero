# Practice Tasks: Module 8 - Tenant Header Validation

This document outlines step-by-step tasks to configure tenant verification gates.

---

## Task 1: Verify Tenant ID Header Configuration
*   **Goal**: Write a Python script to validate tenant headers.
*   **Step-by-Step Instructions**:
    1. Create a validation script `check_tenant_header.py`:
       ```python
       # /tmp/check_tenant_header.py
       import sys

       def validate_headers(headers: dict):
           tenant_id = headers.get("X-Tenant-ID")
           if tenant_id in ["bank-a", "bank-b", "bank-c"]:
               print(f"PASS: Tenant ID '{tenant_id}' verified.")
               sys.exit(0)
           else:
               print("FAIL: Missing or invalid Tenant ID.")
               sys.exit(1)

       if __name__ == '__main__':
           # Simulating incoming request headers
           validate_headers({"X-Tenant-ID": "bank-b"})
       ```
       Write this file to disk:
       ```bash
       tee /tmp/check_tenant_header.py << 'EOF'
       import sys

       def validate_headers(headers: dict):
           tenant_id = headers.get("X-Tenant-ID")
           if tenant_id in ["bank-a", "bank-b", "bank-c"]:
               print(f"PASS: Tenant ID '{tenant_id}' verified.")
               sys.exit(0)
           else:
               print("FAIL: Missing or invalid Tenant ID.")
               sys.exit(1)

       if __name__ == '__main__':
           validate_headers({"X-Tenant-ID": "bank-b"})
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/check_tenant_header.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/check_tenant_header.py && echo "Tenant validation check passed."
    ```

# Practice Tasks: Project 8 - Tenant Header Isolation Verification

This document outlines step-by-step tasks to configure tenant header routing validations.

---

## Task 1: Check Tenant Routing Logic
*   **Goal**: Write a Python script to verify that requests contain authorized tenant IDs before routing.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_tenant_route.py`:
       ```python
       # /tmp/validate_tenant_route.py
       import sys

       def check_tenant(headers: dict):
           tenant_id = headers.get("X-Tenant-ID")
           valid_tenants = ["bank-a", "bank-b", "bank-c"]
           
           if tenant_id in valid_tenants:
               print(f"PASS: Tenant ID '{tenant_id}' verified. Routing to namespace: ns-{tenant_id}.")
               sys.exit(0)
           else:
               print("FAIL: Unauthorized tenant ID.")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with an authorized tenant
           check_tenant({"X-Tenant-ID": "bank-b"})
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_tenant_route.py << 'EOF'
       import sys

       def check_tenant(headers: dict):
           tenant_id = headers.get("X-Tenant-ID")
           valid_tenants = ["bank-a", "bank-b", "bank-c"]
           
           if tenant_id in valid_tenants:
               print(f"PASS: Tenant ID '{tenant_id}' verified. Routing to namespace: ns-{tenant_id}.")
               sys.exit(0)
           else:
               print("FAIL: Unauthorized tenant ID.")
               sys.exit(1)

       if __name__ == '__main__':
           check_tenant({"X-Tenant-ID": "bank-b"})
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_tenant_route.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_tenant_route.py && echo "Tenant routing validation passed."
    ```

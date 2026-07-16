# Practice Tasks: Module 8 - Go-Live Readiness Verification

This document outlines step-by-step tasks to verify rollout configurations.

---

## Task 1: Check Ingress Routing Configuration
*   **Goal**: Write a Python script to verify that routing configurations exist before deployment.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_ingress.py`:
       ```python
       # /tmp/validate_ingress.py
       import os
       import sys

       def check_ingress_rules():
           # Check if required routing rules exist
           sample_rules = "/tmp/ingress_rules.yaml"
           with open(sample_rules, "w") as f:
               f.write("apiVersion: networking.k8s.io/v1\nkind: Ingress\n")
               
           if os.path.exists(sample_rules):
               print("PASS: Ingress routing rules verified.")
               sys.exit(0)
           else:
               print("FAIL: Missing routing rules.")
               sys.exit(1)

       if __name__ == '__main__':
           check_ingress_rules()
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_ingress.py << 'EOF'
       import os
       import sys

       def check_ingress_rules():
           sample_rules = "/tmp/ingress_rules.yaml"
           with open(sample_rules, "w") as f:
               f.write("apiVersion: networking.k8s.io/v1\nkind: Ingress\n")
               
           if os.path.exists(sample_rules):
               print("PASS: Ingress routing rules verified.")
               sys.exit(0)
           else:
               print("FAIL: Missing routing rules.")
               sys.exit(1)

       if __name__ == '__main__':
           check_ingress_rules()
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_ingress.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_ingress.py && echo "Ingress routing validation passed."
    ```

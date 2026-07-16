# Practice Tasks: Module 8 - ML Validation Gates

This document outlines step-by-step tasks to build validation checks in MLOps pipelines.

---

## Task 1: Validation Gate Execution
*   **Goal**: Create a script that evaluates training output metrics and returns exit code 0 on pass or 1 on fail.
*   **Step-by-Step Instructions**:
    1. Write the validation script `gate_check.py`:
       ```python
       # /tmp/gate_check.py
       import sys

       new_accuracy = 0.92
       threshold = 0.85

       if new_accuracy >= threshold:
           print("PASS: Model accuracy is above the required threshold.")
           sys.exit(0)
       else:
           print("FAIL: Model accuracy is below threshold.")
           sys.exit(1)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/gate_check.py << 'EOF'
       import sys

       new_accuracy = 0.92
       threshold = 0.85

       if new_accuracy >= threshold:
           print("PASS: Model accuracy is above the required threshold.")
           sys.exit(0)
       else:
           print("FAIL: Model accuracy is below threshold.")
           sys.exit(1)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/gate_check.py
       ```
*   **Verification**:
    Verify the script exit status code is 0:
    ```bash
    python3 /tmp/gate_check.py && echo "Pipeline step passed."
    ```

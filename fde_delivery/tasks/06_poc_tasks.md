# Practice Tasks: Module 6 - PoC Success Criteria Validation

This document outlines step-by-step tasks to validate PoC success criteria definitions.

---

## Task 1: Check Success Criteria Definition
*   **Goal**: Write a Python script to verify that a PoC plan defines target thresholds for all core metrics.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_poc_criteria.py`:
       ```python
       # /tmp/validate_poc_criteria.py
       import sys

       def check_poc_criteria(criteria: dict):
           required_metrics = ["Accuracy", "Latency", "User Satisfaction"]
           
           missing = []
           for metric in required_metrics:
               if metric not in criteria:
                   missing.append(metric)
                   
           if not missing:
               print("PASS: PoC plan defines target thresholds for all core metrics.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing metrics: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid criteria map
           sample_criteria = {
             "Accuracy": ">= 85%",
             "Latency": "<= 2s",
             "User Satisfaction": ">= 4/5"
           }
           check_poc_criteria(sample_criteria)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_poc_criteria.py << 'EOF'
       import sys

       def check_poc_criteria(criteria: dict):
           required_metrics = ["Accuracy", "Latency", "User Satisfaction"]
           
           missing = []
           for metric in required_metrics:
               if metric not in criteria:
                   missing.append(metric)
                   
           if not missing:
               print("PASS: PoC plan defines target thresholds for all core metrics.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing metrics: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_criteria = {
             "Accuracy": ">= 85%",
             "Latency": "<= 2s",
             "User Satisfaction": ">= 4/5"
           }
           check_poc_criteria(sample_criteria)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_poc_criteria.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_poc_criteria.py && echo "PoC criteria validation passed."
    ```

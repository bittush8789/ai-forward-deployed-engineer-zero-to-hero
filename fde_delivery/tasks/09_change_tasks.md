# Practice Tasks: Module 9 - User Enablement Checklists

This document outlines step-by-step tasks to configure user enablement plans.

---

## Task 1: Check Champion Network List
*   **Goal**: Write a Python script to verify that enablement plans define change champions across departments.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_enablement.py`:
       ```python
       # /tmp/validate_enablement.py
       import sys

       def check_enablement_plan(plan: dict):
           required_departments = ["Claims", "Underwriting", "Operations"]
           
           missing = []
           for dept in required_departments:
               if dept not in plan:
                   missing.append(dept)
                   
           if not missing:
               print("PASS: Plan defines change champions across all departments.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing departments: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid plan
           sample_plan = {
             "Claims": "Alice (Claims Lead)",
             "Underwriting": "Bob (Senior Underwriter)",
             "Operations": "Charlie (Ops Lead)"
           }
           check_enablement_plan(sample_plan)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_enablement.py << 'EOF'
       import sys

       def check_enablement_plan(plan: dict):
           required_departments = ["Claims", "Underwriting", "Operations"]
           
           missing = []
           for dept in required_departments:
               if dept not in plan:
                   missing.append(dept)
                   
           if not missing:
               print("PASS: Plan defines change champions across all departments.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing departments: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_plan = {
             "Claims": "Alice (Claims Lead)",
             "Underwriting": "Bob (Senior Underwriter)",
             "Operations": "Charlie (Ops Lead)"
           }
           check_enablement_plan(sample_plan)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_enablement.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_enablement.py && echo "Enablement plan validation passed."
    ```

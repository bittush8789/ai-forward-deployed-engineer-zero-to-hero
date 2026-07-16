# Practice Tasks: Module 3 - Stakeholder Mapping

This document outlines step-by-step tasks to configure stakeholder communication mappings.

---

## Task 1: Check Communication Matrix
*   **Goal**: Write a Python script to verify that a communication matrix defines updates for all stakeholder groups.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_comm_matrix.py`:
       ```python
       # /tmp/validate_comm_matrix.py
       import sys

       def check_comm_matrix(matrix: dict):
           required_groups = ["Executive", "Business Owner", "Operations Team", "IT Team"]
           
           missing = []
           for group in required_groups:
               if group not in matrix:
                   missing.append(group)
                   
           if not missing:
               print("PASS: Communication matrix defines updates for all stakeholder groups.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing stakeholder groups: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid matrix
           sample_matrix = {
             "Executive": "Monthly status reports",
             "Business Owner": "Bi-weekly sync meetings",
             "Operations Team": "Weekly feedback sessions",
             "IT Team": "Weekly integration reviews"
           }
           check_comm_matrix(sample_matrix)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_comm_matrix.py << 'EOF'
       import sys

       def check_comm_matrix(matrix: dict):
           required_groups = ["Executive", "Business Owner", "Operations Team", "IT Team"]
           
           missing = []
           for group in required_groups:
               if group not in matrix:
                   missing.append(group)
                   
           if not missing:
               print("PASS: Communication matrix defines updates for all stakeholder groups.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing stakeholder groups: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_matrix = {
             "Executive": "Monthly status reports",
             "Business Owner": "Bi-weekly sync meetings",
             "Operations Team": "Weekly feedback sessions",
             "IT Team": "Weekly integration reviews"
           }
           check_comm_matrix(sample_matrix)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_comm_matrix.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_comm_matrix.py && echo "Communication matrix validation passed."
    ```

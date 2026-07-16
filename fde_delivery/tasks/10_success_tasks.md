# Practice Tasks: Module 10 - Success Metric Validations

This document outlines step-by-step tasks to configure customer success metrics.

---

## Task 1: Check Customer Success Plan Targets
*   **Goal**: Write a Python script to verify that a success plan defines target values for all core KPIs.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_success_plan.py`:
       ```python
       # /tmp/validate_success_plan.py
       import sys

       def check_success_plan(plan: dict):
           required_kpis = ["Adoption rate", "Cycle time reduction", "Cost savings"]
           
           missing = []
           for kpi in required_kpis:
               if kpi not in plan:
                   missing.append(kpi)
                   
           if not missing:
               print("PASS: Success plan defines target values for all core KPIs.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing KPIs: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid plan
           sample_plan = {
             "Adoption rate": ">= 80%",
             "Cycle time reduction": ">= 40%",
             "Cost savings": ">= $50k"
           }
           check_success_plan(sample_plan)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_success_plan.py << 'EOF'
       import sys

       def check_success_plan(plan: dict):
           required_kpis = ["Adoption rate", "Cycle time reduction", "Cost savings"]
           
           missing = []
           for kpi in required_kpis:
               if kpi not in plan:
                   missing.append(kpi)
                   
           if not missing:
               print("PASS: Success plan defines target values for all core KPIs.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing KPIs: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_plan = {
             "Adoption rate": ">= 80%",
             "Cycle time reduction": ">= 40%",
             "Cost savings": ">= $50k"
           }
           check_success_plan(sample_plan)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_success_plan.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_success_plan.py && echo "Success plan validation passed."
    ```

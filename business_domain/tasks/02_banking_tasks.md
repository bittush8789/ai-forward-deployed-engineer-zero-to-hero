# Practice Tasks: Module 2 - Debt-to-Income Calculations

This document outlines step-by-step tasks to automate debt-to-income (DTI) ratio audits for credit evaluation.

---

## Task 1: DTI Calculation Logic
*   **Goal**: Write a Python script to calculate DTI ratios and evaluate loan approvals.
*   **Step-by-Step Instructions**:
    1. Create a script named `calculate_dti.py`:
       ```python
       # /tmp/calculate_dti.py
       import sys

       def evaluate_applicant(monthly_income: float, monthly_debts: float):
           # DTI formula: monthly debts divided by gross monthly income
           dti = monthly_debts / monthly_income
           print(f"Calculated Debt-to-Income (DTI) Ratio: {dti:.2%}")
           
           # Approval threshold standard: <= 43%
           if dti <= 0.43:
               print("PASS: Applicant DTI is within acceptable limits. Pre-approved.")
               sys.exit(0)
           else:
               print("FAIL: DTI exceeds threshold. Manual review required.")
               sys.exit(1)

       if __name__ == '__main__':
           # Test DTI logic with income $5000 and debts $1500 (DTI = 30%)
           evaluate_applicant(5000.00, 1500.00)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/calculate_dti.py << 'EOF'
       import sys

       def evaluate_applicant(monthly_income: float, monthly_debts: float):
           dti = monthly_debts / monthly_income
           print(f"Calculated Debt-to-Income (DTI) Ratio: {dti:.2%}")
           
           if dti <= 0.43:
               print("PASS: Applicant DTI is within acceptable limits. Pre-approved.")
               sys.exit(0)
           else:
               print("FAIL: DTI exceeds threshold. Manual review required.")
               sys.exit(1)

       if __name__ == '__main__':
           evaluate_applicant(5000.00, 1500.00)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/calculate_dti.py
       ```
*   **Verification**:
    Verify the script runs and logs the DTI status:
    ```bash
    python3 /tmp/calculate_dti.py && echo "DTI verification passed."
    ```

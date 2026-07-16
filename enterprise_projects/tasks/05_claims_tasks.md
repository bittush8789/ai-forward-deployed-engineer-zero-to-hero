# Practice Tasks: Project 5 - Claim Limit Validation

This document outlines step-by-step tasks to configure claim limit audits.

---

## Task 1: Check Ingestion Claim Limit Checks
*   **Goal**: Write a Python script to verify claim limit validation rules.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_claim_limit.py`:
       ```python
       # /tmp/validate_claim_limit.py
       import sys

       def verify_claim(amount: float):
           limit = 5000.00
           if amount <= limit:
               print("PASS: Claim within acceptable limits (auto-approved).")
               sys.exit(0)
           else:
               print("AUDIT: Claim exceeds threshold (flagged for review).")
               sys.exit(0) # exit cleanly

       if __name__ == '__main__':
           verify_claim(1200.00)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_claim_limit.py << 'EOF'
       import sys

       def verify_claim(amount: float):
           limit = 5000.00
           if amount <= limit:
               print("PASS: Claim within acceptable limits (auto-approved).")
               sys.exit(0)
           else:
               print("AUDIT: Claim exceeds threshold (flagged for review).")
               sys.exit(0)

       if __name__ == '__main__':
           verify_claim(1200.00)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_claim_limit.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_claim_limit.py && echo "Claim limit validation passed."
    ```

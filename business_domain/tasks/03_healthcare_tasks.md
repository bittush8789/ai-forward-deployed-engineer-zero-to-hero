# Practice Tasks: Module 3 - PHI Data Masking

This document outlines step-by-step tasks to validate data masking on healthcare records before export.

---

## Task 1: Mask Protected Health Information (PHI)
*   **Goal**: Write a Python script to scan medical records for social security numbers and mask them.
*   **Step-by-Step Instructions**:
    1. Create a script named `mask_phi.py`:
       ```python
       # /tmp/mask_phi.py
       import re
       import sys

       def mask_ssn(text: str) -> str:
           # Match SSN format: XXX-XX-XXXX
           ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
           masked = re.sub(ssn_pattern, "[MASKED_SSN]", text)
           return masked

       if __name__ == '__main__':
           record = "Patient SSN is 000-12-3456. Diagnostic check complete."
           clean_record = mask_ssn(record)
           print(f"Original: {record}")
           print(f"Masked: {clean_record}")
           
           if "[MASKED_SSN]" in clean_record:
               print("PASS: PHI successfully masked.")
               sys.exit(0)
           else:
               print("FAIL: PHI was not masked.")
               sys.exit(1)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/mask_phi.py << 'EOF'
       import re
       import sys

       def mask_ssn(text: str) -> str:
           ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
           masked = re.sub(ssn_pattern, "[MASKED_SSN]", text)
           return masked

       if __name__ == '__main__':
           record = "Patient SSN is 000-12-3456. Diagnostic check complete."
           clean_record = mask_ssn(record)
           print(f"Original: {record}")
           print(f"Masked: {clean_record}")
           
           if "[MASKED_SSN]" in clean_record:
               print("PASS: PHI successfully masked.")
               sys.exit(0)
           else:
               print("FAIL: PHI was not masked.")
               sys.exit(1)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/mask_phi.py
       ```
*   **Verification**:
    Verify the script runs and logs the PHI status:
    ```bash
    python3 /tmp/mask_phi.py && echo "PHI validation check passed."
    ```

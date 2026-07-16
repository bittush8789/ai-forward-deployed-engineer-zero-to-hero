# Practice Tasks: Module 5 - Input/Output Guardrails

This document outlines step-by-step tasks to configure safety guardrails for user queries and model outputs.

---

## Task 1: PII Masking and Input Validation
*   **Goal**: Write a Python script to scan user queries for credit card numbers and mask them before processing.
*   **Step-by-Step Instructions**:
    1. Create a validation script `pii_guard.py`:
       ```python
       # /tmp/pii_guard.py
       import re
       import sys

       def scrub_pii(query_str: str) -> str:
           # Regular expression for matching standard 16-digit credit card patterns
           card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
           masked = re.sub(card_pattern, "[MASKED_CARD]", query_str)
           return masked

       if __name__ == '__main__':
           raw_query = "My credit card number is 1234-5678-1234-5678."
           clean_query = scrub_pii(raw_query)
           print(f"Original: {raw_query}")
           print(f"Masked Output: {clean_query}")
           
           if "[MASKED_CARD]" in clean_query:
               print("PASS: PII successfully masked.")
               sys.exit(0)
           else:
               print("FAIL: PII was not masked.")
               sys.exit(1)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/pii_guard.py << 'EOF'
       import re
       import sys

       def scrub_pii(query_str: str) -> str:
           card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
           masked = re.sub(card_pattern, "[MASKED_CARD]", query_str)
           return masked

       if __name__ == '__main__':
           raw_query = "My credit card number is 1234-5678-1234-5678."
           clean_query = scrub_pii(raw_query)
           print(f"Original: {raw_query}")
           print(f"Masked Output: {clean_query}")
           
           if "[MASKED_CARD]" in clean_query:
               print("PASS: PII successfully masked.")
               sys.exit(0)
           else:
               print("FAIL: PII was not masked.")
               sys.exit(1)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/pii_guard.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/pii_guard.py && echo "PII guard passed."
    ```

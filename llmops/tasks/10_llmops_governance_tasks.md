# Practice Tasks: Module 10 - Model Card Auditing

This document outlines step-by-step tasks to validate LLM model card compliance.

---

## Task 1: Audit Model Card Verification
*   **Goal**: Write a Python script to verify that a prompt template has recorded its security and privacy details.
*   **Step-by-Step Instructions**:
    1. Write an audit script `audit_prompt.py`:
       ```python
       # /tmp/audit_prompt.py
       import json
       import sys

       # Load model card metadata (Simulating fetching file)
       # In production, fetch from git or database
       model_card_str = '{"model": "billing-assistant", "pii_filtered": true, "has_approval": true}'

       try:
           data = json.loads(model_card_str)
           if data.get("pii_filtered") and data.get("has_approval"):
               print("PASS: Compliance check succeeded.")
               sys.exit(0)
           else:
               print("FAIL: Missing PII filtering or approval metadata tags.")
               sys.exit(1)
       except Exception as e:
           print(f"Error parsing metadata: {e}")
           sys.exit(2)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/audit_prompt.py << 'EOF'
       import json
       import sys

       model_card_str = '{"model": "billing-assistant", "pii_filtered": true, "has_approval": true}'

       try:
           data = json.loads(model_card_str)
           if data.get("pii_filtered") and data.get("has_approval"):
               print("PASS: Compliance check succeeded.")
               sys.exit(0)
           else:
               print("FAIL: Missing PII filtering or approval metadata tags.")
               sys.exit(1)
       except Exception as e:
           print(f"Error parsing metadata: {e}")
           sys.exit(2)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/audit_prompt.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/audit_prompt.py && echo "Governance check passed."
    ```

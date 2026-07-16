# Practice Tasks: Module 1 - Claims Ingestion Workflows

This document outlines step-by-step tasks to model claim ingestion workflows and audit payouts.

---

## Task 1: Map Claim Data Fields
*   **Goal**: Create a configuration file defining parsing targets for invoice documents.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `claims_fields.json` in `/tmp/`:
       ```json
       # /tmp/claims_fields.json
       {
         "extraction_fields": [
           "policyholder_name",
           "claim_date",
           "invoice_amount",
           "damage_description"
         ],
         "audit_rules": {
           "check_name_match": true,
           "max_invoice_limit": 5000.00
         }
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/claims_fields.json << 'EOF'
       {
         "extraction_fields": [
           "policyholder_name",
           "claim_date",
           "invoice_amount",
           "damage_description"
         ],
         "audit_rules": {
           "check_name_match": true,
           "max_invoice_limit": 5000.00
         }
       }
       EOF
       ```
    2. Write a Python script to parse and validate field rules:
       ```python
       # /tmp/parse_claims_rules.py
       import json
       import sys

       def verify_rules():
           with open("/tmp/claims_fields.json", "r") as f:
               data = json.load(f)
           
           print("Target Extraction Fields:")
           for field in data["extraction_fields"]:
               print(f"- {field}")
           print(f"Audit Max Limit: ${data['audit_rules']['max_invoice_limit']:.2f}")
           sys.exit(0)

       if __name__ == '__main__':
           verify_rules()
       ```
       Write this script:
       ```bash
       tee /tmp/parse_claims_rules.py << 'EOF'
       import json
       import sys

       def verify_rules():
           with open("/tmp/claims_fields.json", "r") as f:
               data = json.load(f)
           
           print("Target Extraction Fields:")
           for field in data["extraction_fields"]:
               print(f"- {field}")
           print(f"Audit Max Limit: ${data['audit_rules']['max_invoice_limit']:.2f}")
           sys.exit(0)

       if __name__ == '__main__':
           verify_rules()
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/parse_claims_rules.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/parse_claims_rules.py && echo "Claims configuration verified."
    ```

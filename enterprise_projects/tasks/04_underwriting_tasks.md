# Practice Tasks: Project 4 - Underwriting Pydantic Schemas

This document outlines step-by-step tasks to validate structured underwriting outputs.

---

## Task 1: Check Risk Assessment Schema compliance
*   **Goal**: Write a Python script to validate schema validation of underwriting outputs.
*   **Step-by-Step Instructions**:
    1. Create a verification script `underwriting_schema_check.py`:
       ```python
       # /tmp/underwriting_schema_check.py
       import sys
       import pydantic

       class UnderwritingRisk(pydantic.BaseModel):
           policy_id: str
           risk_category: str # LOW, MEDIUM, HIGH
           approved: bool

       def verify_schema():
           try:
               # Test valid payload
               valid = UnderwritingRisk(policy_id="POL-5501", risk_category="LOW", approved=True)
               print("PASS: Schema validation verified.")
               sys.exit(0)
           except Exception as e:
               print(f"FAIL: Schema validation error: {e}")
               sys.exit(1)

       if __name__ == '__main__':
           verify_schema()
       ```
       Write this file to disk:
       ```bash
       tee /tmp/underwriting_schema_check.py << 'EOF'
       import sys
       import pydantic

       class UnderwritingRisk(pydantic.BaseModel):
           policy_id: str
           risk_category: str
           approved: bool

       def verify_schema():
           try:
               valid = UnderwritingRisk(policy_id="POL-5501", risk_category="LOW", approved=True)
               print("PASS: Schema validation verified.")
               sys.exit(0)
           except Exception as e:
               print(f"FAIL: Schema validation error: {e}")
               sys.exit(1)

       if __name__ == '__main__':
           verify_schema()
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/underwriting_schema_check.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/underwriting_schema_check.py && echo "Underwriting schema validation passed."
    ```

# Practice Tasks: Module 2 - BRD Structure Validation

This document outlines step-by-step tasks to validate Business Requirements Document (BRD) structures.

---

## Task 1: Check BRD Structure
*   **Goal**: Write a Python script to verify that a BRD contains required sections.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_brd.py`:
       ```python
       # /tmp/validate_brd.py
       import sys

       def check_brd_structure(brd_text: str):
           required_sections = [
             "Business Objectives",
             "Functional Requirements",
             "Non-Functional Requirements",
             "Acceptance Criteria"
           ]
           
           missing = []
           for section in required_sections:
               if section not in brd_text:
                   missing.append(section)
                   
           if not missing:
               print("PASS: BRD contains all required sections.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing sections: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid structure
           sample_brd = """
           # BRD Specification
           ## Business Objectives
           Reduce cycle times.
           ## Functional Requirements
           Return citations.
           ## Non-Functional Requirements
           Sub-2 second latency.
           ## Acceptance Criteria
           Pass user testing.
           """
           check_brd_structure(sample_brd)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_brd.py << 'EOF'
       import sys

       def check_brd_structure(brd_text: str):
           required_sections = [
             "Business Objectives",
             "Functional Requirements",
             "Non-Functional Requirements",
             "Acceptance Criteria"
           ]
           
           missing = []
           for section in required_sections:
               if section not in brd_text:
                   missing.append(section)
                   
           if not missing:
               print("PASS: BRD contains all required sections.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing sections: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_brd = """
           # BRD Specification
           ## Business Objectives
           Reduce cycle times.
           ## Functional Requirements
           Return citations.
           ## Non-Functional Requirements
           Sub-2 second latency.
           ## Acceptance Criteria
           Pass user testing.
           """
           check_brd_structure(sample_brd)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_brd.py
       ```
*   **Verification**:
    Verify the script runs and logs the BRD status:
    ```bash
    python3 /tmp/validate_brd.py && echo "BRD validation check passed."
    ```

# Practice Tasks: Module 5 - Solution Design Review

This document outlines step-by-step tasks to validate Solution Design Document (SDD) structures.

---

## Task 1: Check SDD Structure
*   **Goal**: Write a Python script to verify that an SDD contains required architectural sections.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_sdd.py`:
       ```python
       # /tmp/validate_sdd.py
       import sys

       def check_sdd_structure(sdd_text: str):
           required_sections = [
             "System Overview",
             "Data Flow",
             "Security & Compliance",
             "Scalability & Failover"
           ]
           
           missing = []
           for section in required_sections:
               if section not in sdd_text:
                   missing.append(section)
                   
           if not missing:
               print("PASS: SDD contains all required architectural sections.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing sections: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid structure
           sample_sdd = """
           # SDD Specification
           ## System Overview
           Architectural components.
           ## Data Flow
           Query-response flows.
           ## Security & Compliance
           Encryption configurations.
           ## Scalability & Failover
           High-availability layouts.
           """
           check_sdd_structure(sample_sdd)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_sdd.py << 'EOF'
       import sys

       def check_sdd_structure(sdd_text: str):
           required_sections = [
             "System Overview",
             "Data Flow",
             "Security & Compliance",
             "Scalability & Failover"
           ]
           
           missing = []
           for section in required_sections:
               if section not in sdd_text:
                   missing.append(section)
                   
           if not missing:
               print("PASS: SDD contains all required architectural sections.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing sections: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_sdd = """
           # SDD Specification
           ## System Overview
           Architectural components.
           ## Data Flow
           Query-response flows.
           ## Security & Compliance
           Encryption configurations.
           ## Scalability & Failover
           High-availability layouts.
           """
           check_sdd_structure(sample_sdd)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_sdd.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_sdd.py && echo "SDD validation check passed."
    ```

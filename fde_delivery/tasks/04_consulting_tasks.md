# Practice Tasks: Module 4 - Roadmap Scoping Checks

This document outlines step-by-step tasks to validate execution roadmap timelines.

---

## Task 1: Check Phase Allocations
*   **Goal**: Write a Python script to verify that a project roadmap allocates tasks across three execution phases (PoC, Pilot, Rollout).
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_roadmap.py`:
       ```python
       # /tmp/validate_roadmap.py
       import sys

       def check_roadmap(roadmap: dict):
           required_phases = ["PoC", "Pilot", "Rollout"]
           
           missing = []
           for phase in required_phases:
               if phase not in roadmap:
                   missing.append(phase)
                   
           if not missing:
               print("PASS: Roadmap defines tasks across all three execution phases.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing roadmap phases: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with a valid roadmap
           sample_roadmap = {
             "PoC": "Validate core model feasibility",
             "Pilot": "Deploy prototype to test users",
             "Rollout": "Scale access to all production users"
           }
           check_roadmap(sample_roadmap)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_roadmap.py << 'EOF'
       import sys

       def check_roadmap(roadmap: dict):
           required_phases = ["PoC", "Pilot", "Rollout"]
           
           missing = []
           for phase in required_phases:
               if phase not in roadmap:
                   missing.append(phase)
                   
           if not missing:
               print("PASS: Roadmap defines tasks across all three execution phases.")
               sys.exit(0)
           else:
               print(f"FAIL: Missing roadmap phases: {missing}")
               sys.exit(1)

       if __name__ == '__main__':
           sample_roadmap = {
             "PoC": "Validate core model feasibility",
             "Pilot": "Deploy prototype to test users",
             "Rollout": "Scale access to all production users"
           }
           check_roadmap(sample_roadmap)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_roadmap.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_roadmap.py && echo "Roadmap validation passed."
    ```

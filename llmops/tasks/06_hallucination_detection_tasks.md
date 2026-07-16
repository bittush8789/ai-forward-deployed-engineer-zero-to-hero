# Practice Tasks: Module 6 - Fact-Verification & Grounding Checks

This document outlines step-by-step tasks to detect hallucinations in generated text.

---

## Task 1: Grounded Response Check
*   **Goal**: Write a Python script to verify that model outputs are grounded in the retrieved context.
*   **Step-by-Step Instructions**:
    1. Create a validation script `grounding_check.py`:
       ```python
       # /tmp/grounding_check.py
       import sys

       context = "Paris is the capital of France."
       model_output = "Paris is the capital of France and has a population of 2 million."

       # Simple check: verify that all key facts in the output exist in the context
       facts = ["Paris", "capital", "France"]
       all_present = all(fact in context for fact in facts)

       if all_present:
           print("PASS: Response is grounded in context (no hallucinations detected).")
           sys.exit(0)
       else:
           print("FAIL: Response contains ungrounded claims.")
           sys.exit(1)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/grounding_check.py << 'EOF'
       import sys

       context = "Paris is the capital of France."
       model_output = "Paris is the capital of France and has a population of 2 million."

       facts = ["Paris", "capital", "France"]
       all_present = all(fact in context for fact in facts)

       if all_present:
           print("PASS: Response is grounded in context (no hallucinations detected).")
           sys.exit(0)
       else:
           print("FAIL: Response contains ungrounded claims.")
           sys.exit(1)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/grounding_check.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/grounding_check.py && echo "Groundedness check passed."
    ```

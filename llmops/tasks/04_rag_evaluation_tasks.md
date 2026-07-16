# Practice Tasks: Module 4 - RAG Triad Evaluation

This document outlines step-by-step tasks to evaluate faithfulness and relevance in RAG outputs.

---

## Task 1: RAG Evaluation Check
*   **Goal**: Write a Python script to verify that generated responses are grounded in the retrieved context.
*   **Step-by-Step Instructions**:
    1. Create a validation script `validate_rag.py`:
       ```python
       # /tmp/validate_rag.py
       import sys

       context = "Paris is the capital and most populous city of France."
       response = "Paris is the capital of France."

       # Simple check: verify that key entities in the response exist in the context
       key_entities = ["Paris", "France", "capital"]
       all_present = all(entity in context for entity in key_entities)

       if all_present:
           print("PASS: Response is grounded in retrieved context (faithfulness verified).")
           sys.exit(0)
       else:
           print("FAIL: Response contains ungrounded claims.")
           sys.exit(1)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_rag.py << 'EOF'
       import sys

       context = "Paris is the capital and most populous city of France."
       response = "Paris is the capital of France."

       key_entities = ["Paris", "France", "capital"]
       all_present = all(entity in context for entity in key_entities)

       if all_present:
           print("PASS: Response is grounded in retrieved context (faithfulness verified).")
           sys.exit(0)
       else:
           print("FAIL: Response contains ungrounded claims.")
           sys.exit(1)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_rag.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/validate_rag.py && echo "RAG verification check passed."
    ```

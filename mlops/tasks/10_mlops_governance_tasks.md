# Practice Tasks: Module 10 - Model Lineage Validation

This document outlines step-by-step tasks to validate model metadata lineage.

---

## Task 1: Audit Metadata Validation Checks
*   **Goal**: Write a Python script to verify that a model version has recorded lineage details before deployment.
*   **Step-by-Step Instructions**:
    1. Create a validation script `check_lineage.py`:
       ```python
       # /tmp/check_lineage.py
       import json
       import sys

       # Load model card metadata
       model_card_path = "/tmp/model_card.json"

       try:
           with open(model_card_path, "r") as f:
               metadata = json.load(f)
               
           git_commit = metadata.get("model_details", {}).get("git_commit")
           dataset_hash = metadata.get("metrics", {}).get("evaluation_dataset_hash")
           
           if git_commit and dataset_hash:
               print(f"PASS: Lineage verified. Git Commit: {git_commit}, Dataset Hash: {dataset_hash}")
               sys.exit(0)
           else:
               print("FAIL: Missing Git Commit or Dataset Hash in model card.")
               sys.exit(1)
       except FileNotFoundError:
           print("FAIL: Model card metadata file not found.")
           sys.exit(2)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/check_lineage.py << 'EOF'
       import json
       import sys

       model_card_path = "/tmp/model_card.json"

       try:
           with open(model_card_path, "r") as f:
               metadata = json.load(f)
               
           git_commit = metadata.get("model_details", {}).get("git_commit")
           dataset_hash = metadata.get("metrics", {}).get("evaluation_dataset_hash")
           
           if git_commit and dataset_hash:
               print(f"PASS: Lineage verified. Git Commit: {git_commit}, Dataset Hash: {dataset_hash}")
               sys.exit(0)
           else:
               print("FAIL: Missing Git Commit or Dataset Hash in model card.")
               sys.exit(1)
       except FileNotFoundError:
           print("FAIL: Model card metadata file not found.")
           sys.exit(2)
       EOF
       ```
*   **Verification**:
    Generate a mock model card and verify the lineage check passes:
    ```bash
    # Generate mock model card using Module 10 script
    python3 /tmp/model_card_generator.py
    
    # Run lineage validation
    python3 /tmp/check_lineage.py
    ```

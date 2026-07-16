# Practice Tasks: Project 1 - Hybrid Search Verification

This document outlines step-by-step tasks to configure RRF (Reciprocal Rank Fusion) parameters for hybrid search.

---

## Task 1: Verify Hybrid Search Configuration
*   **Goal**: Create a configuration file defining BM25 and vector weight weights.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `hybrid_config.json` in `/tmp/`:
       ```json
       # /tmp/hybrid_config.json
       {
         "alpha": 0.5,
         "top_k": 10,
         "rerank": {
           "model": "cohere-rerank-v3",
           "top_n": 3
         }
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/hybrid_config.json << 'EOF'
       {
         "alpha": 0.5,
         "top_k": 10,
         "rerank": {
           "model": "cohere-rerank-v3",
           "top_n": 3
         }
       }
       EOF
       ```
    2. Write a Python script to parse the configuration:
       ```python
       # /tmp/parse_hybrid.py
       import json
       import sys

       def verify_config():
           with open("/tmp/hybrid_config.json", "r") as f:
               data = json.load(f)
           
           print(f"BM25 vs Vector weight (alpha): {data['alpha']}")
           print(f"Cohere Rerank Top N target: {data['rerank']['top_n']}")
           sys.exit(0)

       if __name__ == '__main__':
           verify_config()
       ```
       Write this script:
       ```bash
       tee /tmp/parse_hybrid.py << 'EOF'
       import json
       import sys

       def verify_config():
           with open("/tmp/hybrid_config.json", "r") as f:
               data = json.load(f)
           
           print(f"BM25 vs Vector weight (alpha): {data['alpha']}")
           print(f"Cohere Rerank Top N target: {data['rerank']['top_n']}")
           sys.exit(0)
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/parse_hybrid.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/parse_hybrid.py && echo "Hybrid search configuration verified."
    ```

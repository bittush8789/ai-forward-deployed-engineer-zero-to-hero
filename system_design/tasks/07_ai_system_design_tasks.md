# Practice Tasks: Module 7 - Ingestion Pipeline Layouts

This document outlines step-by-step tasks to design a RAG ingestion workflow.

---

## Task 1: Verify Ingestion Data Flow
*   **Goal**: Create a configuration file defining text splitting dimensions for document ingestion.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `ingest_config.json`:
       ```json
       # /tmp/ingest_config.json
       {
         "chunk_size": 500,
         "chunk_overlap": 50,
         "embedding_model": "text-embedding-ada-002"
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/ingest_config.json << 'EOF'
       {
         "chunk_size": 500,
         "chunk_overlap": 50,
         "embedding_model": "text-embedding-ada-002"
       }
       EOF
       ```
    2. Write a Python script to parse the configuration:
       ```python
       # /tmp/parse_ingest.py
       import json
       import sys

       def verify_config():
           with open("/tmp/ingest_config.json", "r") as f:
               data = json.load(f)
           
           print(f"Target Chunk Dimensions: {data['chunk_size']} tokens")
           print(f"Overlap Size: {data['chunk_overlap']} tokens")
           sys.exit(0)

       if __name__ == '__main__':
           verify_config()
       ```
       Write this script:
       ```bash
       tee /tmp/parse_ingest.py << 'EOF'
       import json
       import sys

       def verify_config():
           with open("/tmp/ingest_config.json", "r") as f:
               data = json.load(f)
           
           print(f"Target Chunk Dimensions: {data['chunk_size']} tokens")
           print(f"Overlap Size: {data['chunk_overlap']} tokens")
           sys.exit(0)

       if __name__ == '__main__':
           verify_config()
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/parse_ingest.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/parse_ingest.py && echo "Ingestion config parsed successfully."
    ```

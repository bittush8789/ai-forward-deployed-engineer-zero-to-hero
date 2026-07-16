# Practice Tasks: Module 4 - Velero Backup Configuration

This document outlines step-by-step tasks to configure Velero backup scripts.

---

## Task 1: Check Backup Storage Connection
*   **Goal**: Write a script to verify connection access to the backup storage bucket.
*   **Step-by-Step Instructions**:
    1. Create a verification script `verify_backup_store.py`:
       ```python
       # /tmp/verify_backup_store.py
       import os
       import sys

       def verify_store():
           # Check if target backup directory is writable
           backup_path = "/tmp/velero-mock-store"
           os.makedirs(backup_path, exist_ok=True)
           
           test_file = os.path.join(backup_path, "connection_test.txt")
           try:
               with open(test_file, "w") as f:
                   f.write("verify connection")
               print(f"Success: Backup store at {backup_path} is WRITABLE.")
               sys.exit(0)
           except Exception as e:
               print(f"Error accessing backup store: {e}")
               sys.exit(1)

       if __name__ == '__main__':
           verify_store()
       ```
       Write this file to disk:
       ```bash
       tee /tmp/verify_backup_store.py << 'EOF'
       import os
       import sys

       def verify_store():
           backup_path = "/tmp/velero-mock-store"
           os.makedirs(backup_path, exist_ok=True)
           
           test_file = os.path.join(backup_path, "connection_test.txt")
           try:
               with open(test_file, "w") as f:
                   f.write("verify connection")
               print(f"Success: Backup store at {backup_path} is WRITABLE.")
               sys.exit(0)
           except Exception as e:
               print(f"Error accessing backup store: {e}")
               sys.exit(1)

       if __name__ == '__main__':
           verify_store()
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/verify_backup_store.py
       ```
*   **Verification**:
    Verify the script runs and returns status code 0:
    ```bash
    python3 /tmp/verify_backup_store.py && echo "Backup store connection verified."
    ```

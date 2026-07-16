# Practice Tasks: Module 6 - Interface Validation Checks

This document outlines step-by-step tasks to configure Ports & Adapters validation scripts.

---

## Task 1: Verify Adapter Abstract Interfaces
*   **Goal**: Write a Python script to verify that database adapter classes implement required interfaces.
*   **Step-by-Step Instructions**:
    1. Create an interface script `adapter_check.py`:
       ```python
       # /tmp/adapter_check.py
       from abc import ABC, abstractmethod
       import sys

       class DatabasePort(ABC):
           @abstractmethod
           def save_record(self, data: dict):
               pass

       class PostgreSQLAdapter(DatabasePort):
           def save_record(self, data: dict):
               print(f"Record saved to PostgreSQL: {data}")

       if __name__ == '__main__':
           # Check if adapter implements database port interface
           adapter = PostgreSQLAdapter()
           is_valid = isinstance(adapter, DatabasePort)
           print(f"Adapter validation status: {'PASSED' if is_valid else 'FAILED'}")
           sys.exit(0)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/adapter_check.py << 'EOF'
       from abc import ABC, abstractmethod
       import sys

       class DatabasePort(ABC):
           @abstractmethod
           def save_record(self, data: dict):
               pass

       class PostgreSQLAdapter(DatabasePort):
           def save_record(self, data: dict):
               print(f"Record saved to PostgreSQL: {data}")

       if __name__ == '__main__':
           adapter = PostgreSQLAdapter()
           is_valid = isinstance(adapter, DatabasePort)
           print(f"Adapter validation status: {'PASSED' if is_valid else 'FAILED'}")
           sys.exit(0)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/adapter_check.py
       ```
*   **Verification**:
    Verify the script runs and logs the adapter validation status:
    ```bash
    python3 /tmp/adapter_check.py | grep "PASSED"
    ```

# Practice Tasks: Module 3 - DVC Dataset tracking

This document outlines step-by-step tasks to initialize DVC and version datasets.

---

## Task 1: Track Datasets using DVC
*   **Goal**: Create a local directory remote, track a CSV file using DVC, and commit pointer metadata to Git.
*   **Step-by-Step Instructions**:
    1. Initialize repository workspace:
       ```bash
       mkdir -p /tmp/dvc-tasks && cd /tmp/dvc-tasks
       git init
       dvc init
       ```
    2. Create a dummy dataset:
       ```bash
       echo "value_1,value_2" > data.csv
       echo "10,20" >> data.csv
       ```
    3. Add data to DVC tracking:
       ```bash
       dvc add data.csv
       ```
    4. Commit pointers to Git:
       ```bash
       git add data.csv.dvc .gitignore
       git commit -m "Track data.csv via DVC"
       ```
    5. Configure local remote directory storage:
       ```bash
       mkdir -p /tmp/dvc-tasks-remote
       dvc remote add -d myremote /tmp/dvc-tasks-remote
       dvc push
       ```
*   **Verification**:
    Verify the dataset is pushed successfully:
    ```bash
    ls -l /tmp/dvc-tasks-remote
    ```

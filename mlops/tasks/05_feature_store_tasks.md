# Practice Tasks: Module 5 - Feast Feature Store

This document outlines step-by-step tasks to initialize Feast, apply schemas, and materialize features.

---

## Task 1: Initialize and Ingest features
*   **Goal**: Initialize a local SQLite registry and materialize data.
*   **Step-by-Step Instructions**:
    1. Create a workspace:
       ```bash
       mkdir -p /tmp/feast-tasks && cd /tmp/feast-tasks
       feast init my_repo
       cd my_repo
       ```
    2. Apply the default configurations to build the SQLite registry:
       ```bash
       feast apply
       ```
    3. Ingest data into the online store:
       ```bash
       feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
       ```
*   **Verification**:
    Verify the local SQLite registry database has been created:
    ```bash
    ls -lh data/
    ```

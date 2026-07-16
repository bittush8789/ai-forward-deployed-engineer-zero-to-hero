# Practice Tasks: Module 4 - LakeFS Data Versioning

This document outlines step-by-step tasks to create data repositories, branches, and execute commits.

---

## Task 1: Initialize Repository and Branching via CLI
*   **Goal**: Create a repository and execute data branching and commits.
*   **Step-by-Step Instructions**:
    1. Verify your connection credentials variables are exported:
       ```bash
       export LAKECTL_SERVER_URL="http://localhost:8000"
       export LAKECTL_ACCESS_KEY_ID="my-access-key"
       export LAKECTL_SECRET_ACCESS_KEY="my-secret-key"
       ```
    2. Create a repository pointing to a storage bucket:
       ```bash
       # Simulated command (requires active LakeFS backend)
       # lakectl repo create lakefs://my-repo s3://my-bucket
       ```
    3. Create a data branch:
       ```bash
       # lakectl branch create lakefs://my-repo/dev-branch --source lakefs://my-repo/main
       ```
    4. Upload a test file:
       ```bash
       # echo "id,name" > /tmp/users.csv
       # lakectl fs upload /tmp/users.csv lakefs://my-repo/dev-branch/users.csv
       ```
    5. Commit the upload:
       ```bash
       # lakectl commit lakefs://my-repo/dev-branch -m "Commit description"
       ```
*   **Verification**:
    Verify the commit using the log command:
    ```bash
    # lakectl log lakefs://my-repo/dev-branch
    echo "Setup commands configured successfully."
    ```

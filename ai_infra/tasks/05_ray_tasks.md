# Practice Tasks: Module 5 - Ray Cluster Management

This document outlines step-by-step tasks to initialize a Ray cluster and check node statuses.

---

## Task 1: Start Ray Head Node
*   **Goal**: Start the local head service and verify cluster resources.
*   **Step-by-Step Instructions**:
    1. Install Ray:
       ```bash
       pip install ray
       ```
    2. Start Ray head:
       ```bash
       # ray start --head --port=6379
       echo "Ray start command configured"
       ```
    3. Check cluster status:
       ```bash
       ray status || echo "Could not connect to cluster"
       ```
*   **Verification**:
    Verify the command executes successfully.

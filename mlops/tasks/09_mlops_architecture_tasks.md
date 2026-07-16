# Practice Tasks: Module 9 - MLOps Topology Design

This document outlines step-by-step tasks to design a production MLOps system topology.

---

## Task 1: Component Mapping and Port Layout
*   **Goal**: Document port assignments and service connection routing for a local MLOps deployment.
*   **Step-by-Step Instructions**:
    1. Define and map default network ports for each service:
       *   **MLflow**: 5000
       *   **MinIO Console**: 9090
       *   **MinIO API**: 9000
       *   **Redis**: 6379
       *   **PostgreSQL**: 5432
       *   **LakeFS**: 8000
    2. Write a network check script `check_ports.sh`:
       ```bash
       #!/usr/bin/env bash
       set -euo pipefail
       
       PORTS=(5000 9000 6379 5432 8000)
       for PORT in "${PORTS[@]}"; do
           if nc -zv localhost "$PORT" 2>/dev/null; then
               echo "Port $PORT is OPEN and active."
           else
               echo "Port $PORT is CLOSED."
           fi
       done
       ```
       Write this script:
       ```bash
       tee /tmp/check_ports.sh << 'EOF'
       #!/usr/bin/env bash
       set -euo pipefail
       
       PORTS=(5000 9000 6379 5432 8000)
       for PORT in "${PORTS[@]}"; do
           if nc -zv localhost "$PORT" 2>/dev/null; then
               echo "Port $PORT is OPEN and active."
           else
               echo "Port $PORT is CLOSED."
           fi
       done
       EOF
       chmod +x /tmp/check_ports.sh
       ```
*   **Verification**:
    Run the script to check port status:
    ```bash
    /tmp/check_ports.sh
    ```

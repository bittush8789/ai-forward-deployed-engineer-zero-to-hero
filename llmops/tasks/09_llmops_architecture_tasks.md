# Practice Tasks: Module 9 - LLMOps Platform Topology Design

This document outlines step-by-step tasks to design a production LLMOps platform topology.

---

## Task 1: Component Port Mapping
*   **Goal**: Document and verify the network port layout for local service deployment.
*   **Step-by-Step Instructions**:
    1. Define default network ports for each service:
       *   **LiteLLM Gateway**: 8000
       *   **LangFuse Dashboard**: 3000
       *   **Redis Cache**: 6379
       *   **Prometheus**: 9090
    2. Write a verification check script `check_ports.sh`:
       ```bash
       #!/usr/bin/env bash
       set -euo pipefail
       
       PORTS=(8000 3000 6379 9090)
       for PORT in "${PORTS[@]}"; do
           if nc -zv localhost "$PORT" 2>/dev/null; then
               echo "Port $PORT is active."
           else
               echo "Port $PORT is offline."
           fi
       done
       ```
       Write this script:
       ```bash
       tee /tmp/check_ports_llm.sh << 'EOF'
       #!/usr/bin/env bash
       set -euo pipefail
       
       PORTS=(8000 3000 6379 9090)
       for PORT in "${PORTS[@]}"; do
           if nc -zv localhost "$PORT" 2>/dev/null; then
               echo "Port $PORT is active."
           else
               echo "Port $PORT is offline."
           fi
       done
       EOF
       chmod +x /tmp/check_ports_llm.sh
       ```
*   **Verification**:
    Run the port check script:
    ```bash
    /tmp/check_ports_llm.sh
    ```

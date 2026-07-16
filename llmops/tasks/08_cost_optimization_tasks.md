# Practice Tasks: Module 8 - Semantic Caching & Routing

This document outlines step-by-step tasks to configure token caching and model routing.

---

## Task 1: Model Routing Configuration
*   **Goal**: Create a configuration file defining fallback models and route queries dynamically.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `router_config.json`:
       ```json
       # /tmp/router_config.json
       {
         "routing_strategy": "simple-shuffle",
         "fallback_models": ["gpt-3.5-turbo", "llama-2"],
         "allowed_fails": 3
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/router_config.json << 'EOF'
       {
         "routing_strategy": "simple-shuffle",
         "fallback_models": ["gpt-3.5-turbo", "llama-2"],
         "allowed_fails": 3
       }
       EOF
       ```
    2. Write a Python script to parse the configuration and simulate fallback routing:
       ```python
       # /tmp/route_query.py
       import json
       import sys

       def route_query(query_str: str):
           with open("/tmp/router_config.json", "r") as f:
               config = json.load(f)
           
           print(f"Routing query: '{query_str}'")
           print(f"Fallback Strategy: {config['routing_strategy']}")
           print(f"Target Backup Models: {config['fallback_models']}")
           sys.exit(0)

       if __name__ == '__main__':
           route_query("Explain LLMOps platform routing configurations.")
       ```
       Write this script:
       ```bash
       tee /tmp/route_query.py << 'EOF'
       import json
       import sys

       def route_query(query_str: str):
           with open("/tmp/router_config.json", "r") as f:
               config = json.load(f)
           
           print(f"Routing query: '{query_str}'")
           print(f"Fallback Strategy: {config['routing_strategy']}")
           print(f"Target Backup Models: {config['fallback_models']}")
           sys.exit(0)

       if __name__ == '__main__':
           route_query("Explain LLMOps platform routing configurations.")
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/route_query.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/route_query.py && echo "Routing logic executed successfully."
    ```

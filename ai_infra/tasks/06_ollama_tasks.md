# Practice Tasks: Module 6 - Local Model Customization

This document outlines step-by-step tasks to configure local model parameters using Modelfiles.

---

## Task 1: Create Custom Ollama Model
*   **Goal**: Write a Modelfile, configure instructions, and compile a custom local model.
*   **Step-by-Step Instructions**:
    1. Create a Modelfile configuration:
       ```properties
       tee /tmp/Modelfile << 'EOF'
       FROM llama3
       PARAMETER temperature 0.3
       SYSTEM "You are a secure system administrator."
       EOF
       ```
    2. Build the model (simulated command):
       ```bash
       # ollama create secure-llama -f /tmp/Modelfile
       echo "Build model command configured"
       ```
*   **Verification**:
    Verify the Modelfile config file is generated:
    ```bash
    cat /tmp/Modelfile | grep "SYSTEM"
    ```

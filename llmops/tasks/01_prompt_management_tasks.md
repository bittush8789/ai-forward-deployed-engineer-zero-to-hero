# Practice Tasks: Module 1 - Prompt Management Setup

This document outlines step-by-step tasks to configure dynamic prompt templates and initialize registry configurations.

---

## Task 1: Setup Prompt Repository Configuration
*   **Goal**: Create a local prompt template directory, define parameters, and parse them in Python.
*   **Step-by-Step Instructions**:
    1. Create a workspace directory:
       ```bash
       mkdir -p /tmp/prompts-lab
       ```
    2. Define a template in YAML format:
       ```yaml
       # /tmp/prompts-lab/summarize_v1.yaml
       name: summarize_text
       version: 1
       template: |
         You are an expert editor. Summarize this:
         {input_text}
       ```
       Write this file to disk:
       ```bash
       tee /tmp/prompts-lab/summarize_v1.yaml << 'EOF'
       name: summarize_text
       version: 1
       template: |
         You are an expert editor. Summarize this:
         {input_text}
       EOF
       ```
    3. Write a Python script to parse the template and format values:
       ```python
       # /tmp/prompts-lab/parse_prompt.py
       import yaml

       def format_prompt(input_str: str):
           with open("/tmp/prompts-lab/summarize_v1.yaml", "r") as f:
               data = yaml.safe_load(f)
           
           template_str = data["template"]
           formatted = template_str.format(input_text=input_str)
           print("=== Rendered Prompt ===")
           print(formatted)

       if __name__ == '__main__':
           format_prompt("LLMOps enables automated model testing and deployments.")
       ```
       Write this script:
       ```bash
       tee /tmp/prompts-lab/parse_prompt.py << 'EOF'
       import yaml

       def format_prompt(input_str: str):
           with open("/tmp/prompts-lab/summarize_v1.yaml", "r") as f:
               data = yaml.safe_load(f)
           
           template_str = data["template"]
           formatted = template_str.format(input_text=input_str)
           print("=== Rendered Prompt ===")
           print(formatted)

       if __name__ == '__main__':
           format_prompt("LLMOps enables automated model testing and deployments.")
       EOF
       ```
    4. Run the script:
       ```bash
       python3 /tmp/prompts-lab/parse_prompt.py
       ```
*   **Verification**:
    Verify the script outputs the rendered prompt correctly:
    ```bash
    python3 /tmp/prompts-lab/parse_prompt.py | grep "Rendered Prompt"
    ```

# Practice Tasks: Module 2 - Prompt Version Control

This document outlines step-by-step tasks to initialize a Git-integrated prompt repository.

---

## Task 1: Initialize Git Version Tracking
*   **Goal**: Create a Git repository to version prompt template files and track revisions.
*   **Step-by-Step Instructions**:
    1. Create a prompts repository:
       ```bash
       mkdir -p /tmp/prompts-git-repo && cd /tmp/prompts-git-repo
       git init
       ```
    2. Write a prompt configuration file:
       ```json
       # /tmp/prompts-git-repo/prompt_v1.json
       {
         "name": "qa_prompt",
         "version": "1.0.0",
         "template": "Answer this question: {question}"
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/prompts-git-repo/prompt_v1.json << 'EOF'
       {
         "name": "qa_prompt",
         "version": "1.0.0",
         "template": "Answer this question: {question}"
       }
       EOF
       ```
    3. Commit the configuration file:
       ```bash
       git add prompt_v1.json
       git commit -m "feat: add initial QA prompt version"
       ```
    4. Tag the commit with SemVer:
       ```bash
       git tag -a "v1.0.0" -m "Initial release"
       ```
*   **Verification**:
    Verify the commit and tag history:
    ```bash
    git log --oneline
    git show v1.0.0
    ```

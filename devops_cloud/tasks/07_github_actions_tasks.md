# Practice Tasks: Module 7 - GitHub Actions

This document outlines step-by-step tasks to practice GitHub Actions workflow building, environment configuration, and action version pinning.

---

## Task 1: Building a Basic Lint Workflow
*   **Goal**: Create a local workflow file to run automated style checking on Python modifications.
*   **Step-by-Step Instructions**:
    1. Create the workflow directory structure inside your repository root:
       ```bash
       mkdir -p .github/workflows
       ```
    2. Create a workflow file named `lint-test.yml`:
       ```yaml
       # .github/workflows/lint-test.yml
       name: Linting Validator

       on:
         push:
           branches: [main]
         pull_request:
           branches: [main]

       jobs:
         python-lint:
           runs-on: ubuntu-latest
           steps:
             # Pin actions to commit SHAs for security
             - name: Checkout Code
               uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
               
             - name: Initialize Python
               uses: actions/setup-python@0a5c61591373683505ea898e09a3ea4f39ef2b9c # v5.0.0
               with:
                 python-version: "3.11"
                 
             - name: Install Linting Packages
               run: |
                 pip install flake8
                 
             - name: Execute Check
               run: |
                 flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
       ```
       Write this file to disk:
       ```bash
       tee .github/workflows/lint-test.yml << 'EOF'
       name: Linting Validator

       on:
         push:
           branches: [main]
         pull_request:
           branches: [main]

       jobs:
         python-lint:
           runs-on: ubuntu-latest
           steps:
             - name: Checkout Code
               uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
               
             - name: Initialize Python
               uses: actions/setup-python@0a5c61591373683505ea898e09a3ea4f39ef2b9c
               with:
                 python-version: "3.11"
                 
             - name: Install Linting Packages
               run: |
                 pip install flake8
                 
             - name: Execute Check
               run: |
                 flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
       EOF
       ```
*   **Verification**:
    Commit and push this workflow file to your GitHub repository. Navigate to the **Actions** tab in the GitHub UI and verify the run completes successfully.

---

## Task 2: Dependency Caching Setup
*   **Goal**: Integrate caching into your Python pipelines to optimize build execution speed.
*   **Step-by-Step Instructions**:
    1. Create a `requirements.txt` file in your repository:
       ```bash
       echo "flake8==6.1.0" > requirements.txt
       ```
    2. Add a caching step to `.github/workflows/lint-test.yml` before installing packages:
       ```yaml
       # Add this step after Initialize Python
       - name: Cache Pip Packages
         uses: actions/cache@704facf57e6136b1bc63b828d79edcd491e0ee84 # v3.3.2
         with:
           path: ~/.cache/pip
           key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
           restore-keys: |
             ${{ runner.os }}-pip-
       ```
    3. Update the installation step to use the cache:
       ```yaml
       - name: Install Linting Packages
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
       ```
*   **Verification**:
    Push the updated workflow file. In the first run, the cache is created. In the second run, you should see `Cache restored` in the logs, indicating a successful speedup.

# Module 7: CI/CD Automation with GitHub Actions

## 1. Architecture Deep Dive

GitHub Actions is an event-driven automation platform that allows you to run software development workflows directly in your GitHub repositories.

```
+---------------------------------------------------------------------------------------------------+
|                                         GitHub Platform                                           |
|   - Triggers (Pull Request, Push, Issue, Release)                                                 |
|   - Coordinates Workflow Runs, Job Schedules, and Logs                                            |
|   - Manages Secret Stores and Repository Configuration                                           |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (Secure HTTPS Connection)
+------------------------------------+--------------------------------------------------------------+
|                                      Runner Environment                                           |
|   +-------------------------------------------------------------------------------------------+   |
|   |   Job Execution Context                                                                   |   |
|   |   - Executed on GitHub-Hosted (Virtual Machine) or Self-Hosted (Bare Metal/K8s) Runners      |   |
|   |   - Runner agent polling loop pulls job configurations                                   |   |
|   +----+-------------------|---------------------------------|---------------------------+----+   |
|        |                   |                                 |                           |        |
|        v                   v                                 v                           v        |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
|   | Step 1     |  | Step 2          |               | Step 3                |  | Step 4         | |
|   | Setup      |  | Pull Action     |               | Compile Code          |  | Archive        | |
|   | Environment|  | (git checkout)  |               | (docker build)        |  | Artifacts      | |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
+---------------------------------------------------------------------------------------------------+
```

### Runners: Hosted vs. Self-Hosted
*   **GitHub-Hosted Runners**: Clean virtual machines (Ubuntu, Windows, or macOS) provisioned for each job run. They are secure and fully managed but lack persistent caching and have runtime execution limits.
*   **Self-Hosted Runners**: Physical servers or virtual machines that you manage. They allow you to use custom hardware configurations (like GPUs) and reuse build caches, but require manual security hardening and maintenance.

### Workflow Hierarchy
*   **Workflows**: Automated procedures defined in YAML files located in `.github/workflows/`.
*   **Events**: Specific activities that trigger workflows (e.g., `push`, `pull_request`, or manual `workflow_dispatch`).
*   **Jobs**: A set of steps executed on the same runner. Jobs run in parallel by default, but you can define dependencies between them.
*   **Steps**: Individual tasks that run commands or actions. Steps run sequentially.

---

## 2. Internal Working

### Runner Execution Loop
The runner application is an open-source agent written in .NET Core.
1.  The agent connects to GitHub using a long-polling HTTPS connection.
2.  When a workflow is triggered, GitHub schedules jobs and makes them available to the runner pool.
3.  The runner agent pulls the job configuration, downloads required actions, and executes steps sequentially.
4.  It streams logs and step execution status back to GitHub in real-time.

### OIDC (OpenID Connect) Cloud Access
To deploy resources to cloud providers (like AWS, Azure, or GCP), avoid storing permanent cloud access keys inside GitHub secrets.
*   Use OIDC to configure trust relationships.
*   When a job runs, the GitHub runner requests a temporary OIDC JSON Web Token (JWT).
*   The runner exchanges this JWT with the cloud provider for short-lived IAM credentials, minimizing security risks.

---

## 3. Production Use Cases

### Continuous Integration Pipelines
Automatically running linter suites, security vulnerability scans, unit tests, and compilation checks on every pull request before code is merged.

### Automated Container Image Building
Building Docker images, tagging them with Git SHAs, scanning them for vulnerabilities, and pushing them to enterprise container registries (like GHCR or AWS ECR) upon merging to the main branch.

---

## 4. Security Best Practices

### Pinning Action Versions to Git Commit SHAs
To prevent supply chain attacks (e.g., a third-party action repository getting compromised and introducing malicious code), pin actions to specific commit SHAs instead of version tags:
```yaml
# AVOID
uses: actions/checkout@v4

# SECURE
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

### Limiting Secret Scope
*   Limit write permissions for the default `GITHUB_TOKEN` within workflows.
*   Use environments with manual approval requirements to protect production deployment secrets.

---

## 5. Scalability Patterns

### Reusable Workflows
Write common pipeline steps (like Docker build and push configurations) as reusable workflows, and reference them across multiple repositories to maintain consistency:
```yaml
# Caller workflow
jobs:
  call-workflow:
    uses: my-org/shared-workflows/.github/workflows/docker-build.yml@main
    with:
      image-name: my-app
```

### Matrix Builds
Test code against multiple configurations (such as different operating systems or programming language versions) in parallel:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    python-version: ["3.10", "3.11"]
```

---

## 6. Reliability Patterns

### Concurrency Controls
Cancel in-progress runs when a developer pushes a new commit to the same pull request, saving runner capacity and keeping deployment queues clean:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Timeout Limits
Set explicit timeouts on jobs to prevent hung commands or network requests from running indefinitely and consuming build minutes:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
```

---

## 7. Cost Optimization

### Dependency Caching
Cache packages and build dependencies (like `node_modules` or Python `pip` packages) to speed up runs and reduce network traffic:
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

---

## 8. Hands-On Labs

### Lab 8.1: Setting up a Basic Linter Workflow
Create a workflow to run Python linters on code modifications.
```yaml
# .github/workflows/lint.yml
name: Lint Code

on:
  pull_request:
    branches: [main]

jobs:
  flake8-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8
          
      - name: Run linter
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Lab 8.2: Automating Docker Builds & Pushing to GHCR
Build a Docker image and push it to GitHub Container Registry.
```yaml
# .github/workflows/docker-publish.yml
name: Publish Docker Image

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: read
  packages: write

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### Lab 8.3: Deploying to Kubernetes via Workflows
```yaml
# Fragment to add under deployment step
- name: Set Kubernetes Context
  uses: azure/k8s-set-context@v3
  with:
    method: kubeconfig
    kubeconfig: ${{ secrets.KUBECONFIG }}

- name: Deploy manifests
  run: |
    kubectl set image deployment/my-app my-app=ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Lab 8.4: Structuring a Safe Terraform Execution Workflow
```yaml
# .github/workflows/terraform.yml
name: Infrastructure Pipeline

on:
  pull_request:
    branches: [main]

jobs:
  terraform-plan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Init
        run: terraform init

      - name: Plan
        run: terraform plan -no-color
```

### Lab 8.5: Vulnerability Scanning with Trivy
```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'ghcr.io/${{ github.repository }}:${{ github.sha }}'
    format: 'table'
    exit-code: '1' # Fail the build if vulnerabilities are found
    ignore-unfixed: true
    vuln-type: 'os,library'
    severity: 'CRITICAL,HIGH'
```

### Lab 8.6: Integration Testing Execution
```yaml
- name: Run Integration Tests
  run: |
    python -m unittest discover -s tests/integration
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Docker Registry Permission Denied
*   **Symptom**: Docker build pipeline fails on the push step with `denied: Permission to write to package denied`.
*   **Root Cause**: The default GITHUB_TOKEN permissions are restricted to read-only, or the package visibility settings in GitHub prevent write access.
*   **Resolution Strategy**:
    *   Verify the permissions block exists at the top of the workflow file:
        ```yaml
        permissions:
          packages: write
        ```
    *   Go to the package settings page in GitHub and grant write permissions to the repository's action workflow.

### Task 9.2: Stale Package Caches
*   **Symptom**: The build fails due to a dependency error, even though you updated `requirements.txt` or `package.json`.
*   **Root Cause**: The caching step matches the previous cache key, skipping package resolution and restoring old dependencies.
*   **Resolution Strategy**:
    *   Force cache invalidation by updating the cache key.
    *   Use the file hash of the lock file in the cache key definition:
        ```yaml
        key: ${{ runner.os }}-build-${{ hashFiles('**/requirements.txt') }}
        ```

### Task 9.3: Masked Secret Variables Hiding Errors
*   **Symptom**: A failed CLI step prints `***` values instead of descriptive error output, making it difficult to debug.
*   **Root Cause**: GitHub masks secret values in logs. If a CLI command returns a secret value as part of an error trace, the runner masks it.
*   **Resolution Strategy**:
    *   Do not echo secrets directly in run statements.
    *   Verify API credentials locally or direct command output to a file and inspect it securely.

---

## 10. Real Production Incidents

### Case Study: Leakage of Credentials via Debug Logging
*   **Incident**: A developer enabled step debugging (`ACTIONS_STEP_DEBUG=true`) to troubleshoot a workflow. An API initialization script printed all environment variables to standard output, exposing AWS credentials. The credentials were logged in the repository history, requiring security teams to revoke keys and rotate access secrets across the entire platform.
*   **Remediation**:
    *   Disabled permanent AWS credential keys.
    *   Implemented OIDC federation for cloud access across all pipelines.
    *   Configured automated credential scanners (like GitGuardian) to block commits containing sensitive strings.

---

## 11. Interview Questions

### Q1: What is the difference between a self-hosted runner and a GitHub-hosted runner?
*   **Answer**:
    *   **GitHub-hosted runners** are managed virtual machines run in isolated environments. They are clean for every job, secure, but have runtime limits.
    *   **Self-hosted runners** are managed by you. They can run on custom hardware (such as GPU nodes), reuse build dependencies, but require manual updates, provisioning, and security isolation.

### Q2: What is the purpose of the `GITHUB_TOKEN` environment variable?
*   **Answer**: The `GITHUB_TOKEN` is a temporary secret automatically created for each workflow run. It is used to authenticate steps with GitHub APIs (e.g., to create releases, publish packages, or leave comments on PRs). The token expires once the job completes.

### Q3: How do Matrix configurations help in testing architectures?
*   **Answer**: Matrix configurations allow you to run multiple jobs in parallel with different configurations (such as different operating systems, database versions, or runtime engines) using a single job definition, keeping pipeline code clean and maintainable.

### Q4: Explain the difference between `cache` and `artifacts` actions.
*   **Answer**:
    *   **Cache** is used to store packages and build files between workflow runs (e.g., caching `npm` modules to speed up subsequent builds).
    *   **Artifacts** are used to save files (like test reports or build binaries) generated during a workflow run. Artifacts can be shared between jobs in the same run or downloaded from the GitHub UI after the run finishes.

### Q5: What are the security benefits of using OpenID Connect (OIDC) over storing static API tokens?
*   **Answer**: OIDC removes the need to store long-lived cloud credentials (like AWS ACCESS_KEY_ID) in GitHub. Instead, the workflow requests a short-lived token from the cloud provider, reducing the risk of credentials leaking if the repository or runner is compromised.

---

## 12. Enterprise Case Studies

### Pipeline Consolidation at Dow Jones
Dow Jones consolidated its multiple CI platforms (Jenkins, Travis, CircleCI) into a unified GitHub Actions infrastructure. By using reusable workflows and centralizing security scans, they automated pipeline configurations for over 1,500 repositories. This reduced CI build queues, standardizing build compliance requirements across developer teams.

---

## 13. System Design Discussions

### Self-Hosted Runner Infrastructure inside Kubernetes
*   **Objective**: Design a self-hosted runner pool inside a secure Kubernetes cluster.
*   **Architecture Considerations**:
    *   **Orchestration**: Deploy the **Action Runner Controller (ARC)** operator.
    *   **Auto-scaling**: Configure the runner deployment to scale pods dynamically based on pending workflow runs queue length.
    *   **Isolation**: Run runner pods as unprivileged users. Enable ephemeral environments where each runner pod is terminated after executing a single job, preventing side-channel attacks or data residue leaks across builds.

---

## 14. AI Platform Perspective

### GPU-Enabled Self-Hosted Runners for Model Verification
Testing deep learning models requires running code on GPU hardware.

```yaml
# Workflow targeting a self-hosted GPU runner
name: Model Verification Test

on:
  push:
    branches: [main]

jobs:
  test-gpu-eval:
    # Target self-hosted runner pool with GPU access
    runs-on: [self-hosted, linux, x64, gpu-enabled]
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Verify CUDA Access
        run: nvidia-smi

      - name: Run PyTorch Eval tests
        run: python3 -m unittest discover -s tests/eval
```
By utilizing self-hosted runners configured on physical GPU servers, development teams can automate training convergence tests and model evaluation metrics as part of their standard CI/CD lifecycle.

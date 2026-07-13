# Module 4.6: AI FDE Git Patterns

Welcome to **Module 4.6**. How do you version control a 70 Billion parameter LLaMA model? (Hint: You don't put it in Git). As an FDE, you manage Monorepos and implement strict versioning for non-code assets like Prompts and ML Models.

---

## 1. Detailed Theory

### Monorepos vs. Multi-Repos
- **Multi-Repo**: Every microservice (FastAPI Backend, React Frontend, LangGraph Agents) gets its own Git repository.
- **Monorepo**: All code for the entire company lives in ONE massive Git repository. (Google, Meta, and many modern AI startups use this). It ensures that a breaking change to a shared schema immediately breaks tests across all projects, preventing integration bugs.

### AI Model Versioning
Git is designed for text files (code), not 10GB binary weight files (`.pt` or `.bin`). 
- **DVC (Data Version Control)**: A tool that looks and feels like Git, but tracks large data files and AI models by storing them in S3 buckets while only keeping a small text pointer file in Git.

### Prompt Versioning
Prompts are code. If an FDE tweaks a LangChain system prompt, it must be versioned. Enterprise systems store prompts in `.txt` or `.yaml` files in the Git repo, NOT hardcoded as Python strings, so changes can be reviewed in PRs.

---

## 2. Architecture Diagram: The AI Monorepo

```text
enterprise-ai-platform/ (Git Root)
├── .github/workflows/
├── apps/
│   ├── web-ui/ (React)
│   ├── api-gateway/ (FastAPI)
│   └── agent-service/ (LangGraph)
├── packages/
│   ├── shared-schemas/ (Pydantic models used by both API and Agent)
│   └── custom-llm-wrapper/ (Python library)
└── prompts/
    ├── v1/
    │   └── triage_agent.yaml
    └── v2/
        └── triage_agent.yaml
```

---

## 3. Production Use Cases

1. **Shared Schemas (Monorepo)**: The API Gateway and the Agent Service both need to know what a `TicketPayload` looks like. In a Monorepo, they both import from `packages/shared-schemas`. If a developer adds a required field to `TicketPayload`, the CI pipeline instantly runs tests for both microservices to ensure nothing breaks.
2. **Prompt A/B Testing**: Storing prompts in Git under `prompts/v1` and `prompts/v2`. The FastAPI app reads these files at runtime and routes 50% of traffic to v1 and 50% to v2 to test which prompt generates fewer hallucinations.

---

## 4. Real Company Examples

- **Google**: Operates the largest Monorepo in the world (Piper). Billions of lines of code. If you update a core library, you must fix every downstream project that breaks.
- **HuggingFace**: Uses an extension of Git (Git LFS - Large File Storage) to allow users to clone repositories containing massive machine learning models natively.

---

## 5. Coding Examples

### Prompt Versioning (Git + Python)

*Inside your Git Repo, you have `prompts/system.yaml`*
```yaml
version: "1.2.0"
author: "Alice FDE"
template: |
  You are an enterprise AI.
  Current strict policy: Do NOT provide financial advice.
```

*Inside `agent.py`*
```python
import yaml
import os

def load_prompt():
    # Read the prompt from the file tracked by Git
    prompt_path = os.path.join("prompts", "system.yaml")
    with open(prompt_path, 'r') as f:
        data = yaml.safe_load(f)
        
    print(f"Loaded Prompt Version: {data['version']}")
    return data['template']

# If Alice opens a PR modifying system.yaml, it triggers a GitHub Action!
```

---

## 6. Hands-on Labs

**Lab: Git LFS (Large File Storage)**
**Objective**: Track a mock ML model without bloating Git.
**Instructions**:
1. Run `git lfs install` (Assuming you downloaded Git LFS).
2. Create a massive fake file: `dd if=/dev/zero of=model.bin bs=1M count=50`. (Creates a 50MB file).
3. Tell Git LFS to track binaries: `git lfs track "*.bin"`.
4. Run `git add .gitattributes model.bin`.
5. Commit and push. Git will push the actual 50MB file to an external LFS server, and only a tiny 100-byte pointer file to the Git repository history!

---

## 7. Assignments

**Assignment: Monorepo Architecture Analysis**
Look at the architecture diagram in Section 2. Write a paragraph explaining the deployment strategy. If a developer edits a file in `packages/shared-schemas`, which applications (`web-ui`, `api-gateway`, `agent-service`) need to be rebuilt and redeployed?
*(Answer Hint: Since `web-ui` is React, it likely uses a TypeScript version of schemas, but assuming a purely Python ecosystem, both `api-gateway` and `agent-service` import from `shared-schemas`. Both must be rebuilt, tested, and deployed to ensure compatibility).*

---

## 8. Interview Questions

1. **Why is it a bad idea to put a 5GB PyTorch `.pt` model file directly into standard Git?**
   *Answer Hint: Git tracks every version of every file. If you update that 5GB file 10 times, your `.git` folder will grow to 50GB. Anyone running `git clone` will have to download 50GB before they can write a single line of code.*
2. **What is a Monorepo, and what tooling is required to make it work?**
   *Answer Hint: A single repository holding multiple projects. It requires advanced build systems (like Bazel, Turborepo, or Pants) that only test and build the specific sub-folders that changed, otherwise CI pipelines would take hours to run.*

---

## 9. Best Practices (FDE Standards)

- **Treat Prompts as Code**: A bad prompt can crash an application just as easily as a bad `if` statement. Prompts must go through the exact same PR and Code Review process as Python code. Never edit a prompt directly in a production UI console.

---

## 10. Common Mistakes

- **Git Cloning Large Repos**: Running `git clone` on a massive enterprise Monorepo over a slow hotel Wi-Fi connection during an FDE deployment. 
  *Fix: Use `git clone --depth 1 <url>`. This does a "Shallow Clone", downloading ONLY the latest snapshot of the code and ignoring the 10 years of history, saving gigabytes of bandwidth.*

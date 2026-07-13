# Git Capstone Project: Enterprise GitOps Platform

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 6-8 Hours
**Primary Tech Stack:** Git, GitHub Actions, Markdown, Docker

---

## 1. Project Overview

You are deployed to a startup that has terrible engineering practices. Developers push directly to `main`, AI models are uploaded to Google Drive, and API keys are hardcoded. You must architect a secure, automated GitOps repository structure for their new AI Platform.

## 2. Requirements

1. **Repository Setup**: Create a local Git repository modeled as a Monorepo.
2. **Branch Protection (Simulated)**: Create a `main` and `develop` branch. Write a `README.md` documenting the exact GitFlow process the team must follow.
3. **CI/CD Pipeline**: Write a GitHub Actions YAML file that lints Python code and builds a Docker image.
4. **Prompt Versioning**: Create a tracked directory for LLM Prompts.

## 3. Directory Structure to Build

Your final repository should look like this:
```text
enterprise-ai/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── api/
│   ├── main.py (Mock FastAPI app)
│   ├── Dockerfile
│   └── requirements.txt
└── prompts/
    └── v1/
        └── customer_support.yaml
```

## 4. Tasks to Complete

1. **Initialize**: Run `git init`. Create the `.gitignore` to ignore `__pycache__` and `.env`.
2. **Templates**: Write a strict `PULL_REQUEST_TEMPLATE.md` requiring developers to link to Jira tickets and confirm they haven't hardcoded API keys.
3. **CODEOWNERS**: Write a `.github/CODEOWNERS` file that forces the `@data-science` team to review any PR that modifies files in the `prompts/` directory.
4. **GitHub Actions**: Write `ci.yml`. It should trigger on Pull Requests to `main`. It should check out the code, set up Python, and run `pip install flake8 && flake8 api/main.py`.
5. **Git History**:
   - Make an initial commit on `main`.
   - Branch to `feature/add-api`.
   - Create the `api/` folder and mock code. Commit.
   - Branch to `feature/add-prompts`.
   - Create the `prompts/` folder. Commit.
   - Run a `git merge` or `git rebase` to combine these into your `develop` or `main` branch to simulate a completed workflow.

## 5. Submission Checklist
- [ ] A clean `git log --graph --oneline` showing feature branches merging into main.
- [ ] Functional `.gitignore` preventing secrets from being tracked.
- [ ] A valid `.github/workflows/ci.yml` that would successfully run on GitHub.
- [ ] A `CODEOWNERS` file implementing security governance over the AI prompt assets.

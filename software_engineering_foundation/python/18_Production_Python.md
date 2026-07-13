# Module 18: Production Python for AI FDEs

Welcome to **Module 18**. Writing the code is only 30% of the job. The other 70% is getting that code to run securely, reliably, and consistently on a client's enterprise infrastructure. This module covers the essential devops and packaging skills required for a Forward Deployed Engineer.

---

## 1. Detailed Theory

### Configuration & Environment Variables
Hardcoding API keys, database passwords, or endpoint URLs in your Python code is a fireable offense. All configuration that changes between environments (Dev, Staging, Prod) MUST be injected via Environment Variables (`.env` files).

### Secrets Management
In enterprise deployments, you don't even use `.env` files for production. Passwords are kept in secure vaults (like AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault). Your Python app authenticates with the Vault using IAM roles to fetch the API keys at runtime.

### Dockerization
"It works on my machine" is solved by Docker. Docker packages your Python code, the exact Python interpreter version, the OS libraries, and the dependencies into a single, immutable container image. This image will run identically on your laptop and on a Kubernetes cluster.

### Makefiles
FDEs often use `Makefiles` to create aliases for complex setup commands. (e.g., `make build`, `make test`, `make deploy`).

---

## 2. Architecture Diagram: CI/CD & Deployment Flow

```mermaid
graph TD
    A[FDE pushes code to GitHub] --> B(GitHub Actions CI)
    
    subgraph CI Pipeline
        B --> C[Run Pytest]
        C --> D[Run Mypy & Linter]
    end
    
    D -->|Tests Pass| E(Build Docker Image)
    E --> F[(Docker Registry / ECR)]
    
    F --> G(Kubernetes Cluster pulls Image)
    
    subgraph Kubernetes Prod
        G --> H[FastAPI Pod 1]
        G --> I[FastAPI Pod 2]
        H -.-> J[AWS Secrets Manager fetches API Key]
    end
    
    style E fill:#d5e8d4,stroke:#333
    style J fill:#f96,stroke:#333
```

---

## 3. Production Use Cases

1. **Client Deployment (Docker)**: An FDE arrives at an Air-Gapped (no internet) defense client. They cannot `pip install`. They bring a Docker image on a secure drive and run the entire AI application instantly.
2. **Environment Overrides**: Running an AI app locally uses `DATABASE_URL=sqlite:///test.db`. When deployed to AWS, the container is injected with `DATABASE_URL=postgresql://user:pass@rds-server`. The Python code never changes.
3. **Multi-Model Support**: Using environment variables like `ACTIVE_LLM_PROVIDER=azure` to toggle which API client the Python backend instantiates.

---

## 4. Real Company Examples

- **Palantir**: Uses Docker (Apollo platform) extensively to deploy highly secure, containerized Python microservices across vastly different client infrastructures (AWS, Azure, On-Prem servers).
- **Any AI Startup**: Deploys containerized FastAPI backends to Vercel, Render, or AWS Fargate.

---

## 5. Coding Examples

### Secure Configuration with Pydantic BaseSettings

*Pre-requisite: `pip install pydantic-settings`*

Instead of raw `os.getenv()`, modern apps use Pydantic to validate that the required environment variables actually exist when the app boots up.

```python
# file: config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Enterprise AI Copilot"
    api_key: str          # Required! App will crash if not found.
    database_url: str     # Required!
    debug_mode: bool = False # Has a default
    
    class Config:
        env_file = ".env" # Will read from a .env file during local dev

# Will parse OS env vars, cast types, and validate!
settings = Settings()

print(f"Connecting to {settings.database_url}")
# print(settings.api_key) # Never print this in production!
```

### The Ultimate Python Dockerfile

```dockerfile
# 1. Base Image (Slim, secure, Python 3.11)
FROM python:3.11-slim-bookworm

# 2. Set environment variables to optimize Python for Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.0

# 3. Create a non-root user for security (MANDATORY in enterprise)
RUN useradd -m -r appuser

# 4. Set working directory
WORKDIR /app

# 5. Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# 6. Copy ONLY dependency files first (Leverages Docker build cache!)
COPY pyproject.toml poetry.lock ./

# 7. Install dependencies (without virtualenvs, since Docker is isolated)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# 8. Copy the rest of the application code
COPY src/ ./src/

# 9. Switch to the secure non-root user
USER appuser

# 10. Expose the FastAPI port
EXPOSE 8000

# 11. Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 6. Hands-on Labs

**Lab: The `.env` Loader**
**Objective**: Separate config from code.
**Instructions**:
1. Create a file named `.env` manually. Add:
   `OPENAI_API_KEY=sk-mock123`
   `PORT=8080`
2. In a Python script, `import os` and `from dotenv import load_dotenv`. (Run `pip install python-dotenv` first).
3. Call `load_dotenv()`.
4. Read the values: `port = int(os.getenv("PORT", 8000))`.
5. Print the port.

---

## 7. Assignments

**Assignment: Build the Docker Image**
*Pre-requisite: Install Docker Desktop.*
1. Take the Dockerfile provided in section 5. Save it as `Dockerfile`.
2. Create a `pyproject.toml` or `requirements.txt` with `fastapi` and `uvicorn`.
3. Create a simple `src/main.py` FastAPI app.
4. Run `docker build -t enterprise-ai-app .` in your terminal.
5. Run `docker run -p 8000:8000 enterprise-ai-app`.
6. Visit `localhost:8000` in your browser. You just deployed a container!

---

## 8. Interview Questions

1. **Why do we copy the `requirements.txt` (or poetry locks) and run `pip install` BEFORE copying the rest of the application code in a Dockerfile?**
   *Answer Hint: Docker caches layers. Dependencies rarely change, but application code changes constantly. By copying dependencies first, Docker skips the 5-minute `pip install` process on subsequent builds, speeding up CI/CD.*
2. **Why must you run your Python web server as a non-root user inside a Docker container?**
   *Answer Hint: Security. If an attacker exploits a vulnerability in your FastAPI code or a dependency, and the app runs as root, they gain root access to the container and potentially the host machine. Running as `appuser` limits the blast radius.*
3. **What does `PYTHONUNBUFFERED=1` do?**
   *Answer Hint: It prevents Python from buffering stdout/stderr. In Docker, if output is buffered, you might not see your logs in the external system (like Datadog) immediately, or they might be lost if the container crashes.*

---

## 9. Best Practices (FDE Standards)

- **Use `.dockerignore`**: Always create a `.dockerignore` file containing `.git`, `__pycache__`, `.env`, and `venv/`. This prevents secure keys and massive useless folders from being bloated into your Docker image.
- **Fail Fast on Boot**: Use Pydantic BaseSettings. If an environment variable is missing, the app should crash *immediately* during `uvicorn` startup, not 3 days later when a user hits a specific endpoint.

---

## 10. Common Mistakes

- **Committing `.env` to Git**: This is the fastest way to leak company API keys and get fired. Ensure `.env` is inside your `.gitignore` file.
- **Using `latest` Docker tags**: `FROM python:latest`. Tomorrow, `latest` might point to Python 3.13 which breaks your LangChain dependencies. Always pin specific versions (e.g., `python:3.11.6-slim`).

---

## 11. End-to-End Project: Multi-Environment Config Bootstrapper

**Scenario**: You need a script that ensures the environment is perfectly configured before the AI model starts. It checks for keys, sets up folders, and validates connections.

**Code (`pre_flight_check.py`):**
```python
import os
import sys

def check_env_vars():
    required_keys = ["OPENAI_API_KEY", "DB_HOST", "ENVIRONMENT"]
    missing = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)
            
    if missing:
        print(f"[CRITICAL] Boot failed. Missing required environment variables: {missing}")
        print("Please inject these via Docker ENV or .env file.")
        sys.exit(1) # Exit with error code to halt Docker deployment

def check_directories():
    required_dirs = ["/app/logs", "/app/data/chromadb"]
    
    for d in required_dirs:
        if not os.path.exists(d):
            print(f"[INFO] Directory {d} not found. Creating...")
            # In a real Docker container, you need write permissions here!
            try:
                os.makedirs(d, exist_ok=True)
            except PermissionError:
                print(f"[CRITICAL] Permission denied creating {d}. Are you running as root?")
                sys.exit(1)

def run_pre_flight():
    print("--- Starting Application Pre-Flight Checks ---")
    
    # In local dev, we might load .env here. In prod Docker, they are already injected.
    if os.getenv("ENVIRONMENT") == "development":
        print("[INFO] Development mode detected. Loading .env file.")
        # load_dotenv() # requires python-dotenv
        
    check_env_vars()
    check_directories()
    
    print("[SUCCESS] Pre-flight checks passed. Booting FastAPI...")
    # Here you would normally run uvicorn programmatically, or let the script exit 
    # successfully so the Docker CMD can proceed.

if __name__ == "__main__":
    # Mocking env vars so the script passes when you test it
    os.environ["OPENAI_API_KEY"] = "sk-mock"
    os.environ["DB_HOST"] = "localhost"
    os.environ["ENVIRONMENT"] = "development"
    
    run_pre_flight()
```

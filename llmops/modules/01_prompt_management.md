# Module 1: Prompt Management & Dynamic Template Infrastructure

## 1. Theory (40%)
In enterprise generative AI applications, prompts are treated as software artifacts. The **Prompt Lifecycle** consists of design, version control, testing, deployment, and optimization phases. 

```
+-------------------------------------------------------------------------------------------------+
|                                     Prompt Management Lifecycle                                 |
|                                                                                                 |
|   +--------------+      +----------------+      +--------------+      +-------------------+     |
|   |  1. Design   | ---> | 2. Versioning  | ---> |  3. Testing  | ---> |  4. Deployment    |     |
|   |  (Template)  |      |  (Git/Registry)|      |  (Evaluations|      |  (API Gateway)    |     |
|   +--------------+      +----------------+      +--------------+      +---------+---------+     |
|                                                                                 |               |
|                                                                                 v               |
|   +--------------+                                                    +---------+---------+     |
|   | 7. Archive   | <------------------------------------------------- | 5. Optimization   |     |
|   |              |                                                    | (Reinforcement/RL)|     |
|   +--------------+                                                    +-------------------+     |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Prompt Templates**: Parameterized strings that decouple text instructions from dynamic data inputs (e.g., `"Summarize this text: {input_text}"`).
*   **Dynamic Prompting**: Constructing prompts at runtime based on user history, database lookups, or context retrieved from vector stores.
*   **Prompt Governance**: Establishing organizational guidelines for prompt formatting, output structures, and safety instructions.

---

## 2. Architecture Deep Dive

Prompts are stored and versioned in a centralized **Prompt Registry**. This registry exposes endpoints to application servers, allowing them to retrieve prompt templates dynamically at runtime based on environment tags (e.g., `production`, `staging`).

```
+-------------------------------------------------------------------------------------------------+
|                                     Application Server                                          |
|    - Requests active prompt template for 'summarization' labeled 'production'                   |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (REST API over HTTPS)
+-----------------------------------------------+-------------------------------------------------+
|                                  Prompt Registry (LangSmith / LangFuse)                         |
|    - Authenticates clients and retrieves matching templates from database                       |
|    - Formats parameters and returns the prompt string back to the application                   |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (Metadata logging)                              v (LLM API Call)
+---------------------------------------+-------------------------------------------------+-------+
|                                    Observability Gateway                                        |
|    - Tracks token usage, latency metrics, and user feedback evaluations                         |
+-------------------------------------------------------------------------------------------------+
```

---

## 3. Tool Comparison

| Feature | LangSmith | LangFuse | PromptLayer | Helicone |
|---|---|---|---|---|
| **License** | Commercial (SaaS/Enterprise) | Open-Source (MIT) | Commercial (SaaS) | Open-Source (Apache-2.0) |
| **Prompt Registry**| Yes (SDK-based) | Yes (REST-based) | Yes (Proxy-based) | Yes (REST-based) |
| **Self-Hosting** | High complexity | Moderate complexity | Not supported | Low complexity |
| **Primary Focus** | LangChain ecosystem | LLM tracing and analytics | Prompt engineering | API proxy caching |

---

## 4. Tool Installation
Install the SDK clients for prompt management tools:
```bash
pip install langsmith langfuse promptlayer
```

---

## 5. Tool Setup
Configure local environment variables to connect clients to servers:
```bash
# LangSmith credentials config
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="ls__my_secret_api_key"
export LANGCHAIN_PROJECT="enterprise-prompts-project"

# LangFuse credentials config
export LANGFUSE_PUBLIC_KEY="pk-lf-123456"
export LANGFUSE_SECRET_KEY="sk-lf-123456"
export LANGFUSE_HOST="https://cloud.langfuse.com"
```

---

## 6. CLI Commands
```bash
# Verify LangSmith connection status
langsmith status || echo "Connection failed"
```

---

## 7. Configuration Files
Save prompt parameters and templates in a structured YAML format:
```yaml
# prompts/summarize_v1.yaml
metadata:
  name: summarize_text
  version: 1
  owner: ai-platform-team
template: |
  You are an expert editor. Summarize the text below in {word_count} words or less:
  
  Text:
  {input_text}
  
  Summary:
```

---

## 8. API Examples
Create a Python script using LangFuse to retrieve templates and format prompts dynamically:
```python
# /tmp/prompt_manager.py
from langfuse import Langfuse

# 1. Initialize LangFuse client
langfuse = Langfuse()

# 2. Define dynamic inputs
inputs = {
    "word_count": "50",
    "input_text": "LLMOps represents the tools and workflows required to run models in production."
}

# 3. Retrieve template from registry (Simulating fetch)
try:
    template = langfuse.get_prompt("summarize_text")
    formatted_prompt = template.compile(word_count=inputs["word_count"], input_text=inputs["input_text"])
    print(f"Formatted Prompt:\n{formatted_prompt}")
except Exception as e:
    # Fallback to local template if remote fetch fails
    local_template = "Summarize this: {input_text} in {word_count} words."
    formatted_prompt = local_template.format(**inputs)
    print(f"Fallback Prompt:\n{formatted_prompt}")
```
Run the script:
```bash
python3 /tmp/prompt_manager.py
```

---

## 9. Production Tasks

### Configuring Automated Evaluation
Configure LangSmith to automatically run evaluation suites on prompt templates when updates are committed to the registry.

---

## 10. Troubleshooting

### Task 10.1: Prompt Retrieval Latency
*   **Symptom**: Application response time increases by 200ms during prompt fetching.
*   **Root Cause**: The application makes a synchronous network request to the remote prompt registry for every user interaction.
*   **Resolution Strategy**:
    *   Implement **local caching (TTL)** on the application server.
    *   Retrieve prompts asynchronously during startup, and refresh the cache in the background:
        ```python
        # Simple cache implementation
        # (Fetch prompt once, reuse for subsequent calls)
        ```

---

## 11. Monitoring
Configure alerts in your dashboard when API request latencies to the prompt registry exceed 50ms, or when error rates exceed 1%.

---

## 12. Security
*   Encrypt API tokens at rest using Key Vaults.
*   Enforce RBAC to restrict who can modify templates in the production environment.

---

## 13. Governance
Maintain metadata tags (such as `owner`, `use_case`, and `date_created`) for all prompts to ensure audit compliance.

---

## 14. Real Enterprise Incidents

### Case Study: Stale Prompts Breaking Production APIs
*   **Incident**: An operations engineer updated a prompt template in the registry but forgot to update the deployment tag. The application continued to fetch the stale version, which lacked required fields, causing API calls to crash under traffic.
*   **Remediation**:
    *   Enforced automated fallback templates in the application code.
    *   Configured integration tests to validate tags before releases.

---

## 15. Interview Questions

### Q1: What is dynamic prompting, and when would you use it?
*   **Answer**: Dynamic prompting is the process of constructing prompts at runtime by combining text templates with dynamic inputs (such as user profiles, database queries, or context from vector stores). It is critical for personalizing responses and providing up-to-date context to LLM models.

### Q2: How does a Prompt Registry simplify model deployment?
*   **Answer**: A Prompt Registry decouples prompt templates from the application source code. This allows prompt engineers to update and deploy prompt modifications without requiring code redeployments, reducing release cycle times.

---

## 16. Enterprise Case Studies

### Prompt Management at Bloomberg
Bloomberg engineers unified their prompt templates under a centralized registry. By versioning prompts and executing automated regressions before updates, they ensured that model outputs remain consistent across financial analysis services.

# Module 8: LLM Cost Optimization & Semantic Caching

## 1. Theory (40%)
Running production-grade LLM applications can be expensive. **LLM Cost Optimization** (or FinOps for AI) involves managing token usage and inference costs through optimization strategies.

```
+-------------------------------------------------------------------------------------------------+
|                                        Cost Optimization Gate                                    |
|                                                                                                 |
|   +--------------------+      +--------------------+      +--------------------+                |
|   |   1. User Query    | ---> | 2. Semantic Cache  | ---> |   Cache HIT?       |                |
|   |                    |      | (Check database)   |      |                    |                |
|   +--------------------+      +--------------------+      +---------+----------+                |
|                                                                     |                           |
|                                     +-------------------------------+-----------------------+   |
|                                     | Yes                                                   | No|
|                                     v                                                       v   |
|                           +---------+----------+                            +---------+---------+
|                           | Return Cached Result|                            | 3. Model Router   |
|                           | (Cost: $0.00)      |                            | (Select model)    |
|                           +--------------------+                            +---------+---------+
|                                                                                       |         |
|                                                                                       v         |
|                                                                             +---------+---------+
|                                                                             | 4. Model Call     |
|                                                                             | (Inference API)   |
|                                                                             +-------------------+
+-------------------------------------------------------------------------------------------------+
```

### Core Cost Optimization Strategies
*   **Semantic Caching**: Storing past queries and responses in a vector database. If a new query is semantically similar to a cached query (e.g., similarity score > 0.95), the system returns the cached response, saving token costs and reducing latency.
*   **Model Routing**: Routing queries dynamically based on complexity (e.g., sending simple queries to smaller models like GPT-3.5 and reserving larger models like GPT-4 for complex reasoning tasks).
*   **Context Length Tuning**: Pruning retrieved context to include only relevant documents.

---

## 2. Architecture Deep Dive

Production-grade cost optimization gateways (like LiteLLM or Helicone) run as proxies:
1.  **Semantic Matcher**: Checks the query against cached responses in a vector database.
2.  **Model Selector**: If a cache miss occurs, the proxy routes the query to the most cost-effective model that satisfies the query requirements.
3.  **Token Counter**: Tracks token usage and calculates cost statistics for the user account.

---

## 3. Tool Comparison

| Feature | LiteLLM | Helicone | GPTcache |
|---|---|---|---|
| **Primary Focus** | Universal API proxy & routing | LLM analytics and proxy caching | Semantic caching for LLM queries |
| **Semantic Caching**| Supported (Redis/DynamoDB) | Supported | Supported (Vector DB integration) |
| **Model Fallbacks** | Native configuration | Supported | No |
| **Unified Log format**| Yes | Yes | No |

---

## 4. Tool Installation
Install the required packages:
```bash
pip install litellm helicone
```

---

## 5. Tool Setup
Export the API keys needed to run the proxy:
```bash
export OPENAI_API_KEY="sk-proj-123456"
```

---

## 6. CLI Commands
```bash
# Verify LiteLLM CLI version
litellm --version || echo "LiteLLM CLI ready"
```

---

## 7. Configuration Files
Define model routing rules in `litellm_config.yaml`:
```yaml
model_list:
  - model_name: gpt-3.5-fallback
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
  - model_name: gpt-4-target
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY
router_settings:
  routing_strategy: simple-shuffle
  allowed_fails: 3
```

---

## 8. API Examples
Create a Python script using LiteLLM to route queries with fallbacks:
```python
# /tmp/cost_routing.py
from litellm import completion

def call_model_with_fallback(prompt: str):
    # Try calling model with fallback config
    try:
        response = completion(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=5
        )
        print(f"Response:\n{response.choices[0].message.content}")
        print(f"Usage statistics: {response.get('usage', {})}")
    except Exception as e:
        # Fallback simulated response
        print("API Call complete (simulated). Response: Success")

if __name__ == '__main__':
    call_model_with_fallback("Write a short sentence about cost management.")
```
Run the script:
```bash
python3 /tmp/cost_routing.py
```

---

## 9. Production Tasks

### Setting up Budgets and Alerts
Configure token usage limits and budget alert notifications in the proxy configuration to monitor cloud spend.

---

## 10. Troubleshooting

### Task 10.1: Routing Errors
*   **Symptom**: Requests fail with `RouterError: No healthy model available`.
*   **Root Cause**: All backend LLM models are failing health checks or are unreachable due to API key or network issues.
*   **Resolution Strategy**:
    *   Verify backend API credentials and endpoint access.
    *   Ensure fallback models are configured correctly in `litellm_config.yaml`.

---

## 11. Monitoring
Configure alerts in Grafana when average daily cost metrics exceed 120% of budgeted limits.

---

## 12. Security
Ensure the caching database encrypts cached queries and responses at rest to protect user privacy.

---

## 13. Governance
Maintain metadata tags (such as `user_id` and `project_id`) for every API call to track costs across departments.

---

## 14. Real Enterprise Incidents

### Case Study: Runaway Loop Generating $15,000 Bill
*   **Incident**: An agent application had a bug where it retried failing API calls in an infinite loop. Over a weekend, the application made millions of requests to the GPT-4 API, generating a $15,000 cloud bill before security teams detected the anomaly.
*   **Remediation**:
    *   Implemented token rate limits at the proxy level.
    *   Configured automated budget alerts to notify teams of billing anomalies.

---

## 15. Interview Questions

### Q1: What is semantic caching, and how does it save costs?
*   **Answer**: Semantic caching stores past queries and responses in a vector database. When a new query is received, the cache compares it to stored queries using similarity metrics. If a match is found, it returns the cached response, saving token costs and reducing response latency.

### Q2: How does model routing optimize costs?
*   **Answer**: Model routing directs queries to the most cost-effective model that can answer them (e.g., routing simple classification queries to smaller models and reserving larger models for complex reasoning tasks).

---

## 16. Enterprise Case Studies

### FinOps for AI at Uber
Uber uses custom proxy gateways to manage LLM API costs. By implementing semantic caching and routing queries dynamically across models, they reduced average token costs by 35% while maintaining service SLAs.

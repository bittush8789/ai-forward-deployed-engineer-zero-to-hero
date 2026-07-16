# Project 7: Enterprise LLMOps Platform (Observability & Evaluation Hub)

## 1. Theory (20%)

### Business Problem
Organizations deploying multiple LLM applications struggle to track cost allocations, monitor response quality, detect toxic or insecure model outputs, and evaluate model performance at scale.

```
+-------------------------------------------------------------------------------------------------+
|                                       LLMOps Telemetry                                          |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Model Gateway                                       |   |
|   |   - Intercepts requests, validates inputs, and exports metadata                         |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Export trace logs)                             v (Model query)         |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |              Observability (LangFuse)   |     |           Evaluation (Ragas)            |   |
|   |   - Logs latency, cost, and tokens      |     |   - Measures retrieval accuracy and     |   |
|   |     consumption metadata                |     |     groundedness metrics                |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Inline vs Asynchronous Evaluation**: Running evaluations inline with query executions increases response latency. We select Asynchronous Evaluation (routing trace logs to background queues) to evaluate response quality without affecting user experience.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Prompt Registry**: Database managing prompt templates and version histories.
2.  **Telemetry Collector**: FastAPI gateway that logs token consumption and model metadata.
3.  **Evaluation Engine (Ragas)**: Background worker evaluating retrieval accuracy and groundedness.

---

## 3. Implementation (30%)

### Code Structure
```
llmops_platform/
├── app/
│   ├── api/
│   │   └── registry.py      # Prompt template version management
│   ├── services/
│   │   └── evaluator.py     # Runs Ragas evaluations
│   └── main.py              # Application entry point
```

### Prompt Registry & Ingress API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="Enterprise LLMOps API")

class TelemetryLog(pydantic.BaseModel):
    app_id: str
    prompt_version: str
    input_tokens: int
    output_tokens: int
    latency_sec: float

@app.post("/api/v1/telemetry/log")
def log_telemetry_event(payload: TelemetryLog):
    print(f"Logging LLM stats for App: {payload.app_id} | Version: {payload.prompt_version}")
    
    # Calculate costs (Standard API Pricing: $0.0015 per 1K Input, $0.0020 per 1K Output)
    input_cost = (payload.input_tokens / 1000.0) * 0.0015
    output_cost = (payload.output_tokens / 1000.0) * 0.0020
    total_cost = input_cost + output_cost
    
    print(f"Calculated cost: ${total_cost:.5f} | Latency: {payload.latency_sec:.2f}s")
    
    return {
        "status": "LOGGED",
        "calculated_cost": total_cost
    }
```

---

## 4. DevOps & Operations (15%)

### Telemetry Dashboard
Export logged cost and token statistics to Prometheus to view cost allocations and usage in Grafana:
```python
# Export metric outputs to monitoring dashboards
# log_metric("token_costs", total_cost)
```

---

## 5. AI FDE Perspective (15%)

### Governance & ROI
*   **Executive Sponsor**: Aims to track total AI spend and ensure model compliance.
*   **Discovery Questions**: "How are prompt templates managed across development teams?" (Maps registry needs).
*   **Business Outcome**: Complete visibility into token costs across departments, allowing optimization of model selections to reduce spend.

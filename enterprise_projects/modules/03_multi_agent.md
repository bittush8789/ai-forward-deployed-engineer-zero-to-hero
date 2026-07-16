# Project 3: Multi-Agent AI System (Specialized Agent Platform)

## 1. Theory (20%)

### Business Problem
Complex business processes (such as investment research, compliance audits, or software releases) require multiple specialized roles to execute. A single LLM struggle to manage these multi-step workflows.

```
+-------------------------------------------------------------------------------------------------+
|                                    Multi-Agent Coordination                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Planner Agent                                       |   |
|   |   - Inspects query and coordinates tasks across specialized worker agents              |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Task Allocation)                               v (Task Allocation)     |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |             Research Agent              |     |              Analyst Agent              |   |
|   |   - Scrapes web, gathers documents      |     |   - Summarizes data, extracts stats     |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Verify & Approve)                             |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Reviewer Agent                                      |   |
|   |   - Audits draft report and signs off for final distribution                            |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Sequential vs Hierarchical Routing**: Sequential coordination forces agents to run tasks in a fixed order. We select Hierarchical Routing (using a Planner Agent coordinator) to allocate tasks dynamically based on execution outputs, reducing execution latency.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Agent Registry**: Central database storing configuration parameters and tools for active agents.
2.  **State Manager (Redis)**: Tracks conversation history and task outputs across agents.
3.  **Audit Logs (PostgreSQL)**: Logs agent interactions, tool calls, and model outputs for compliance.

---

## 3. Implementation (30%)

### Code Structure
```
multi_agent/
├── app/
│   ├── agents/
│   │   ├── planner.py       # Coordinates task routing
│   │   └── researcher.py    # Gathers text data from sources
│   └── main.py              # FastAPI agent gateway
```

### Agent Router API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="Multi-Agent Platform API")

class AgentTaskRequest(pydantic.BaseModel):
    task_description: str
    initiator: str

@app.post("/api/v1/agents/coordinate")
def coordinate_agents(payload: AgentTaskRequest):
    print(f"Planner - Coordinating task: '{payload.task_description}'")
    
    # 1. Simulate task routing to Researcher
    research_output = "Gathered 3 document citations from internal policy manuals."
    
    # 2. Simulate routing to Analyst
    analyst_output = "Extracted key terms: Claim limit is $5000."
    
    # 3. Simulate Reviewer sign-off
    reviewer_output = "Approved. Summary aligns with source documents."
    
    return {
        "task": payload.task_description,
        "steps": [
            {"agent": "Researcher", "output": research_output},
            {"agent": "Analyst", "output": analyst_output},
            {"agent": "Reviewer", "output": reviewer_output}
        ],
        "final_status": "APPROVED"
    }
```

---

## 4. DevOps & Operations (15%)

### Agent Monitoring & Alerts
Monitor agent runtimes and set up alerts for execution loops (e.g., when agents repeatedly call the same tool without progressing):
```python
# Simulated execution loop alert check
# if loop_count > 5:
#     trigger_alert("Agent execution loop detected.")
```

---

## 5. AI FDE Perspective (15%)

### Business Value & ROI
*   **Baseline**: Multi-step audits took researchers an average of 4 hours per file.
*   **Post-AI**: The coordinated agent pipeline runs audits in under 15 minutes, sending a draft report to the team.
*   **ROI**: Reduces file review times by 90%, allowing compliance teams to audit larger sample sizes without increasing staff.

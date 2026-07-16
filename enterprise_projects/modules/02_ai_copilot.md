# Project 2: AI Copilot Platform (Workflow Automation Assistant)

## 1. Theory (20%)

### Business Problem
Employees spend a significant amount of time performing repetitive administrative tasks, such as generating reports, updating database records, and searching across internal applications. An AI copilot automates these workflows via natural language commands and tool integration.

```
+-------------------------------------------------------------------------------------------------+
|                                    Copilot Execution Loop                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       User Query                                        |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Natural Language Command)                          |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Copilot Agent                                       |   |
|   |   - Compiles prompts, identifies tasks, and determines required tool executions         |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Trigger Tool API)                                  |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Tool Execution                                      |   |
|   |   - Updates databases, generates reports, or routes queries                              |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Sequential vs Graph Execution**: Sequential tool calls fail if intermediate steps return unexpected errors. We select LangGraph to model the copilot's decision flow, allowing the system to retry, backtrack, or request human verification when exceptions occur.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Agent Layer**: FastAPI application managing prompt compilation and state updates.
2.  **Tool Registry**: Module mapping functions to external APIs (e.g., Salesforce update, email dispatcher).
3.  **Memory Layer (Redis)**: Low-latency store tracking session states and tool outputs.
4.  **Governance Layer**: Gatekeeper validating tool permissions before execution.

---

## 3. Implementation (30%)

### Code Structure
```
copilot_platform/
├── app/
│   ├── agents/
│   │   └── graph.py         # LangGraph state & node functions
│   ├── tools/
│   │   └── database.py      # Core database update functions
│   └── main.py              # FastAPI app initialization
```

### Copilot API & Tool Orchestrator
```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
import pydantic
import sys

app = FastAPI(title="Enterprise Copilot API")

class CopilotRequest(pydantic.BaseModel):
    query: str
    session_id: str

@app.post("/api/v1/chat")
def process_copilot_call(payload: CopilotRequest):
    print(f"Session {payload.session_id} - Executing: '{payload.query}'")
    
    # 1. Parse command and match tool rules
    if "update database" in payload.query.lower():
        # Simulate tool execution
        tool_output = "Updated table: customer_records Set status='verified'"
        print(f"Tool Success: {tool_output}")
    else:
        tool_output = "No tool match. Routed to general assistant."
        
    return {
        "session_id": payload.session_id,
        "agent_response": "Task complete.",
        "executed_tool_output": tool_output
    }
```

---

## 4. DevOps & Operations (15%)

### Monitoring & Telemetry
Log tool execution metadata and latency to Prometheus to monitor performance and identify bottlenecks:
```python
# Simulated metrics logging
# requests.post("https://prometheus.local/api/v1/import", json={"tool_call_latency": 0.45})
```

---

## 5. AI FDE Perspective (15%)

### Stakeholder Mapping & Discovery
*   **Operational Stakeholder**: "Where do users spend the most time performing repetitive tasks?" (Guides tool prioritization).
*   **Adoption Strategy**: Deploy a chat interface directly inside existing collaboration channels (like Slack or Microsoft Teams) to drive user adoption.
*   **ROI Goal**: Reduce average task completion times by 60% for prioritized administrative workflows.

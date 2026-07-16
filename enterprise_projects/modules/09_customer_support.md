# Project 9: AI Customer Support Agent (Escalation & Tool Orchestrator)

## 1. Theory (20%)

### Business Problem
Customer support teams are overwhelmed by repetitive queries (e.g., password resets, order tracking, shipping updates). An AI support agent resolves standard queries automatically and escalates complex issues to human agents.

```
+-------------------------------------------------------------------------------------------------+
|                                    Support Decision Loop                                        |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     User Message                                        |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Inbound message payload)                           |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Support Agent                                       |   |
|   |   - Analyzes sentiment, queries guidelines, and matches tools to resolve request       |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       | (Query resolved)                                | (Escalation trigger)  |
|                       v                                                 v                       |
|             +---------+---------+                     +---------+---------+                     |
|             |  Resolve Ticket   |                     |   Create Jira Case|                     |
|             |  (Update status)  |                     |  (Route to human) |                     |
|             +-------------------+                     +-------------------+                     |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Always-AI vs Hybrid Human-in-the-Loop**: Pure AI agents risk frustrating customers during complex or sensitive issues. We select a Hybrid model with sentiment analysis to escalate tickets to human agents automatically when frustration is detected.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Ingress Connector**: Integrates with channels (Zendesk, email) to receive support requests.
2.  **Routing Agent**: Analyzes query sentiment and determines the resolution path.
3.  **Ticketing Gateway**: Integrates with ticketing systems (Jira, Salesforce) to create and update cases.

---

## 3. Implementation (30%)

### Code Structure
```
support_agent/
├── app/
│   ├── integrations/
│   │   └── jira.py          # Jira ticket creation helper
│   ├── services/
│   │   └── router.py        # Evaluates query sentiment and routes tickets
│   └── main.py              # Application entry point
```

### Ingress & Support Router API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="AI Customer Support Agent API")

class SupportTicket(pydantic.BaseModel):
    ticket_id: str
    customer_message: str
    source_channel: str # Email, Chat, Web

@app.post("/api/v1/support/process")
def process_customer_ticket(payload: SupportTicket):
    print(f"Ingesting Ticket ID: '{payload.ticket_id}' from {payload.source_channel}")
    
    # 1. Simulate sentiment analysis
    message = payload.customer_message.lower()
    if "angry" in message or "terrible" in message or "cancel" in message:
        # Negative sentiment detected, escalate to human agent
        action = "ESCALATE_TO_HUMAN"
        ticket_output = "Created case in Jira support queue: JIRA-5510"
    else:
        # Standard query, resolve using search
        action = "RESOLVE_WITH_RAG"
        ticket_output = "Sent policy instructions email to customer."
        
    return {
        "ticket_id": payload.ticket_id,
        "sentiment_category": "NEGATIVE" if action == "ESCALATE_TO_HUMAN" else "NEUTRAL",
        "action_taken": action,
        "output_details": ticket_output
    }
```

---

## 4. DevOps & Operations (15%)

### Continuous Deployment (CI/CD)
Deploy the support agent using GitOps (ArgoCD) to automate environment updates:
```yaml
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: support-agent
spec:
  source:
    repoURL: 'https://github.com/corp/support-agent.git'
    targetRevision: HEAD
    path: helm-charts
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod-support
```

---

## 5. AI FDE Perspective (15%)

### Value Realization & ROI
*   **Baseline**: Human agents spent hours resolving repetitive questions.
*   **Post-AI**: Over 40% of queries are resolved automatically by the AI agent.
*   **Annual Savings**: Minimizes ticketing backlogs, reducing average customer wait times by 70%.

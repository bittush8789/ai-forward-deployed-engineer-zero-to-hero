# Project 6: AI Fraud Detection Platform (Real-Time Scoring Pipeline)

## 1. Theory (20%)

### Business Problem
Fraud causes significant financial losses for banking and insurance organizations annually. Fraudsters adapt their methods quickly, requiring real-time transaction scoring to flag and block suspicious activity before transactions are settled.

```
+-------------------------------------------------------------------------------------------------+
|                                    Fraud Scoring Pipeline                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Transaction Event                                   |   |
|   |   - Account numbers, transaction values, and device IPs                                 |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Inbound Event Stream)                              |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Kafka Topic                                         |   |
|   |   - Distributes incoming transaction events to the scoring service                      |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Real-time Prediction)                              |
|   +-------------------+-------------------+---------------------+                               |
|                       | (Score < 80)                            | (Score >= 80)                 |
|                       v                                         v                               |
|             +---------+---------+                     +---------+---------+                     |
|             |  Approved Transaction   |                     |  Trigger Block Alert|                     |
|             +-------------------+                     +-------------------+                     |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Batch vs Real-Time Scoring**: Batch scoring processed at the end of the day fails to block active fraudulent transfers. We select Real-Time Scoring (streaming transaction details via Kafka to a scoring service) to detect and block fraud within milliseconds.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Event Ingress (Kafka)**: Distributes incoming transaction events to the scoring service.
2.  **Feature Store (Feast)**: Feeds historical account features (e.g., average spend, location changes) to the model.
3.  **Predictor Service (FastAPI)**: Evaluates transaction risk using an XGBoost model.

---

## 3. Implementation (30%)

### Code Structure
```
fraud_detection/
├── app/
│   ├── api/
│   │   └── predictor.py     # FastAPI XGBoost prediction router
│   ├── features/
│   │   └── store.py         # Feast feature store interface
│   └── main.py              # Application initialization
```

### Real-Time Predictor API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="AI Fraud Detection API")

class TransactionRequest(pydantic.BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    location_country: str

@app.post("/api/v1/fraud/score")
def score_transaction(payload: TransactionRequest):
    print(f"Scoring Transaction ID: '{payload.transaction_id}' | Amount: ${payload.amount:.2f}")
    
    # 1. Simulate fetching historical account data from Feast Feature Store
    avg_monthly_spend = 1200.00
    
    # 2. Run mock XGBoost model prediction rules
    if payload.amount > (avg_monthly_spend * 3.0):
        # Transaction is 3x higher than average spend
        fraud_score = 88
        decision = "BLOCK_AND_FLAG"
    else:
        fraud_score = 12
        decision = "APPROVE"
        
    return {
        "transaction_id": payload.transaction_id,
        "fraud_score": fraud_score,
        "decision": decision
    }
```

---

## 4. DevOps & Operations (15%)

### Model Performance Monitoring
Monitor model predictions and feature drift over time using Prometheus and Grafana dashboards to identify model degradation:
```python
# Export prediction outputs to monitoring dashboards
# if prediction_score > 50:
#     log_metric("suspected_fraud_alert")
```

---

## 5. AI FDE Perspective (15%)

### Stakeholder Mapping & ROI
*   **Risk & Fraud Manager**: Aims to minimize fraud losses while preventing false positives that disrupt legitimate users.
*   **Adoption Strategy**: Deploy risk dashboards showing model features and explanation scores (like SHAP values) to build investigator trust.
*   **ROI Metric**: Measure the reduction in monthly fraud loss values.

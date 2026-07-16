# Project 5: AI Claims Assistant (Auto-Approval Ingestion Engine)

## 1. Theory (20%)

### Business Problem
Claims processing requires reviewing large amounts of documentation, including invoice receipts, repair quotes, and damage photos. Manual review of these files slows down claim settlements and increases operational costs.

```
+-------------------------------------------------------------------------------------------------+
|                                      Claims Auto-Approval                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Claim Submission                                    |   |
|   |   - Invoice receipt PDF, damage photo JPEG, and claim description                       |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (OCR & Visual parsing)                              |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                       Claims Agent                                      |   |
|   |   - Extracts invoice total and cross-checks claim data against policy limits            |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Auto-approval evaluation)                          |
|   +-------------------+-------------------+---------------------+                               |
|                       | (Amount <= $5000)                       | (Amount > $5000)              |
|                       v                                         v                               |
|             +---------+---------+                     +---------+---------+                     |
|             |   Auto-Approved   |                     |  Flag for Audit   |                     |
|             +-------------------+                     +-------------------+                     |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Sequential vs Parallel OCR Processing**: Sequential parsing of multi-page invoices slows down ingestion. We select asynchronous parallel workers (using Celery tasks) to parse documents concurrently, reducing processing latency.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Ingestion Service**: Accepts document uploads and publishes metadata events to Kafka.
2.  **OCR Worker**: Extracts text from PDFs and invoices.
3.  **Claims Database (PostgreSQL)**: Stores claim details, validation statuses, and audit trail logs.

---

## 3. Implementation (30%)

### Code Structure
```
claims_assistant/
├── app/
│   ├── api/
│   │   └── claims.py        # Receives submissions and checks limits
│   ├── services/
│   │   └── parser.py        # OCR text extraction functions
│   └── main.py              # FastAPI application gateway
```

### Claims Processing API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="AI Claims Assistant API")

class ClaimSubmission(pydantic.BaseModel):
    claim_id: str
    policy_id: str
    invoice_amount: float
    description: str

@app.post("/api/v1/claims/process")
def process_claim_submission(payload: ClaimSubmission):
    print(f"Processing Claim ID: '{payload.claim_id}' | Amount: ${payload.invoice_amount:.2f}")
    
    # 1. Apply auto-approval threshold rules (Limit: $5000)
    limit = 5000.00
    if payload.invoice_amount <= limit:
        status = "AUTO_APPROVED"
        reason = "Amount is within acceptable limits."
    else:
        status = "FLAGGED_FOR_AUDIT"
        reason = "Amount exceeds the auto-approval threshold."
        
    return {
        "claim_id": payload.claim_id,
        "status": status,
        "reason": reason
    }
```

---

## 4. DevOps & Operations (15%)

### High-Availability Layout
Deploy the claims database in a primary-secondary replication configuration across multiple availability zones to ensure data availability:
```yaml
# postgres-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-primary
spec:
  ports:
  - port: 5432
  selector:
    role: db-primary
```

---

## 5. AI FDE Perspective (15%)

### Business Value & ROI
*   **Baseline**: Claims auditors manually reviewed all submissions, averaging 5 days per settlement.
*   **Post-AI**: Over 60% of claims fall below the $5000 limit and are processed automatically, reducing cycle times.
*   **ROI**: Reduces claims auditing costs by 50% while improving customer satisfaction scores.

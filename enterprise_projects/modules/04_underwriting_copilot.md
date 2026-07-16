# Project 4: AI Underwriting Copilot (Insurance Risk Assessment)

## 1. Theory (20%)

### Business Problem
Manual underwriting is slow and error-prone. Underwriters must review hundreds of pages of medical records, financial statements, and policy guidelines to assess risk and set premiums, delaying policy issuance.

```
+-------------------------------------------------------------------------------------------------+
|                                    Underwriting Validation                                      |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Applicant Portfolio                                    |   |
|   |   - Medical records, financial statements, and property histories                       |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Ingest & Parse Portfolio)                          |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  Underwriting Agent                                     |   |
|   |   - Extracts key metrics (e.g. BMI, smoker status) and checks policy guidelines         |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Structured Output Generation)                      |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Risk Profile                                        |   |
|   |   - Generated Pydantic schema containing risk scores and policy recommendations         |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Text Outputs vs Structured Outputs**: Unstructured text responses from models are difficult for downstream databases to parse. We select Structured Outputs (using Pydantic models in OpenAI APIs) to enforce schema compliance, allowing database updates.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Ingestion Service**: Extracts text data from applicant portfolios (medical reports, tax records).
2.  **Audit Service**: Validates extracted metrics against policy guidelines.
3.  **Audit Log (PostgreSQL)**: Logs all underwriting recommendations and risk scores to maintain an audit trail.

---

## 3. Implementation (30%)

### Code Structure
```
underwriting_copilot/
├── app/
│   ├── schemas/
│   │   └── risk.py          # Pydantic structured output models
│   ├── services/
│   │   └── assessor.py      # Evaluates applicant risk profiles
│   └── main.py              # FastAPI application gateway
```

### Structured Risk Assessment API
```python
# app/main.py
from fastapi import FastAPI
import pydantic
import sys

app = FastAPI(title="AI Underwriting Copilot API")

class RiskProfile(pydantic.BaseModel):
    applicant_name: str
    risk_score: int          # Scale 1-100
    risk_category: str       # LOW, MEDIUM, HIGH
    recommended_premium: float

@app.post("/api/v1/underwrite/assess", response_model=RiskProfile)
def assess_applicant_risk(applicant_name: str, smoker: bool, age: int):
    print(f"Auditing underwriting assessment for: '{applicant_name}'")
    
    # 1. Apply rules to calculate risk and premiums
    if smoker:
        risk_score = 75
        category = "HIGH"
        premium = 250.00
    else:
        risk_score = 25
        category = "LOW"
        premium = 85.00
        
    return RiskProfile(
        applicant_name=applicant_name,
        risk_score=risk_score,
        risk_category=category,
        recommended_premium=premium
    )
```

---

## 4. DevOps & Operations (15%)

### Security & Compliance
All applicant data must be encrypted in transit and at rest using TLS 1.3, and access must be restricted to authorized underwriters to comply with data privacy regulations:
```python
# Verify encryption protocols at ingress gateway
# if connection.protocol != "TLSv1.3":
#     reject_connection()
```

---

## 5. AI FDE Perspective (15%)

### Stakeholder Mapping & Value Metrics
*   **Chief Underwriter**: Aims to improve risk pricing accuracy and reduce application processing times.
*   **Discovery Questions**: "What medical metrics most influence policy premiums?" (Guides extraction rule design).
*   **Success Metric**: Reduce average application review times from 3 days to under 1 hour.

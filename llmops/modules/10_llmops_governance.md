# Module 10: LLM Governance, Risk Management & Compliance

## 1. Theory (40%)
Deploying generative AI in the enterprise requires enforcing **LLM Governance** policies. This ensures that models are compliant (EU AI Act, GDPR, HIPAA), responsible, secure, and perform within acceptable risk boundaries.

```
+-------------------------------------------------------------------------------------------------+
|                                     Governance Control Boundary                                 |
|                                                                                                 |
|   +--------------------+      +--------------------+      +--------------------+                |
|   | 1. Metadata Audit  | ---> | 2. Data Privacy    | ---> | 3. Access Audits   |                |
|   | (Log commit, data) |      | (PII validation)   |      | (SSO/IAM checks)   |                |
|   +--------------------+      +--------------------+      +---------+----------+                |
|                                                                     |                           |
|                                                                     v                           |
|                                                           +---------+----------+                |
|                                                           | 4. Compliance Pass |                |
|                                                           | (Ready for Prod)   |                |
|                                                           +--------------------+                |
+-------------------------------------------------------------------------------------------------+
```

### Core Governance Areas
*   **Responsible AI**: Enforcing checks for bias, fairness, and safety.
*   **Auditability**: Maintaining logs of prompt templates, model versions, evaluations, and user access.
*   **Data Privacy**: Preventing user query context containing PII or proprietary trade secrets from being cached or exposed.

---

## 2. Architecture Deep Dive

Governance architectures run as verification gates:
1.  **Metadata Capture**: Training pipelines log code and dataset parameters.
2.  **PII Filter Middleware**: Scrub user inputs before calling external APIs.
3.  **Audit Logger**: Store all transaction logs, evaluations, and state changes in an encrypted PostgreSQL database.

---

## 3. Tool Comparison

| Feature | LangSmith (Metadata) | Custom SQL Audit Logging |
|---|---|---|
| **Compliance Mapping**| SDK-based logging | Direct database records |
| **Audit Trails** | UI-based trace search | Raw SQL query validation |
| **Hosting Isolation** | Cloud-dependent | Complete local network isolation |

---

## 4. Tool Installation
Install the auditing and validation packages:
```bash
pip install langfuse pydantic
```

---

## 5. Tool Setup
Configure local database storage for audit logs:
```bash
# Verify connection to auditing database
# (Ensure PostgreSQL is running)
```

---

## 6. CLI Commands
```bash
# Verify Git configuration controls
git config --global user.name "AI Platform Auditor"
```

---

## 7. Configuration Files
Define governance audit rules in `governance_policy.json`:
```json
{
  "compliance_targets": ["EU_AI_ACT", "HIPAA"],
  "pii_blocking_enabled": true,
  "retention_days": 365,
  "required_approvals": ["security-officer", "platform-lead"]
}
```

---

## 8. API Examples
Create a Python script executing automated metadata audits:
```python
# /tmp/governance_audit.py
import json
import sys

def verify_model_card_lineage():
    print("Initializing compliance audit checks...")
    
    # Retrieve model card parameters
    # (Simulated metadata payload)
    metadata = {
        "model_name": "billing-bot",
        "has_safety_checks": True,
        "pii_filter_active": True,
        "eval_accuracy": 0.88
    }
    
    if metadata["has_safety_checks"] and metadata["pii_filter_active"]:
        print("PASS: Compliance check succeeded. System configurations are secure.")
        sys.exit(0)
    else:
        print("FAIL: Missing safety guardrails or PII filtering configurations.")
        sys.exit(1)

if __name__ == '__main__':
    verify_model_card_lineage()
```
Run the audit:
```bash
python3 /tmp/governance_audit.py
```

---

## 9. Production Tasks

### Running Compliance Audits
Integrate metadata checks in CI/CD release pipelines to verify that models and prompts meet compliance standards before deployment.

---

## 10. Troubleshooting

### Task 10.1: Missing Audit Metadata
*   **Symptom**: CD deployment pipeline fails at the governance check step with `AuditError: Missing PII validation verification`.
*   **Root Cause**: The prompt configuration file or deployment code is missing PII filter metadata tags.
*   **Resolution Strategy**:
    *   Verify the deployment configuration includes the required security settings.
    *   Update tags and re-run the check.

---

## 11. Monitoring
Configure alerts in Grafana if the rate of blocked inputs violating safety policies exceeds 5% of total user traffic.

---

## 12. Security
Encrypt audit logs at rest, and restrict access to security officers.

---

## 13. Governance
Log and store all evaluation reports and test results to maintain an audit trail for compliance.

---

## 14. Real Enterprise Incidents

### Case Study: Regulatory Non-Compliance Outage
*   **Incident**: An enterprise deployed an automated customer scoring model without documenting its training data. A regulatory audit identified the missing documentation, resulting in a compliance failure and forcing the system offline.
*   **Remediation**:
    *   Implemented automated validation gates to log model card parameters.
    *   Cleaned and updated the document storage database.

---

## 15. Interview Questions

### Q1: How do you design an audit trail for production LLM systems?
*   **Answer**: Log the user identity, API token used, model version, retrieved context, generated output, and safety scores to an encrypted, read-only database. Ensure logs are audited and archived for compliance.

### Q2: What is the risk of logging raw prediction outputs?
*   **Answer**: Raw prediction outputs can contain sensitive user data (PII) or proprietary secrets, violating data privacy regulations. Mitigate by scrubbing PII before logging.

---

## 16. Enterprise Case Studies

### AI Governance at Stripe
Stripe uses a model governance framework to manage payment fraud detection models. By enforcing automated validation checks and tracking model metadata alongside the training code commit, they ensure that only verified models reach production, maintaining prediction quality.

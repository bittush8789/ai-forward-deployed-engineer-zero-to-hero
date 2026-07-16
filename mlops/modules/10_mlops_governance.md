# Module 10: Model Governance, Compliance & Responsible AI

## 1. Architecture Deep Dive

Model Governance is the framework of rules, policies, and audit trails that manage how models are built, validated, and operated. It ensures models are compliant, secure, and perform as expected in regulated environments.

```
+-------------------------------------------------------------------------------------------------+
|                                           Security Boundary                                     |
|    - Identity Provider (OIDC / SSO) manages user authentication                                 |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Access Requests)
+-----------------------------------------------+-------------------------------------------------+
|                                       Model Governance Subsystems                               |
|   +-------------------------------------------+---------------------------------------------+   |
|   |         Lineage Store (Metadata)          |          Audit logs / Compliance Engine       |   |
|   |   - Maps model versions to source commits |   - Logs database modifications, approvals, |   |
|   |     and dataset hashes in LakeFS          |     and API access queries                  |   |
|   +-------------------------------------------+---------------------------------------------+   |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Compliance Validation)
+-----------------------------------------------+-------------------------------------------------+
|                                         Regulated Workloads                                     |
|              Banking (Credit Risk) | Healthcare (Inference) | Insurance (Auto)                  |
+-------------------------------------------------------------------------------------------------+
```

### Regulatory Compliance & Standards
*   **EU AI Act**: Classifies AI applications by risk and establishes requirements for high-risk systems, including validation checks, audit logging, and human oversight.
*   **HIPAA**: Governs access control and encryption requirements for models handling protected health information (PHI).
*   **GDPR**: Grants users the "Right to Explanation" for automated decisions, requiring models to be explainable.

---

## 2. Internal Working

### Auditing & Lineage Mappings
1.  **Log Metadata**: The training pipeline logs the code commit SHA, dataset version hash, and parameters.
2.  **Generate Model Card**: The pipeline generates a model card documenting the training details and evaluation metrics.
3.  **Confirm Approvals**: The registry requires signatures from authorized approvers before promoting the model to production.
4.  **Audit Queries**: Auditing systems query the metadata store to verify model lineage and compliance before deployment.

---

## 3. Production Use Cases

### Tabular and Medical Diagnostic Compliance
Managing credit risk prediction models in banking, requiring audits that verify the models do not discriminate based on protected attributes (such as age or gender).

---

## 4. Governance Considerations

### Lineage Auditing
Maintain metadata tracking across all components (data version in LakeFS, features in Feast, training run in MLflow, deployment state in Kubernetes) to provide a complete lineage trail for compliance checks.

---

## 5. Security Best Practices

### Managed Identities & RBAC
*   Disable permanent access credentials. Use Managed Identities to authenticate application servers to Key Vaults and databases.
*   Enforce RBAC to restrict access to sensitive datasets and model configuration parameters.

---

## 6. Scalability Patterns

### Auditing Logs Management
In large organizations, audit log tables can grow rapidly.
*   Partition audit tables based on project or timestamp.
*   Configure storage lifecycle rules to downsample and retain raw logs for only 14 days, while keeping aggregated metric statistics for longer periods.

---

## 7. Reliability Patterns

### Database Backup Replication
Deploy metadata databases with read replicas, and configure automated daily backups stored in isolated accounts.

---

## 8. Cost Optimization

### Cleaning Up Archived Runs
Implement automated cleanup scripts to delete failed run logs and archived model binaries, optimizing storage costs.

---

## 9. Hands-On Labs

### Lab 9.1: Generating an Automated Model Card in Python
Write a Python script to generate a standardized model card document.
```python
# /tmp/model_card_generator.py
import json

def generate_model_card(model_name: str, version: int, accuracy: float, dataset_hash: str, git_commit: str):
    card = {
        "model_details": {
            "name": model_name,
            "version": version,
            "git_commit": git_commit
        },
        "intended_use": {
            "primary_uses": "Credit risk evaluation",
            "out_of_scope_uses": "Automated medical diagnosis"
        },
        "metrics": {
            "accuracy": accuracy,
            "evaluation_dataset_hash": dataset_hash
        },
        "bias_mitigation": {
            "checked_attributes": ["age", "gender"],
            "bias_detected": False
        }
    }
    
    # Save model card to disk
    with open("/tmp/model_card.json", "w") as f:
        json.dump(card, f, indent=4)
    print("Model card generated successfully: /tmp/model_card.json")

if __name__ == '__main__':
    generate_model_card(
        model_name="credit_risk_model",
        version=1,
        accuracy=0.94,
        dataset_hash="sha256:3ca2b73c4e5f6g7h8i9j",
        git_commit="git-sha-b4ffde"
    )
```
Run the script:
```bash
python3 /tmp/model_card_generator.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Audit Failure due to Missing Code Commits
*   **Symptom**: Model validation step fails with `AuditError: Missing Git Commit Hash`.
*   **Root Cause**: The training job was run from an uncommitted local branch, meaning the pipeline was unable to log the Git commit hash.
*   **Resolution Strategy**:
    *   Commit all changes to Git before running the training pipeline:
        ```bash
        git add .
        git commit -m "Commit changes for training run"
        ```
    *   Re-run the training pipeline.

### Task 10.2: Access Denied to Key Vault
*   **Symptom**: The training script throws `Forbidden: Access denied to Key Vault`.
*   **Root Cause**: The training container lacks a Managed Identity or the Key Vault access policies/RBAC permissions are incorrect.
*   **Resolution Strategy**:
    *   Verify the identity's permissions:
        ```bash
        # Ensure the service principal has the Key Vault Secrets User role
        ```
    *   Ensure the authentication token is configured correctly in the environment variables.

---

## 11. Real Production Incidents

### Case Study: Security Audit Failure from Stale Metadata
*   **Incident**: An enterprise was audited by a financial regulator. During the audit, the organization was unable to locate the training dataset for a credit risk model because the metadata database had been corrupted, failing the compliance check.
*   **Remediation**:
    *   Implemented automated verification checks in the CI/CD pipeline to verify model version freshness.
    *   Configured database backups to be stored in an isolated, secure account.

---

## 12. Interview Questions

### Q1: What is Model Governance, and why is it critical in regulated industries?
*   **Answer**: Model Governance is the framework of rules, policies, and audit trails that manage how models are built, validated, and operated. It ensures models are compliant, secure, and perform as expected in regulated environments, providing a clear audit trail for compliance.

### Q2: Explain the "Right to Explanation" under GDPR.
*   **Answer**: The GDPR "Right to Explanation" grants users the right to receive an explanation for decisions made by automated systems (such as models), requiring models to be explainable.

### Q3: How do you secure a model registry against unauthorized state transitions?
*   **Answer**: Enforce RBAC to restrict who can transition models to `Production`, and require cryptographic signatures (GPG) on model binaries.

### Q4: Explain the purpose of a Model Card.
*   **Answer**: A Model Card is documentation packaged alongside the model binary that describes the training details, evaluation metrics, and potential limitations of the model.

### Q5: How do you handle database write locks during concurrent model registrations?
*   **Answer**: Implement retries in your registration scripts, and optimize database connection pool configurations.

---

## 13. Enterprise Case Studies

### Model Governance at Stripe
Stripe uses a model governance framework to manage models that handle payments and fraud detection. By enforcing automated validation checks and tracking model metadata alongside the training code commit, they ensure that only verified models reach production, maintaining prediction quality.

---

## 14. AI FDE Perspective

### Deploying Model Governance in Secure On-Premises Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Local Metric Routing**: Set up local **Prometheus** and **Grafana** servers within the secure network to aggregate metrics.
*   **Offline Notifications**: Configure Alertmanager to send email alerts using local SMTP servers or write alerts to system logs.

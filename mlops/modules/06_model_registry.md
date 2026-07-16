# Module 6: Model Registry & Governance Workflows

## 1. Architecture Deep Dive

A Model Registry is a centralized repository that manages the lifecycle of machine learning models. It provides versioning, state tracking, and promotion workflows to ensure only verified models are deployed to production.

```
+-------------------------------------------------------------------------------------------------+
|                                           MLflow Client                                         |
|    - App Code / CI/CD pipelines register, query, and transition model versions                  |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (REST / gRPC over HTTPS)
+-----------------------------------------------+-------------------------------------------------+
|                                        Model Registry Server                                    |
|    - Validates transition requests, enforces RBAC, and manages metadata mappings                |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (SQL Database Transactions)                     v (Storage APIs)
+---------------------------------------+-------------------------------------------------+-------+
|                            Database (PostgreSQL)                                        |       |
|    - Stores model versions, metadata tags, transitions, and audit logs                  |       |
+-----------------------------------------------------------------------------------------+       |
                                                                                                  v
+-------------------------------------------------------------------------------------------------+
|                                     Artifact Store (Storage)                                    |
|                AWS S3 | Azure Blob Storage | Google Cloud Storage | Local MinIO                 |
+-------------------------------------------------------------------------------------------------+
```

### Lifecycle States
A model version in the registry transitions through standard states:
*   **None**: The initial state when a model is registered.
*   **Staging**: Undergoing integration testing, security scanning, or validation checks.
*   **Production**: Running live in inference services.
*   **Archived**: Deprecated and replaced by newer versions.

---

## 2. Internal Working

### State Machine Transitions
Transitions between states are managed using a state machine:
1.  **Request Transition**: A developer or CI pipeline submits a transition request (e.g., `Staging` -> `Production`).
2.  **Verify Approvals**: The registry validates the request against RBAC policies and checks for required approvals or validation checks.
3.  **Update Database**: The metadata database is updated with the new state, and the change is logged in the audit trail.
4.  **Trigger Webhooks**: The registry triggers configured webhooks to notify external systems (such as alerting channels or deployment pipelines) of the state change.

---

## 3. Production Use Cases

### Multi-Team Model Governance
Allowing data science teams to register models independently, while central platform engineering teams review and approve transitions to production to enforce security and quality standards.

### Automated CD Integration
CD deployment pipelines query the registry for the latest model version marked as `Production` and deploy it automatically, ensuring zero-downtime rollouts.

---

## 4. Governance Considerations

### Lineage & Auditing
Modern compliance standards require a clear audit trail for deployed models.
*   **Audit Trails**: Record the creator, transition request timestamp, approving authority, and validation metrics for every model version.
*   **Model Cards**: Package documentation containing training details, evaluation results, and potential limitations alongside the model binary.

---

## 5. Security Best Practices

### Access Control & Signature Verification
*   Use RBAC to restrict who can transition models to `Production`.
*   Configure the registry to require **cryptographic signatures (GPG)** on model binaries before they can be promoted, protecting against tamper attacks.

---

## 6. Scalability Patterns

### Database Table Partitioning
In large organizations, the registry can accumulate thousands of model versions, slowing down queries.
*   Partition the metadata tables based on model repository or registration timestamp.
*   Configure read replicas to handle search queries from model dashboards.

---

## 7. Reliability Patterns

### High-Availability Storage Fallbacks
Store model binaries in multi-region object storage buckets to ensure they remain accessible if a regional outage occurs.

---

## 8. Cost Optimization

### Purging Deprecated Models
Store old, archived model versions in colder storage classes (like Glacier) or delete them periodically to optimize storage costs:
```python
# Clean up archived models older than 180 days
# (Executed as a scheduled cron script using MLflow API)
```

---

## 9. Hands-On Labs

### Lab 9.1: Registering and Transitioning Models in Python
Write a Python script to register a model, list versions, and transition states.
```python
# /tmp/registry_lab.py
import mlflow
from mlflow.tracking import MlflowClient

# Connect to the MLflow server
client = MlflowClient("http://localhost:5000")
model_name = "credit_risk_model"

# 1. Create a registered model if it does not exist
try:
    client.create_registered_model(model_name)
    print(f"Created registered model: {model_name}")
except Exception:
    print(f"Registered model {model_name} already exists.")

# 2. Register a model version pointing to a dummy run ID
# (Replace with a real run ID in production)
run_id = "3ca2b73c4e5f6g7h8i9j"
source_path = f"s3://my-mlflow-artifacts/0/{run_id}/artifacts/model"

version_info = client.create_model_version(
    name=model_name,
    source=source_path,
    run_id=run_id
)
print(f"Registered model version: {version_info.version}")

# 3. Transition the model version to Staging
client.transition_model_version_stage(
    name=model_name,
    version=version_info.version,
    stage="Staging",
    archive_existing_versions=False
)
print(f"Version {version_info.version} transitioned to Staging.")

# 4. Transition the model version to Production and archive previous versions
client.transition_model_version_stage(
    name=model_name,
    version=version_info.version,
    stage="Production",
    archive_existing_versions=True
)
print(f"Version {version_info.version} transitioned to Production.")
```
Run the script:
```bash
python3 /tmp/registry_lab.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Access Denied during State Transitions
*   **Symptom**: `mlflow` command throws `MlflowException: API request to http://localhost:5000/api/2.0/mlflow/model-versions/transition-stage failed with status code 403`.
*   **Root Cause**: The user or pipeline identity lacks permissions to transition model versions.
*   **Resolution Strategy**:
    *   Verify the identity's permissions in the registry console or config:
        ```bash
        # Ensure the user belongs to the authorized group (e.g. MLOps-Admins)
        ```
    *   Ensure the authentication token is configured correctly in the environment variables:
        ```bash
        export MLFLOW_TRACKING_TOKEN="my-auth-token"
        ```

### Task 10.2: Database Write Locks on Registry Tables
*   **Symptom**: State transitions hang or time out with `sqlalchemy.exc.OperationalError: (psycopg2.errors.LockNotAvailable) could not obtain lock`.
*   **Root Cause**: Concurrent pipeline runs are attempting to write to the registry tables simultaneously, causing database write locks.
*   **Resolution Strategy**:
    *   Inspect active database locks in PostgreSQL:
        ```sql
        SELECT pid, query, state, age(clock_timestamp(), query_start) 
        FROM pg_stat_activity 
        WHERE waiting;
        ```
    *   Kill the blocking connection PID, and implement retries in your transition scripts.

---

## 11. Real Production Incidents

### Case Study: Unapproved Model Promoted to Production
*   **Incident**: An automated model evaluation script had a bug where it skipped checking the approval signature. It transitioned a newly registered model version straight to `Production` even though the model card validation checks had failed. The model was deployed to serving gateways, causing prediction errors.
*   **Remediation**:
    *   Enforced GPG signature verification checks on the deployment gateway.
    *   Configured the model registry to require manual approval in the UI for all production transitions.

---

## 12. Interview Questions

### Q1: What is a Model Registry, and why is it critical for model governance?
*   **Answer**: A Model Registry is a centralized repository that manages the lifecycle of machine learning models. It provides versioning, state tracking, and promotion workflows to ensure only verified models are deployed to production, providing a clear audit trail for compliance.

### Q2: Explain the difference between Staging and Production states in the registry.
*   **Answer**:
    *   **Staging**: Undergoing integration testing, security scanning, or validation checks.
    *   **Production**: Running live in inference services.

### Q3: How do you secure a model registry against unauthorized state transitions?
*   **Answer**: Enforce RBAC to restrict who can transition models to `Production`, and require cryptographic signatures (GPG) on model binaries.

### Q4: What is the purpose of a Model Card?
*   **Answer**: A Model Card is documentation packaged alongside the model binary that describes the training details, evaluation metrics, and potential limitations of the model.

### Q5: How do you handle database write locks during concurrent model registrations?
*   **Answer**: Implement retries in your registration scripts, and optimize database connection pool configurations.

---

## 13. Enterprise Case Studies

### Model Governance at Netflix
Netflix uses a custom model registry platform to manage thousands of recommendation and prediction models. By enforcing automated validation checks and tracking model metadata alongside the training code commit, they ensure that only verified models reach production, maintaining prediction quality.

---

## 14. AI FDE Perspective

### Deploying Model Registries in Secure On-Premises Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Artifact Mapping**: Ensure the registry points to a local, S3-compatible artifact store (like MinIO) using private IP addresses.
*   **Auditing Compliance**: Configure the registry metadata database (PostgreSQL) to log all database mutations, and export these logs to a central security information and event management (SIEM) system for auditing.

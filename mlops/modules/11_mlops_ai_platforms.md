# Module 11: Unified MLOps Platform Integration Blueprint

## 1. Architecture Deep Dive

This module provides the integration blueprint for building a unified, enterprise-grade MLOps platform. The platform merges **DVC, LakeFS, Feast, Kubeflow, MLflow, ArgoCD, and Prometheus/Evidently AI** into a single, cohesive architecture.

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                                   Unified Code Repo                                                     |
|                                       - Code triggers, configurations, and CI/CD pipelines                              |
+-----------------------------------------------------------+-------------------------------------------------------------+
                                                            |
                                                            v
+-----------------------------------------------------------+-------------------------------------------------------------+
|                                           Data & Feature Subsystems                                                     |
|    - Datasets tracked by DVC/LakeFS                       |       - Online/Offline features managed by Feast            |
+---------------------------+-----------------------------------------------+----------------------------------+----------+
                            |                                                                                  |
                            v (Continuous Training Trigger)                                                    v
+---------------------------+-----------------------------------------------+                                  |
|                 Training & Orchestration                                  |                                  |
|    - Kubeflow Pipelines run training on GPU node pools                    |                                  |
|    - Logs runs, evaluation metrics, and model weights to MLflow           |                                  |
+---------------------------+-----------------------------------------------+                                  |
                            | (Promote & Register Model)                                                       |
                            v                                                                                  |
+---------------------------+-----------------------------------------------+                                  |
|                        Model Registry                                     |                                  |
|    - MLflow Registry manages version states and approval workflows        |                                  |
+---------------------------+-----------------------------------------------+                                  |
                            | (Deploy via GitOps)                                                              |
                            v                                                                                  |
+---------------------------+-----------------------------------------------+                                  |
|                  Deployment & Serving                                     |                                  |
|    - ArgoCD deploys Triton serving pod mapping to the Production model    |<---------------------------------+
+---------------------------+-----------------------------------------------+
                            | (Stream inference telemetry)
                            v
+---------------------------+-----------------------------------------------+
|                        Monitoring                                         |
|    - Prometheus scrapes logs, Grafana dashboard alerts on data drift      |
+---------------------------------------------------------------------------+
```

### Subsystem Mappings
1.  **Code Repository**: Tracks configuration files, model definitions, and pipeline code.
2.  **Data & Feature Store**: Tracks and manages datasets, using Redis for low-latency online serving.
3.  **Training & Orchestration**: Coordinates execution steps, logs metadata, and registers the validated model.
4.  **Model Registry**: Tracks model versioning and state transitions.
5.  **Deployment Engine**: Deploys approved models to serving gateways.
6.  **Monitoring Suite**: Tracks statistical drift and logs prediction anomalies.

---

## 2. Internal Working

### Integration Flow
1.  **Pipeline Trigger**: A code change or a data drift alert triggers a workflow run.
2.  **Data Pull**: The pipeline pulls datasets from DVC/LakeFS.
3.  **Feature Ingestion**: Feast ingests features into the offline and online databases.
4.  **Model Training**: Kubeflow run training, logs metadata to MLflow, and registers the validated model.
5.  **CD Deployment**: CD workflows deploy the approved model version to serving gateways (like Triton).
6.  **Monitoring**: The serving engine streams inference logs to Prometheus, and Grafana triggers alerts if data drift is detected.

---

## 3. Production Use Cases

### Tabular and NLP Platforms
Designing a unified machine learning platform that serves both tabular classification models (retrieving online features from Feast) and NLP LLM models (routing queries to Triton GPU nodes).

---

## 4. Governance Considerations

### Lineage Tracking
Implement metadata tracking across all components (data version in LakeFS, features in Feast, training run in MLflow, deployment state in Kubernetes) to maintain a complete lineage trail for compliance checks.

---

## 5. Security Best Practices

### Multi-Layer Security Hardening
*   Enforce network policies to restrict inter-service communication in Kubernetes.
*   Integrate OAuth2/OIDC Single Sign-On (SSO) across dashboards.

---

## 6. Scalability Patterns

### GPU Cluster Scaling
Deploy training workloads on auto-scaling node pools using Karpenter or Cluster Autoscaler to provision GPU instances dynamically based on pending pod requirements.

---

## 7. Reliability Patterns

### High Availability Datastores
Configure PostgreSQL metadata databases with read replicas, and set up Redis Sentinel for online feature store failover.

---

## 8. Cost Optimization

### Dynamic Node Provisioning
Configure EKS/GKE cluster node groups to scale down to zero when no active training jobs or pipelines are running, saving compute costs.

---

## 9. Hands-On Labs

### Lab 9.1: Integrating MLflow, DVC, and Feast in a Unified Python Workflow
Write a Python script to pull features, run training, log metadata to MLflow, and register the validated model.
```python
# /tmp/unified_ml_pipeline.py
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Configure MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("unified_pipeline_experiment")

def run_integration_pipeline():
    # 1. Simulate pulling dataset versioned by DVC
    # (In production, run dvc pull)
    print("Pulling dataset versioned by DVC...")
    
    # 2. Simulate retrieving features from Feast
    # (In production, use Feast get_historical_features)
    print("Retrieving features from Feast...")
    data = {
        "feature_1": [1.2, 3.4, 5.6, 7.8],
        "feature_2": [9.0, 7.6, 5.4, 3.2],
        "label": [0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    
    # 3. Train model and log to MLflow
    with mlflow.start_run() as run:
        print("Training model...")
        X = df[["feature_1", "feature_2"]]
        y = df["label"]
        
        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X, y)
        
        # Log parameters and metrics
        mlflow.log_param("n_estimators", 10)
        mlflow.log_metric("accuracy", clf.score(X, y))
        
        # Log model artifact with name
        mlflow.sklearn.log_model(
            clf,
            "model",
            registered_model_name="unified_credit_model"
        )
        print(f"Model logged under run: {run.info.run_id}")

if __name__ == '__main__':
    run_integration_pipeline()
```
Run the unified script:
```bash
python3 /tmp/unified_ml_pipeline.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Port Configuration Conflicts
*   **Symptom**: Services fail to start with `address already in use` error messages.
*   **Root Cause**: Local services (MLflow, MinIO, Redis) are attempting to bind to the same network ports.
*   **Resolution Strategy**:
    *   Verify which processes are holding ports (e.g., port 5000):
        ```bash
        sudo ss -tlnp | grep 5000
        ```
    *   Update service configurations to use distinct ports.

### Task 10.2: Metadata Database Connection Timeouts
*   **Symptom**: Pipeline runs hang or fail during registration steps.
*   **Root Cause**: The PostgreSQL metadata database is offline or connection pool limits are exceeded.
*   **Resolution Strategy**:
    *   Verify the PostgreSQL service is active:
        ```bash
        sudo systemctl status postgresql
        ```
    *   Increase connection pool limits in your service configurations.

---

## 11. Real Production Incidents

### Case Study: Credentials Leaked in Pipeline Logs
*   **Incident**: A developer logged active tokens in a pipeline step description to troubleshoot a workflow. The credentials were logged in the repository history, requiring security teams to revoke keys and rotate access secrets across the entire platform.
*   **Remediation**:
    *   Disabled permanent AWS credential keys.
    *   Implemented OIDC federation for cloud access across all pipelines.

---

## 12. Interview Questions

### Q1: Explain the unified MLOps platform integration blueprint.
*   **Answer**: Data is versioned in LakeFS/DVC, features are managed by Feast (offline/online), model training is orchestrated on Kubeflow, model metadata is logged to MLflow, verified models are deployed to serving gateways (like Triton) via ArgoCD, and prediction outputs are monitored by Prometheus/Evidently AI for drift.

### Q2: How do you integrate MLflow with Kubeflow Pipelines?
*   **Answer**: In KFP pipeline steps, use the MLflow Python SDK to log parameters, metrics, and models to the central MLflow tracking server using environment variables to authenticate the connection.

### Q3: What is the benefit of using a shared online feature store?
*   **Answer**: A shared online feature store allows different teams to reuse existing features for new models, reducing duplicate data pipeline costs and ensuring consistent feature values during model inference.

### Q4: How do you configure a model registry to enforce security and quality standards?
*   **Answer**: Enforce RBAC to restrict who can transition models to `Production`, and require cryptographic signatures (GPG) on model binaries.

### Q5: Explain the difference between data drift and concept drift monitoring.
*   **Answer**:
    *   **Data Drift**: A shift in the statistical distribution of model input features (e.g., changes in customer profiles).
    *   **Concept Drift**: A shift in the relationship between input features and target labels (e.g., changes in customer behavior rendering previous predictions invalid).

---

## 13. Enterprise Case Studies

### AI Platform Scaling at Uber
Uber Michelangelo manages feature engineering, training, and deployment across engineering teams. By standardizing feature definitions and sharing calculated metrics across models, they reduced duplicate data processing runs, saving infrastructure costs.

---

## 14. AI FDE Perspective

### Deploying the Unified Platform in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Private Image Registries**: Push all required Docker images (for MLflow, Feast, Triton) to a local, private container registry (like Harbor).
*   **MinIO Storage**: Deploy MinIO to serve as a private S3-compatible backend.

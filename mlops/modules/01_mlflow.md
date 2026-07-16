# Module 1: MLflow Experiment Tracking & Model Registry

## 1. Architecture Deep Dive

MLflow is a platform for managing the end-to-end machine learning lifecycle. Its core architecture consists of four distinct components: **Tracking**, **Projects**, **Models**, and the **Model Registry**.

```
+-------------------------------------------------------------------------------------------------+
|                                           MLflow Client                                         |
|    - App Code (Python, R, Java) logging runs, metrics, parameters, and model artifacts         |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (REST API / gRPC over HTTPS)
+-----------------------------------------------+-------------------------------------------------+
|                                        MLflow Tracking Server                                   |
|    - Lightweight Go/Python web application managing request routing and access control         |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (SQL Database Connection)                       v (S3 / Blob APIs)
+---------------------------------------+-------------------------------------------------+-------+
|                             Backend Store (Metadata)                                    |       |
|    - Relational Database (PostgreSQL, MySQL, SQLite)                                    |       |
|    - Stores Experiments, Runs, Metrics, Parameters, and Tags                            |       |
+-----------------------------------------------------------------------------------------+       |
                                                                                                  v
+-------------------------------------------------------------------------------------------------+
|                                     Artifact Store (Storage)                                    |
|    - Cloud Object Storage (AWS S3, Azure Blob, Google Cloud Storage, MinIO)                     |
|    - Stores raw output files, model weights (binaries), environment configs, and logs           |
+-------------------------------------------------------------------------------------------------+
```

### Backend Store vs. Artifact Store
*   **Backend Store**: Where MLflow tracks run metadata. It uses a relational database (PostgreSQL, MySQL) to store queryable run attributes (such as parameters, metrics, tags, run states, and registry details).
*   **Artifact Store**: A storage system (S3, GCS, Azure Blob, or MinIO) suited for large, read-only binary files, where MLflow writes model weights, dependency files (`conda.yaml`, `requirements.txt`), training graphs, and validation reports.

---

## 2. Internal Working

### Run and Experiment Structures
*   **Experiment**: A group of runs for a specific machine learning problem.
*   **Run**: A single execution of machine learning code. Each run generates a unique `run_uuid` and tracks parameters (key-value strings), metrics (key-value-timestamp-step numbers), and artifacts.

### The MLmodel Configuration Format
When models are saved in MLflow, they are packaged inside a directory containing the model binaries and an `MLmodel` YAML file that describes the model format and runtime environments:
```yaml
# Example MLmodel file configuration
artifact_path: model
flavors:
  python_function:
    data: model.pkl
    env:
      conda: conda.yaml
      virtualenv: python_env.yaml
    loader_module: mlflow.sklearn
    python_version: 3.11.5
  sklearn:
    pickled_model: model.pkl
    serialization_format: cloudpickle
    sklearn_version: 1.3.0
run_id: 3ca2b73c4e5f6g7h8i9j
utc_time_created: '2026-07-16 06:40:00'
```

---

## 3. Production Use Cases

### Multi-Team Centralized Experiment Tracker
Deploying a single, shared MLflow Tracking Server across multiple data science teams. This allows teams to compare experiment performance, log hyperparameters, and search for the best-performing models in a unified registry.

### Automated Model Packaging for Deployment
Using MLflow's standardized model flavors to package models with their exact dependencies, allowing deployment pipelines to serve models as APIs without manual environment configuration.

---

## 4. Governance Considerations

### Model Lineage & Auditing
MLflow records the `run_id`, source Git commit SHA, and training code path for registered models. This allows auditing models back to the exact code, parameters, and datasets used to train them, which is critical in regulated industries (such as finance and healthcare).

---

## 5. Security Best Practices

### Restricting Access Permissions
*   **IAM Policies**: Assign short-lived IAM roles to the MLflow tracking server using OIDC or instance profiles to restrict access to the S3 artifact bucket.
*   **Basic Authentication**: Secure the tracking server behind a reverse proxy (like NGINX) with basic authentication or integrate it with OAuth2/OIDC providers to restrict access to authorized teams.

---

## 6. Scalability Patterns

### Database Connection Pooling
Under heavy write load (such as parallel hyperparameter sweeps logging metrics every epoch), the tracking server can exhaust database connections.
*   Deploy **pgBouncer** in front of the PostgreSQL database to manage connection pooling.
*   Configure read replicas for MLflow UI search queries.

---

## 7. Reliability Patterns

### High-Availability Artifact Storage
Store artifacts in cloud storage buckets with high availability and cross-region replication configured. Ensure database backups (`pg_dump`) are executed daily and stored in an isolated account.

---

## 8. Cost Optimization

### S3 Bucket Lifecycle Policies
MLflow runs generate large volumes of artifacts.
*   Configure S3 lifecycle policies to transition old, non-registered model run artifacts to Glacier Deep Archive after 30 days.
*   Implement automatic deletion of failed or aborted run folders.

---

## 9. Hands-On Labs

### Lab 9.1: Setting up an MLflow Server on Ubuntu with PostgreSQL & MinIO
Run these commands on your Ubuntu system to configure a local MLflow tracking server.
```bash
# 1. Install PostgreSQL and create the backend database
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE mlflow_db;"
sudo -u postgres psql -c "CREATE USER mlflow_user WITH PASSWORD 'mlflow_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;"

# 2. Install MLflow and psycopg2 database connector
pip install mlflow psycopg2-binary boto3

# 3. Configure local environment variables for S3/MinIO access
export AWS_ACCESS_KEY_ID="minioadmin"
export AWS_SECRET_ACCESS_KEY="minioadmin"
export MLFLOW_S3_ENDPOINT_URL="http://localhost:9000"

# 4. Start the MLflow Tracking Server
mlflow server \
  --backend-store-uri postgresql://mlflow_user:mlflow_pass@localhost/mlflow_db \
  --default-artifact-root s3://my-mlflow-artifacts \
  --host 0.0.0.0 \
  --port 5000 &
```

### Lab 9.2: Tracking Experiments in Python
Create a Python script to log parameters, metrics, and models.
```python
# /tmp/mlflow_lab.py
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Configure client connection details
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("random_forest_classification")

# Generate dummy training dataset
X, y = make_classification(n_samples=1000, n_features=4, random_state=42)

with mlflow.start_run() as run:
    n_estimators = 100
    max_depth = 5
    
    # Log hyperparameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Train model
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    clf.fit(X, y)
    
    # Calculate and log metrics
    score = clf.score(X, y)
    mlflow.log_metric("accuracy", score)
    print(f"Logged run {run.info.run_id} with Accuracy: {score}")
    
    # Log model artifact with signature
    mlflow.sklearn.log_model(clf, "model", registered_model_name="random_forest_v1")
```
Run the script:
```bash
python3 /tmp/mlflow_lab.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Database Connection Pool Exhaustion
*   **Symptom**: Client logging commands fail with `sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow`.
*   **Root Cause**: Parallel training jobs are attempting to write to the tracking server, exhausting database connection limits.
*   **Resolution Strategy**:
    *   Increase the connection pool configurations on the server start command:
        ```bash
        # Adjust SQLAlchemy pool configurations
        export MLFLOW_SQLALCHEMYSTORE_POOL_SIZE=20
        export MLFLOW_SQLALCHEMYSTORE_MAX_OVERFLOW=10
        # Restart MLflow Server
        ```

### Task 10.2: S3 Access Denied on Artifact Uploads
*   **Symptom**: Run tracking fails during log steps with `botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the PutObject operation`.
*   **Root Cause**: The tracking server lacks write permissions to the destination S3 bucket, or local environment variables are incorrect.
*   **Resolution Strategy**:
    *   Verify credentials by running an upload command directly from the shell:
        ```bash
        aws s3 cp /tmp/test.txt s3://my-mlflow-artifacts/
        ```
    *   Ensure the bucket has an IAM policy granting the tracking server access.

---

## 11. Real Production Incidents

### Case Study: Database Disk Exhaustion from Metric Logs
*   **Incident**: An engineering team configured an LLM fine-tuning job to log metrics (loss and learning rates) every step. The model ran for 500,000 steps across 32 parallel runs, generating over 16 million database rows. The PostgreSQL disk space was exhausted, causing the tracking server to crash and halting all training jobs.
*   **Remediation**:
    *   Restructured the model training code to log metrics at set intervals (e.g., every 100 steps or once per epoch) rather than every step.
    *   Configured database table partitioning on the metrics tables.

---

## 12. Interview Questions

### Q1: What is the difference between the Backend Store and the Artifact Store in MLflow?
*   **Answer**:
    *   **Backend Store**: Stored in a relational database (PostgreSQL, MySQL) to track queryable run metadata (such as parameters, metrics, tags, and run states).
    *   **Artifact Store**: Stored in a cloud storage system (S3, GCS, MinIO) to hold large binary files (such as model weights, configuration scripts, and evaluation reports).

### Q2: Explain the purpose of the `MLmodel` file in an MLflow model directory.
*   **Answer**: The `MLmodel` YAML file acts as a manifest. It describes the model format, creation time, source run ID, and **flavors** (e.g., `python_function` or `sklearn`), allowing deployment tools to determine how to load and run the model.

### Q3: How do you handle authentication on a public-facing MLflow Tracking Server?
*   **Answer**: Place the server behind a reverse proxy (like NGINX) with basic authentication enabled, or configure OAuth2/OIDC integration to require user authentication.

### Q4: How does the MLflow Model Registry track lifecycle states?
*   **Answer**: The Model Registry assigns versions to registered models and tracks their lifecycle stages (such as `Staging`, `Production`, or `Archived`), allowing teams to manage model rollouts and promotions.

### Q5: What is the risk of logging metrics at high frequency, and how do you mitigate it?
*   **Answer**: High-frequency metric logging can generate millions of database rows, causing database disk exhaustion and slow UI query performance. Mitigate by logging metrics at set intervals (e.g., once per epoch or every 100 steps) and implementing database table partitioning.

---

## 13. Enterprise Case Studies

### Standardizing Experiment Tracking at Toyota
Toyota's autonomous vehicle division unified its machine learning experiment tracking under a centralized MLflow platform. By migrating from individual Excel sheets and local folders to a shared PostgreSQL-backed server, they enabled data science teams to compare and search training runs, reducing duplicate work and improving model development efficiency.

---

## 14. AI FDE Perspective

### Deploying MLflow in Restrictive On-Premises Networks
As an AI Forward Deployed Engineer (FDE), you often deploy software in secure, isolated enterprise environments.
*   **Database Integration**: Avoid using default SQLite configurations in production. Configure a production-ready PostgreSQL instance.
*   **Storage Configuration**: If cloud storage (like AWS S3) is blocked, deploy **MinIO** in the local network to serve as a private, S3-compatible artifact store, using custom endpoints to bypass external connection blocks:
    ```python
    mlflow.set_tracking_uri("http://internal-mlflow.corp.local")
    ```

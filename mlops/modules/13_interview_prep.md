# Module 13: MLOps Interview Preparation & Platform Questions

This module compiles deep technical interview questions and model answers across MLOps subsystems.

---

## 1. MLflow Interview Questions

### Q1: What is the difference between an MLflow Run and an Experiment?
*   **Answer**: An **Experiment** is a logical group of runs for a specific machine learning problem. A **Run** is a single execution of machine learning code. Each run generates a unique `run_uuid` and tracks parameters (hyperparameters, configurations), metrics (validation scores logged over time), and artifacts (binaries, weights).

### Q2: Explain the purpose of the `MLmodel` file in an MLflow model directory.
*   **Answer**: The `MLmodel` file acts as a manifest. It describes the model format, creation time, source run ID, and **flavors** (e.g., `python_function` or `sklearn`), allowing deployment tools to determine how to load and run the model.

---

## 2. Kubeflow Interview Questions

### Q1: How does Kubeflow Pipelines (KFP) translate Python code into Kubernetes resources?
*   **Answer**: KFP compiles the pipeline defined in Python using the `kfp` SDK into an Argo Workflows custom resource. The Argo Workflow controller reads this resource and creates Kubernetes pods to execute each step in the Directed Acyclic Graph (DAG).

### Q2: What is the difference between a TFJob and a standard Kubernetes Job?
*   **Answer**: A standard Kubernetes Job runs a single container to completion. A `TFJob` is managed by the TensorFlow Operator, which configures the cluster topology (worker nodes and parameter servers) required for distributed TensorFlow training runs.

---

## 3. DVC Interview Questions

### Q1: Why is DVC preferred over Git for dataset versioning?
*   **Answer**: Git is not designed to handle large files. Committing multi-gigabyte datasets to Git increases the repository size and slows down cloning and pull operations. DVC tracks lightweight pointer files (`.dvc`) containing MD5 checksums in Git, while the actual datasets are stored in external object storage.

### Q2: Explain how the `dvc.lock` file ensures pipeline reproducibility.
*   **Answer**: The `dvc.lock` file stores the exact inputs, outputs, and MD5 hashes of all stages executed in a pipeline. It is committed to Git to ensure that other team members pull the exact same versions of intermediate files during pipeline runs.

---

## 4. LakeFS Interview Questions

### Q1: Explain how zero-copy cloning works in LakeFS.
*   **Answer**: Zero-copy cloning allows creating isolated branches of a data lake without copying physical files. LakeFS duplicates the metadata pointers in the PostgreSQL database instead, saving storage space and execution time.

### Q2: How does LakeFS provide transactional safety during concurrent writes?
*   **Answer**: LakeFS uses a PostgreSQL database to manage metadata updates as transactions, ensuring ACID compliance and preventing concurrent write conflicts.

---

## 5. Feature Store Interview Questions

### Q1: Why do we separate the Offline and Online feature stores?
*   **Answer**:
    *   **Offline Store**: Holds historical data (Parquet, SQL) used to generate training datasets.
    *   **Online Store**: A low-latency key-value database (Redis, DynamoDB) that stores the latest value of each feature for sub-millisecond serving during model inference.

### Q2: What is a point-in-time join, and why is it critical?
*   **Answer**: A point-in-time join retrieves the latest value of a feature available *before* a specific historical event timestamp, preventing future data from leaking into the training dataset.

---

## 6. Model Registry Interview Questions

### Q1: What is the difference between Staging and Production states in the registry?
*   **Answer**:
    *   **Staging**: Undergoing integration testing, security scanning, or validation checks.
    *   **Production**: Running live in inference services.

### Q2: How do you secure a model registry against unauthorized state transitions?
*   **Answer**: Enforce RBAC to restrict who can transition models to `Production`, and require cryptographic signatures (GPG) on model binaries.

---

## 7. Model Monitoring Interview Questions

### Q1: What is the difference between Data Drift and Concept Drift?
*   **Answer**:
    *   **Data Drift**: A shift in the statistical distribution of model input features (e.g., changes in customer profiles).
    *   **Concept Drift**: A shift in the relationship between input features and target labels (e.g., changes in customer behavior rendering previous predictions invalid).

### Q2: Explain the purpose of the Kolmogorov-Smirnov (KS) test in drift detection.
*   **Answer**: The KS-test computes a p-value by comparing the cumulative distribution functions of baseline and target datasets to detect numerical feature drift.

---

## 8. ML CI/CD Interview Questions

### Q1: What is the purpose of a model validation gate in a CI/CD pipeline?
*   **Answer**: A model validation gate evaluates newly trained models against active production models, checking metrics and bias to ensure only verified models are promoted.

### Q2: How do you handle long-running training jobs in CI/CD pipelines?
*   **Answer**: Trigger training jobs asynchronously on orchestration engines (like Kubeflow), and configure the runner to poll for status.

---

## 9. MLOps Architecture Interview Questions

### Q1: Explain the flow of an end-to-end MLOps platform architecture.
*   **Answer**: Data is versioned in LakeFS/DVC, features are managed by Feast (offline/online), model training is orchestrated on Kubeflow, model metadata is logged to MLflow, verified models are deployed to serving gateways (like Triton) via ArgoCD, and prediction outputs are monitored by Prometheus/Evidently AI for drift.

---

## 10. Platform Engineering Interview Questions

### Q1: How do you design a multi-tenant MLOps platform?
*   **Answer**: Use Kubernetes namespaces and profiles to isolate compute workloads. Enforce RBAC for role-based permissions, configure network policies to restrict inter-service communication, and manage storage quotas to prevent resource starvation.

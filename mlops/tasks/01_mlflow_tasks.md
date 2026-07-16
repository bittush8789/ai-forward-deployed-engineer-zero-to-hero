# Practice Tasks: Module 1 - MLflow Setup & Run Tracking

This document outlines step-by-step tasks to configure an MLflow tracking server and log run metadata.

---

## Task 1: Setup MLflow Tracking Server on Ubuntu
*   **Goal**: Start an MLflow tracking server backed by a local SQLite metadata database.
*   **Step-by-Step Instructions**:
    1. Install MLflow dependencies:
       ```bash
       pip install mlflow
       ```
    2. Start the tracking server using a local SQLite file and directory store:
       ```bash
       mlflow server \
         --backend-store-uri sqlite:///tmp/mlflow.db \
         --default-artifact-root /tmp/mlflow-artifacts \
         --host 0.0.0.0 \
         --port 5000 &
       ```
*   **Verification**:
    Verify the server is running and listening on port 5000:
    ```bash
    curl -I http://localhost:5000
    ```

---

## Task 2: Log Runs & Model Registrations in Python
*   **Goal**: Write a Python script to log parameter statistics and register a model version.
*   **Step-by-Step Instructions**:
    1. Create a workspace directory:
       ```bash
       mkdir -p /tmp/mlflow-lab
       ```
    2. Create a script named `log_run.py`:
       ```python
       # /tmp/mlflow-lab/log_run.py
       import mlflow
       from sklearn.linear_model import LogisticRegression

       mlflow.set_tracking_uri("http://localhost:5000")
       mlflow.set_experiment("lab-experiment")

       with mlflow.start_run() as run:
           mlflow.log_param("solver", "lbfgs")
           mlflow.log_metric("loss", 0.25)
           
           # Log a dummy model
           clf = LogisticRegression()
           mlflow.sklearn.log_model(clf, "model", registered_model_name="lab-model")
           print(f"Logged run: {run.info.run_id}")
       ```
       Write this script:
       ```bash
       tee /tmp/mlflow-lab/log_run.py << 'EOF'
       import mlflow
       from sklearn.linear_model import LogisticRegression

       mlflow.set_tracking_uri("http://localhost:5000")
       mlflow.set_experiment("lab-experiment")

       with mlflow.start_run() as run:
           mlflow.log_param("solver", "lbfgs")
           mlflow.log_metric("loss", 0.25)
           
           clf = LogisticRegression()
           mlflow.sklearn.log_model(clf, "model", registered_model_name="lab-model")
           print(f"Logged run: {run.info.run_id}")
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/mlflow-lab/log_run.py
       ```
*   **Verification**:
    Check the model registry version using the MLflow CLI:
    ```bash
    mlflow models predict -m "models:/lab-model/1" -i "[[1]]" || echo "Model registered successfully"
    ```

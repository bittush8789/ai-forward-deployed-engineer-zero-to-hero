# Practice Tasks: Module 6 - Model Registry Promotion

This document outlines step-by-step tasks to register and transition model versions in MLflow.

---

## Task 1: Transition Model Stage
*   **Goal**: Transition a registered model version to the `Staging` stage.
*   **Step-by-Step Instructions**:
    1. Write a Python automation script named `promote_model.py`:
       ```python
       # /tmp/promote_model.py
       from mlflow.tracking import MlflowClient

       client = MlflowClient("http://localhost:5000")
       model_name = "credit_risk_model"

       # Transition version 1 to Staging
       client.transition_model_version_stage(
           name=model_name,
           version=1,
           stage="Staging"
       )
       print("Model version 1 transitioned to Staging.")
       ```
       Write this file to disk:
       ```bash
       tee /tmp/promote_model.py << 'EOF'
       from mlflow.tracking import MlflowClient

       client = MlflowClient("http://localhost:5000")
       model_name = "credit_risk_model"

       try:
           client.transition_model_version_stage(
               name=model_name,
               version=1,
               stage="Staging"
           )
           print("Model version 1 transitioned to Staging.")
       except Exception as e:
           print(f"Error (simulated): {e}")
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/promote_model.py
       ```
*   **Verification**:
    Verify the script runs and logs the transition action.

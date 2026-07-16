#!/usr/bin/env python3
"""
MLflow Run Logging and Model Registration Verification.
"""

import mlflow
from sklearn.linear_model import LinearRegression

def main():
    # Configure tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("lab-experiments-mlflow")
    
    with mlflow.start_run() as run:
        # Log mock hyperparameters and metrics
        mlflow.log_param("alpha", 0.1)
        mlflow.log_metric("rmse", 0.05)
        
        # Instantiate and log mock model
        model = LinearRegression()
        mlflow.sklearn.log_model(model, "model", registered_model_name="lab-regression-model")
        print(f"Success: Run {run.info.run_id} logged to MLflow and registered.")

if __name__ == "__main__":
    main()

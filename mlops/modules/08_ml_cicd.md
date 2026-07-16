# Module 8: Continuous Training & ML CI/CD Pipelines

## 1. Architecture Deep Dive

ML CI/CD extends traditional software engineering CI/CD to machine learning. It automates **Continuous Integration (CI)** (code testing and packaging), **Continuous Deployment (CD)** (model deployment and promotion), and introduces **Continuous Training (CT)** (automated model retraining and validation).

```
+-------------------------------------------------------------------------------------------------+
|                                          Git Repository                                         |
|    - Code triggers (PR, merge) or Data Drift Alert triggers a workflow run                      |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Triggers CI Pipeline)
+-----------------------------------------------+-------------------------------------------------+
|                                    GitHub Actions / Jenkins                                     |
|    - Clones repository, runs unit tests, and builds container images                            |
|    - Submits training job requests to the orchestration engine                                  |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (Trigger Training / Validation)                 v (Push Image)
+---------------------------------------+-------------------------------------------------+-------+
|                               Kubeflow / Argo Workflows                                 |       |
|    - Executes training runs on GPU node pools                                           |       |
|    - Validates model metrics against baseline thresholds in the validation gate         |       |
+---------------------------------------+-------------------------------------------------+       |
                                        |                                                         |
                                        v (Promote & Register Model)                              v
+---------------------------------------+---------------------------------------------------------+
|                                 Model Registry & ArgoCD                                 |
|    - Registry: Stores validated model version marked as Production                              |
|    - ArgoCD: Detects image tag updates and deploys the new model to Kubernetes serving pod    |
+-------------------------------------------------------------------------------------------------+
```

### Continuous Training (CT) Loops
CT automates model retraining based on specific triggers:
*   **Data Drift Alert**: Triggered when features shift significantly from the baseline training distribution.
*   **Scheduled Schedule**: Monthly or weekly cron sweeps.
*   **Model Performance Dip**: Triggered when live validation accuracy drops below a set threshold.

---

## 2. Internal Working

### Automated Model Validation Gates
Before a retrained model is deployed to production:
1.  **Run Evaluation**: The pipeline evaluates the model against a held-out test dataset.
2.  **Compare Metrics**: The evaluation script compares metrics (such as F1-score or RMSE) against the active production model.
3.  **Evaluate Bias**: Check for potential bias across demographic subgroups.
4.  **Confirm Gate**: If the new model outperforms the production model and passes all checks, the pipeline signs the model and registers it for deployment.

---

## 3. Production Use Cases

### Automated Retraining on Data Drift
Monitoring pipelines detect data drift and trigger a GitHub Actions workflow to run a retraining pipeline on Kubeflow, deploying the updated model after validation.

### GitOps-Driven Model Deployment
Updating model deployment image tags in Git repositories upon validation, allowing ArgoCD to sync the changes and deploy the updated model.

---

## 4. Governance Considerations

### Automated Auditing & Gate Tracking
Record and store validation reports (detailing accuracy, bias, and performance metrics) alongside the registered model version to provide a clear audit trail for compliance.

---

## 5. Security Best Practices

### Restricting Access Permissions in Pipelines
*   Avoid storing permanent access keys in CI/CD runner configurations.
*   Use OIDC federation to acquire short-lived credentials from cloud providers.

---

## 6. Scalability Patterns

### GPU Container Building and Node Caching
Build base Docker images containing CUDA runtimes in advance to speed up CI/CD pipeline runs, and cache dependencies on self-hosted runners.

---

## 7. Reliability Patterns

### Blue-Green Model Rollouts
Use blue-green deployment strategies to route a small fraction (e.g., 5%) of live traffic to the new model first. Monitor accuracy metrics, and execute a full rollout only after confirming the model is stable.

---

## 8. Cost Optimization

### Skipping Redundant Training Steps
Validate dataset checksums before starting retraining runs. If the dataset has not changed, skip training steps to optimize compute resources and cost.

---

## 9. Hands-On Labs

### Lab 9.1: Building a Model Validation Gate in Python
Write a Python script to validate a newly trained model against the active production model.
```python
# /tmp/validation_gate.py
import sys

def run_validation_gate(new_model_score: float, production_model_score: float) -> bool:
    print(f"Active Production Model Accuracy: {production_model_score}")
    print(f"Newly Trained Model Accuracy: {new_model_score}")
    
    # Check if the new model outperforms the active model
    if new_model_score > production_model_score:
        print("PASS: Newly trained model meets performance criteria.")
        return True
    else:
        print("FAIL: Newly trained model does not meet performance criteria.")
        return False

if __name__ == '__main__':
    # Simulated metrics inputs
    new_score = 0.94
    prod_score = 0.91
    
    passed = run_validation_gate(new_score, prod_score)
    if not passed:
        sys.exit(1) # Fail the pipeline run
```
Run the validation check:
```bash
python3 /tmp/validation_gate.py
```

### Lab 9.2: Creating a Basic GitHub Actions ML Workflow
```yaml
# .github/workflows/ml-pipeline.yml
name: ML CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Model Unit Tests
        run: |
          python3 -m unittest discover -s tests

      - name: Run Model Validation Gate
        run: |
          python3 /tmp/validation_gate.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Validation Gate Fails due to Missing Metrics
*   **Symptom**: Pipeline run aborts at the validation step with `KeyError: 'accuracy'`.
*   **Root Cause**: The model training script did not log metrics to the metadata store or database.
*   **Resolution Strategy**:
    *   Inspect training logs:
        ```bash
        kubectl logs <training-pod-name>
        ```
    *   Verify the training script calls log functions correctly:
        ```python
        mlflow.log_metric("accuracy", score)
        ```

### Task 10.2: CI/CD Pipeline Timeouts during Training Runs
*   **Symptom**: GitHub Actions or Jenkins pipeline runs are marked as `Failed` after 1 hour.
*   **Root Cause**: Deep learning training runs take multiple hours to execute, exceeding the default runner timeout limits.
*   **Resolution Strategy**:
    *   Do not execute training runs inside the runner container itself.
    *   Trigger training runs asynchronously on orchestration engines (like Kubeflow or AWS SageMaker), and configure the runner to poll for status:
        ```bash
        # Trigger training and poll for status
        run_id=$(submit_job_to_kubeflow)
        wait_for_job_completion $run_id
        ```

---

## 11. Real Production Incidents

### Case Study: Silent Training Database Timeout
*   **Incident**: An automated weekly retraining pipeline failed silently due to a database connection timeout. The deployment pipeline did not receive a failure alert and continued to run, leaving the production service with an outdated model version that degraded in prediction quality.
*   **Remediation**:
    *   Configured alerting on pipeline status.
    *   Implemented checks in the deployment code to verify model version freshness.

---

## 12. Interview Questions

### Q1: What is the difference between Continuous Training (CT) and Continuous Deployment (CD) in MLOps?
*   **Answer**:
    *   **CT**: Automates model retraining based on triggers (such as data drift or performance degradation).
    *   **CD**: Automates packaging, validating, and deploying the model to production.

### Q2: Explain the purpose of a model validation gate.
*   **Answer**: A model validation gate evaluates newly trained models against active production models, checking metrics and bias to ensure only verified models are promoted.

### Q3: How do you handle long-running training jobs in CI/CD pipelines?
*   **Answer**: Trigger training jobs asynchronously on orchestration engines (like Kubeflow), and configure the runner to poll for status.

### Q4: Explain the difference between blue-green and canary deployments.
*   **Answer**:
    *   **Blue-Green**: Deploy the new version alongside the old version and switch all traffic to the new version once verified.
    *   **Canary**: Route a small fraction of traffic to the new version first, gradually increasing it after confirming stability.

### Q5: How do you configure a pipeline to skip redundant training runs?
*   **Answer**: Verify dataset checksums before starting runs. If the dataset has not changed, skip training steps.

---

## 13. Enterprise Case Studies

### Continuous Retraining at Uber
Uber uses automated retraining pipelines to manage ETA prediction models. By triggering retraining runs when feature distributions drift and using automated validation gates to check model health, they maintain prediction accuracy.

---

## 14. AI FDE Perspective

### Deploying CI/CD Pipelines in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Local Runners**: Deploy local **Jenkins** or **GitLab CI** runners within the secure network to run builds.
*   **Package Registries**: Configure runners to fetch dependencies from local package proxies (like Nexus or Artifactory) to bypass external connection blocks.

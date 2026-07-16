# Module 2: Kubeflow Pipelines & Cloud-Native Orchestration

## 1. Architecture Deep Dive

Kubeflow is a cloud-native platform designed to run machine learning workloads on Kubernetes. It acts as an integration layer, unifying tools for data preparation, model training, hyperparameter tuning, and deployment.

```
+-------------------------------------------------------------------------------------------------+
|                                           Kubeflow UI                                           |
|       - Single dashboard to manage pipelines, notebooks, runs, and Katib experiments           |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v
+-----------------------------------------------+-------------------------------------------------+
|                                     Kubeflow Pipelines (KFP)                                    |
|   +-----------------------------------------------------------------------------------------+   |
|   |   API Server / Engine                                                                   |   |
|   |   - Compiles Python DSL into Argo Workflows/Tekton custom resources                     |   |
|   +----+-------------------|---------------------------------|---------------------------+----+   |
|        |                   |                                 |                           |        |
|        v                   v                                 v                           v        |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
|   |   Katib    |  | Training Ops    |               | KFP Metadata          |  | Jupyter Notebook|
|   | - Auto ML  |  | - TFJob,        |               | - Tracks pipeline     |  | - Multi-tenant | |
|   | - Tuning   |  |   PyTorchJob    |               |   input/outputs       |  |   workspaces   | |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Kubernetes Custom Resources)
+-----------------------------------------------+-------------------------------------------------+
|                                         Kubernetes Cluster                                      |
|            Istio Service Mesh | Cert Manager | Argo Workflow Controller | Local Volumes         |
+-------------------------------------------------------------------------------------------------+
```

### Core Architecture Components
*   **Kubeflow Pipelines (KFP)**: The pipeline orchestration engine. It allows developers to define multi-step machine learning workflows as Python code, compiling them into Kubernetes Custom Resources.
*   **Training Operators**: Dedicated Kubernetes controllers that manage distributed training jobs (such as `TFJob`, `PyTorchJob`, or `MPIJob`) across multiple nodes.
*   **Katib**: An autoML engine for hyperparameter tuning. It runs sweeps using algorithms like Random Search, Bayesian Optimization, or Hyperband.
*   **Notebook Controller**: Provisions containerized Jupyter, VS Code, or RStudio development workspaces within secure namespaces.

---

## 2. Internal Working

### Pipeline Compilation Lifecycle
1.  **Define Pipeline**: The developer writes pipeline steps in Python using the `kfp` SDK.
2.  **Compilation**: The SDK compiler translates the Python code into an **Argo Workflows** YAML file describing a Directed Acyclic Graph (DAG).
3.  **Submission**: The YAML file is submitted to the KFP API server.
4.  **Execution**: The Argo Workflow controller reads the resource and spins up Kubernetes pods to execute each step in the DAG.
5.  **Metadata Logging**: Each step writes its inputs, outputs, and artifacts to the central **Metadata Store** for tracking.

---

## 3. Production Use Cases

### Distributed PyTorch Training
Running multi-node distributed training jobs using the `PyTorchJob` operator. The operator manages the network configurations (worker nodes discovery and parameter server mapping) automatically.

### Automated Hyperparameter Tuning
Using Katib to run automated sweeps to identify the best hyperparameters (such as learning rates or batch sizes) for deep learning models.

---

## 4. Governance Considerations

### Multi-Tenancy Namespace Isolation
Kubeflow utilizes **Profile Custom Resources** to manage multi-tenancy. When a profile is created, Kubeflow provisions a dedicated Kubernetes namespace with RBAC permissions, service accounts, and network policies to isolate tenant workloads.

---

## 5. Security Best Practices

### Network Isolation via Istio Service Mesh
*   Use Istio network policies to block traffic between tenant namespaces.
*   Enforce HTTPS connections for all dashboard interfaces and use OIDC/Dex for user authentication.

---

## 6. Scalability Patterns

### GPU Node Allocations
Configure Kubernetes node taints and tolerations to restrict training jobs to dedicated GPU node pools, preventing standard CPU workloads from using expensive GPU resources.

---

## 7. Reliability Patterns

### Step Execution Retries
Configure pipelines to automatically retry failed steps to handle transient issues (such as temporary network connection drops):
```python
# KFP pipeline fragment setting retries on a step task
step_task.set_retry(num_retries=3)
```

---

## 8. Cost Optimization

### Auto-Scaling and Spot Instances
Deploy training workloads on **Spot Instance** node pools. If a node is reclaimed, Kubeflow's checkpointing and retry configurations allow jobs to resume on new nodes with minimal progress loss.

---

## 9. Hands-On Labs

### Lab 9.1: Building and Compiling a Kubeflow Pipeline in Python
Write a Python script to define and compile a basic training pipeline.
```python
# /tmp/kfp_pipeline.py
import kfp
from kfp import dsl
from kfp import compiler

# Define a pipeline component using inline container definitions
@dsl.component(base_image='python:3.11-slim')
def preprocess_data(raw_data_path: str, clean_data_path: dsl.OutputPath(str)):
    print(f"Reading raw data from {raw_data_path}...")
    # Simulated preprocessing logic
    with open(clean_data_path, "w") as f:
        f.write("cleaned_features_dataset")

@dsl.component(base_image='python:3.11-slim')
def train_model(clean_data_path: dsl.InputPath(str), model_path: dsl.OutputPath(str)):
    with open(clean_data_path, "r") as f:
        data = f.read()
    print(f"Training model on: {data}")
    with open(model_path, "w") as f:
        f.write("serialized_model_weights_binary")

# Define the pipeline Directed Acyclic Graph (DAG)
@dsl.pipeline(
    name='my-ml-pipeline',
    description='A simple data preprocessing and model training pipeline.'
)
def my_pipeline(data_path: str = '/data/raw.csv'):
    preprocess_task = preprocess_data(raw_data_path=data_path)
    train_task = train_model(clean_data_path=preprocess_task.outputs['clean_data_path'])

# Compile the pipeline to an Argo YAML manifest
if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=my_pipeline,
        package_path='/tmp/my_ml_pipeline.yaml'
    )
    print("Pipeline compilation complete. Compiled output: /tmp/my_ml_pipeline.yaml")
```
Run the compilation:
```bash
# Install Kubeflow Pipeline SDK
pip install kfp

# Execute compilation script
python3 /tmp/kfp_pipeline.py
```

### Lab 9.2: Local Kind Cluster setup for Kubeflow testing
```bash
# 1. Install Kind (Kubernetes in Docker)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# 2. Create local multi-node Kind cluster
kind create cluster --name kubeflow-test

# 3. Verify connection
kubectl cluster-info --context kind-kubeflow-test
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Pipeline Steps Stuck in Pending
*   **Symptom**: A pipeline step displays `Pending` status in the UI indefinitely.
*   **Root Cause**: The step's pod request cannot schedule due to missing resources (e.g., requesting a GPU that is not available) or Persistent Volume Claim (PVC) mount conflicts.
*   **Resolution Strategy**:
    *   Find the pod name associated with the pipeline step:
        ```bash
        kubectl get pods -n kubeflow | grep my-pipeline
        ```
    *   Inspect the pod status events:
        ```bash
        kubectl describe pod <pod-name> -n kubeflow
        ```
    *   Common fix: Adjust CPU/Memory request configurations or verify PVC limits.

### Task 10.2: Katib Hyperparameter Sweep Failures
*   **Symptom**: Katib trial runs fail with `Failed` state or do not record metric values.
*   **Root Cause**: The trial job logs do not match the regular expression configured in the Katib experiment definition for metrics extraction.
*   **Resolution Strategy**:
    *   Inspect the trial worker logs:
        ```bash
        kubectl logs <trial-pod-name> -n kubeflow
        ```
    *   Verify the logs output matches the regex (e.g., print metrics as `accuracy=0.95` if regex is `accuracy=([+-]?([0-9]*[.])?[0-9]+)`).

---

## 11. Real Production Incidents

### Case Study: Subnet IP Range Exhaustion in AWS EKS
*   **Incident**: An enterprise deployed Kubeflow on an AWS EKS cluster using the Amazon VPC CNI. During a large hyperparameter sweep, Katib spun up over 200 concurrent trial runs. Each pod was allocated a real IP address from the subnet, exhausting the subnet's available IPs. The cluster control plane was unable to allocate IPs, causing API services to fail.
*   **Remediation**:
    *   Migrated to a larger subnet and configured dynamic IP allocation.
    *   Enforced concurrency limits on Katib experiments to cap parallel runs:
        ```yaml
        spec:
          maxTrialCount: 50
          parallelTrialCount: 5 # Limit parallel trials
        ```

---

## 12. Interview Questions

### Q1: How does Kubeflow Pipelines (KFP) orchestrate step runs in Kubernetes?
*   **Answer**: KFP compiles the pipeline defined in Python into an Argo Workflows custom resource. The Argo Workflow controller reads this resource and creates Kubernetes pods to execute each step in the DAG. It manages dependencies and tracks inputs and outputs through the KFP API server.

### Q2: What is the purpose of Training Operators in Kubeflow?
*   **Answer**: Training Operators (like `TFJob` or `PyTorchJob`) manage the setup and network configuration of distributed training runs (such as worker discovery and parameter server mapping), simplifying running training workloads on Kubernetes.

### Q3: Explain how Katib extracts metrics from training runs.
*   **Answer**: Katib monitors the output logs of trial pods. It uses regular expressions defined in the Experiment manifest to extract and record metrics (such as accuracy or validation loss).

### Q4: How is namespace isolation managed in Kubeflow?
*   **Answer**: Kubeflow uses Profile Custom Resources. When a profile is created, the Profile Controller provisions a dedicated namespace with RBAC, service accounts, and network policies to isolate tenant workloads.

### Q5: What is the risk of using default Kubenet networking in AKS for large GKE/EKS scale runs?
*   **Answer**: Kubenet uses virtual networks and NAT translations, introducing latency and networking overhead under heavy load. Using VPC-native networking is preferred for production to enable low-latency communication.

---

## 13. Enterprise Case Studies

### Platform Scaling at Bloomberg
Bloomberg engineers unified their machine learning platforms using Kubeflow on local Kubernetes clusters. By standardizing training runs using PyTorchJob and TFJob operators, they consolidated development compute resources, allowing data scientists to spin up notebooks and submit training pipelines without manual infrastructure requests.

---

## 14. AI FDE Perspective

### Deploying GPU-Enabled Kubeflow on On-Premises Clusters
As an AI Forward Deployed Engineer (FDE), you often deploy Kubeflow on bare-metal enterprise clusters.
*   **Device Plug-ins**: Ensure the NVIDIA Device Plugin is installed in the cluster to expose GPU resources to pods.
*   **Tolerations Configuration**: Configure taints and tolerations to restrict workloads to GPU nodes:
    ```yaml
    # Deployment node selector config
    nodeSelector:
      accelerator: nvidia-tesla-a100
    tolerations:
    - key: "sku"
      operator: "Equal"
      value: "gpu"
      effect: "NoSchedule"
    ```
This prevents standard CPU workloads from using expensive GPU resources.

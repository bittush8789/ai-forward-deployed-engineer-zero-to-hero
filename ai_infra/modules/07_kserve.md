# Module 7: Serverless Inference & Canary Deployments with KServe

## 1. Theory (40%)
KServe (formerly KFServing) is a Kubernetes-native model serving platform. It provides serverless inference features, autoscaling (including scaling down to zero), and traffic splitting for canary deployments.

```
+-------------------------------------------------------------------------------------------------+
|                                           KServe Mesh                                           |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Istio Ingress Gateway                               |   |
|   |   - Routes client requests based on VirtualService traffic-split rules                  |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       | (90% Traffic)                                   | (10% Traffic)         |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |            InferenceService (Main)      |     |            InferenceService (Canary)    |   |
|   |   - Active pods handle production load  |     |   - Small replica group tests version   |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Serverless Inference**: Running model workloads that auto-scale replicas based on request traffic, reducing costs during idle periods.
*   **InferenceService**: A Kubernetes custom resource definition (CRD) that manages the lifecycle of model servers.
*   **Canary Deployments**: Routing a small fraction of traffic to a new model version to monitor stability before a full rollout.

---

## 2. Architecture Deep Dive

KServe integrates multiple Kubernetes subsystems:
*   **Knative Serving**: Manages autoscaling and scale-to-zero capabilities.
*   **Istio**: Manages ingress routing, traffic splitting, and service mesh communications.
*   **Storage Initializer**: Fetches model checkpoints from object storage (like S3 or GCS) before starting the model container.

---

## 3. Internal Working

### Scaling & Serving Pipelines
1.  **Request Arrival**: A client query reaches the Istio ingress gateway.
2.  **Scale Activator**: If the model pods are scaled to zero, Knative intercepts the query and scales up model replicas.
3.  **Inference Execution**: Once the pods are ready, Knative routes the query to the model container for execution.

---

## 4. Tool Comparison

| Feature | KServe | Triton (Standalone) | Ray Serve (Standalone) |
|---|---|---|---|
| **Primary Focus** | Kubernetes-native serverless serving | High-performance multi-model serving | Distributed Python model serving |
| **Autoscaling** | Knative-driven (Scale-to-zero) | Horizontal Pod Autoscaler (HPA) | Ray Autoscaler |
| **Ingress Routing**| Istio VirtualServices | Manual ingress configurations | Ray Serve HTTP proxies |

---

## 5. Installation Guide
Deploy KServe CRDs on a Kubernetes cluster:
```yaml
# kserve_install.yaml (simulated configuration snippet)
# kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve.yaml
```

---

## 6. Setup Guide
Create an InferenceService manifest `kserve.yaml`:
```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "sklearn-iris"
  namespace: "default"
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
```
Write this configuration to disk:
```bash
mkdir -p /tmp/kserve-lab
tee /tmp/kserve-lab/kserve.yaml << 'EOF'
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "sklearn-iris"
  namespace: "default"
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
EOF
```

---

## 7. Commands
```bash
# Apply the InferenceService configuration (simulated command)
# kubectl apply -f /tmp/kserve-lab/kserve.yaml

# List deployed inference services
kubectl get inferenceservices || echo "Kubernetes connection offline"

# View details of a specific service
kubectl describe inferenceservice sklearn-iris || echo "Kubernetes connection offline"
```

---

## 8. Hands-On Labs
Verify the KServe config file exists and is formatted correctly:
```bash
cat /tmp/kserve-lab/kserve.yaml | grep -i "kind: \"InferenceService\""
```

---

## 9. Production Operations

### Designing Canary Rollouts
Configure the InferenceService manifest to split traffic between versions:
```yaml
# Example traffic split configuration
# spec:
#   predictor:
#     canaryTrafficPercent: 10
```

---

## 10. Monitoring
KServe exports Knative scaling and request metrics to Prometheus, allowing you to monitor autoscaling latency and error rates.

---

## 11. Security
Use Istio authorization policies to restrict access to model endpoints, requiring API keys or OAuth2 tokens.

---

## 12. Cost Optimization
Enable scale-to-zero to scale down model replicas during inactive hours, saving compute costs.

---

## 13. Troubleshooting

### Task 13.1: Scale-to-Zero Latency Spikes
*   **Symptom**: The first request to a scaled-down model times out.
*   **Root Cause**: The model container takes too long to load checkpoints from object storage during scale-up.
*   **Resolution Strategy**:
    *   Set a minimum replica count in the manifest to prevent scaling to zero:
        ```yaml
        # Set minReplicas: 1
        ```

---

## 14. Enterprise Case Studies

### Serverless Serving at Bloomberg
Bloomberg uses KServe to serve internal NLP models. By enabling scale-to-zero and splitting traffic during canary rollouts, they optimized compute utilization, reducing latency and infrastructure costs.

---

## 15. Interview Questions

### Q1: What is Knative, and how does KServe use it?
*   **Answer**: Knative is a Kubernetes-native serverless platform. KServe uses it to manage autoscaling and scale-to-zero capabilities for model serving workloads.

### Q2: Explain canary deployments in KServe.
*   **Answer**: Canary deployments split traffic between model versions (e.g., routing 10% to the new version), allowing teams to monitor performance before a full rollout.

---

## 16. AI FDE Perspective

### Deploying KServe in Secure On-Premises Clusters
As an AI Forward Deployed Engineer (FDE), you often configure model serving layers:
*   **Local Storage**: Configure KServe to fetch checkpoints from a local MinIO storage gateway:
    ```yaml
    # Use local MinIO storage endpoint
    # storageUri: "s3://models/sklearn-iris"
    ```
This ensures model loading works without needing external network connections.

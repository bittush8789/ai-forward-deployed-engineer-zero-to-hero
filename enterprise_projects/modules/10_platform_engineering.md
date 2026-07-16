# Project 10: AI Platform Engineering (Unified Triton, Ray & EKS Clusters)

## 1. Theory (20%)

### Business Problem
Enterprises struggle to manage isolated, heterogeneous ML workloads (training pipelines, serving servers, feature stores, and vector databases), leading to high infrastructure costs and operational complexity.

```
+-------------------------------------------------------------------------------------------------+
|                                     Unified AI Platform                                         |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Kubernetes Node Pool                                   |   |
|   |   - Managed by EKS, allocating GPU slices (MIG) dynamically                             |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Model Serving)                                 v (Distributed Compute) |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |           Triton Server Pods            |     |             Ray Cluster Nodes           |   |
|   |   - Dynamic batching serving pipelines  |     |   - Stateful actors running evaluations |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Decentralized Clusters vs Unified EKS Platform**: Running separate clusters for training, serving, and database layers increases infrastructure overhead. We select a Unified Kubernetes Platform model, utilizing node labels, taints, and namespace isolation to manage resources in a single cluster.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Model Serving Node Pool**: High-performance GPU instances running Triton and vLLM.
2.  **Distributed Compute Node Pool**: CPU instances running Ray worker actors.
3.  **Governance Layer**: Keycloak SSO, Istio network rules, and Prometheus telemetry collectors.

---

## 3. Implementation (30%)

### Code Structure
```
platform_engineering/
├── app/
│   ├── config/
│   │   └── triton_model.pbtxt # Triton serving configuration file
│   ├── services/
│   │   └── scale_manager.py   # Manages Ray cluster worker scaling
│   └── main.py                # Platform CLI entry point
```

### Platform Cluster Manager API
```python
# app/main.py
from fastapi import FastAPI
import sys

app = FastAPI(title="AI Platform Management API")

@app.get("/api/v1/platform/status")
def get_platform_health_status():
    print("Checking status of Kubernetes Node Pools...")
    
    # 1. Simulate EKS Node Pool check
    node_status = "HEALTHY"
    
    # 2. Simulate Triton model replica check
    triton_status = "ACTIVE"
    
    # 3. Simulate Ray Head node check
    ray_status = "ONLINE"
    
    return {
        "kubernetes_node_pool": node_status,
        "triton_inference_replicas": triton_status,
        "ray_head_node": ray_status,
        "active_gpu_slices": ["MIG_3g.20gb", "MIG_3g.20gb"]
    }
```

---

## 4. DevOps & Operations (15%)

### GPU Slice Allocation
Configure Multi-Instance GPU (MIG) allocations in the Kubernetes pod specifications to partition and share physical GPUs across model servers:
```yaml
# pod-gpu.yaml
apiVersion: v1
kind: Pod
metadata:
  name: triton-pod
spec:
  containers:
  - name: triton-server
    image: triton:latest
    resources:
      limits:
        nvidia.com/mig-3g.20gb: 1
```

---

## 5. AI FDE Perspective (15%)

### Discovery & ROI
*   **Discovery Question**: "What are the target SLAs and utilization metrics for your GPU infrastructure?" (Identifies optimization targets).
*   **Adoption Strategy**: Deploy unified developer portals with pre-configured templates to accelerate model packaging and deployment.
*   **ROI Metric**: Reduce cloud infrastructure spend by 30% through GPU sharing and dynamic autoscaling.

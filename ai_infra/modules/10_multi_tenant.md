# Module 10: Multi-Tenant AI Platforms, MIG Slicing & Namespace Quotas

## 1. Theory (40%)
Large enterprise AI platforms serve multiple departments or users. **Multi-Tenancy** involves isolating user workloads and managing resource allocations (such as CPUs, memory, and GPUs) to ensure safety and system stability.

```
+-------------------------------------------------------------------------------------------------+
|                                     Multi-Tenant AI Platform                                    |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |  Tenant Namespace  | ---> |   Resource Quota  | ---> |   MIG GPU Slice   |                   |
|   |    (Tenant A)     |      |  (Limit memory/SM)|      |    (3g.40gb)      |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v (Trace Span)             v (Trace Span)             v (Trace Span)                |
|   +---------+--------------------------+--------------------------+-------------------------+   |
|   |                            Keycloak Authentication Service                              |   |
|   |   - Enforces user authorization, role mappings, and SSO across dashboards               |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Tenancy Principles
*   **Tenant Isolation**: Isolating workloads (using Kubernetes namespaces or networks) to prevent data access leaks or interference.
*   **Resource Quotas**: Defining compute limits to prevent any single tenant from exhausting resources.
*   **Cost Allocation**: Mapping resource usage statistics to tenants to calculate cost allocations.

---

## 2. Architecture Deep Dive

Multi-tenant platforms use namespaces for isolation:
*   **Kubernetes Namespaces**: Logical partitions inside the cluster that isolate deployments and services.
*   **Istio VirtualServices**: Manage request routing and enforce identity checks across namespaces.
*   **Keycloak Identity Provider**: Integrates with dashboards and gateways to enforce user roles.

---

## 3. Internal Working

### Resource Allocation Validation
1.  **Request Workload**: A developer submits a model training deployment manifest.
2.  **Quota Verification**: The Kubernetes controller compares requested resources against the namespace's resource quota.
3.  **Deploy Pod**: If within limits, the pod is scheduled on the assigned node slices.

---

## 4. Tool Comparison

| Feature | Namespace Isolation | Standalone Virtual Machines |
|---|---|---|
| **Resource Efficiency** | Very High (Shared kernel resources) | Low (Dedicated OS overhead) |
| **Isolation Strength** | Strong (Network/process boundaries) | Very Strong (Hardware virtualization) |
| **Startup Overhead** | Minimal (Pod startup seconds) | High (VM booting minutes) |

---

## 5. Installation Guide
Install Istio and Keycloak on a Kubernetes cluster:
```yaml
# istio_install.yaml (simulated configuration snippet)
# kubectl apply -f https://github.com/istio/istio/releases/download/1.18.0/istio.yaml
```

---

## 6. Setup Guide
Create a resource quota configuration manifest `quota.yaml`:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    requests.nvidia.com/gpu: "1"
```
Write this configuration to disk:
```bash
mkdir -p /tmp/tenancy-lab
tee /tmp/tenancy-lab/quota.yaml << 'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    requests.nvidia.com/gpu: "1"
EOF
```

---

## 7. Commands
```bash
# Create a tenant namespace
kubectl create namespace tenant-a || echo "Kubernetes offline"

# Apply resource quota configurations
kubectl apply -f /tmp/tenancy-lab/quota.yaml || echo "Kubernetes offline"

# View active quotas inside the namespace
kubectl get quota -n tenant-a || echo "Kubernetes offline"
```

---

## 8. Hands-On Labs
Verify the quota configuration file exists and is formatted correctly:
```bash
cat /tmp/tenancy-lab/quota.yaml | grep -i "requests.nvidia.com/gpu"
```

---

## 9. Production Operations

### Dynamic MIG Slicing Setup
In production clusters containing A100/H100 GPUs, configure the **GPU Operator** to dynamically partition card nodes based on namespace requirements:
```yaml
# Example GPU Operator MIG partitioning config
# config:
#   default: "all-1g.10gb"
```

---

## 10. Monitoring
Expose namespace-level resource consumption metrics to Prometheus, allowing teams to audit resource usage and calculate cost allocations.

---

## 11. Security
Enforce network policies to block inter-namespace network traffic, securing tenant data.

---

## 12. Cost Optimization
Configure autoscaling rules on tenant node groups to scale down resources during idle hours, optimizing compute costs.

---

## 13. Troubleshooting

### Task 13.1: Deployment Blocked by Quotas
*   **Symptom**: Pod deployments fail with `Forbidden: ... exceeded quota`.
*   **Root Cause**: The pod requests exceed the namespace's resource quota limits.
*   **Resolution Strategy**:
    *   Verify the namespace's active resource quotas and limits.
    *   Optimize the deployment resource configurations to fit within limits, or request a quota increase.

---

## 14. Enterprise Case Studies

### Platform Scaling at Uber
Uber Michelangelo uses multi-tenant partitions to serve teams. By isolating compute allocations and tracking resource consumption metrics, they prevent resource exhaustion and audit costs.

---

## 15. Interview Questions

### Q1: What is a Resource Quota, and why is it critical for multi-tenant systems?
*   **Answer**: A Resource Quota defines compute limits (such as CPUs, memory, or GPUs) for a namespace, preventing any single tenant from exhausting resources and ensuring system stability.

### Q2: Explain the difference between logical and hardware isolation in multi-tenant systems.
*   **Answer**:
    *   **Logical Isolation**: Isolating workloads using namespaces or network policies. Efficient but shares kernel resources.
    *   **Hardware Isolation**: Slicing physical hardware (e.g., MIG) to isolate compute and memory resources. Secure but less flexible.

---

## 16. AI FDE Perspective

### Deploying Multi-Tenant Platforms in Air-Gapped Clusters
As an AI Forward Deployed Engineer (FDE), you often configure model serving layers:
*   **Local Identity Management**: Deploy **Keycloak** local instances to manage authentication and user roles within the private network:
    ```bash
    # Run Keycloak container local setup
    # docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
    ```
This ensures secure user access without needing external network connections.

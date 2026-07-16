# Project 8: Multi-Tenant AI SaaS Platform (AWS EKS & Istio)

## 1. Theory (20%)

### Business Problem
SaaS platforms serving corporate clients must isolate tenant workloads and data to satisfy security compliance, while optimizing infrastructure usage to minimize costs.

```
+-------------------------------------------------------------------------------------------------+
|                                      EKS Multi-Tenancy                                          |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Istio Ingress Gateway                                  |   |
|   |   - Inspects client headers (e.g. X-Tenant-ID) and routes queries to namespaces        |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Route)                                         v (Route)               |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |             Namespace: bank-a           |     |             Namespace: bank-b           |   |
|   |   - Isolated serving pods (FastAPI)     |     |   - Isolated serving pods (FastAPI)     |   |
|   |   - Resource quota bounds (CPU/VRAM)    |     |   - Resource quota bounds (CPU/VRAM)    |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Log usage)                                    |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Billing Database                                    |   |
|   |   - Tracks monthly tenant usage metrics for Stripe billing integration                    |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Shared Clusters vs Dedicated Clusters**: Dedicated clusters for each client provide maximum isolation but are expensive. We select a Shared Cluster model using Kubernetes Namespaces and Resource Quotas to isolate workloads, optimizing resource usage.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Ingress Gateway (Istio)**: Inspects request headers and routes traffic to tenant namespaces.
2.  **Isolated Workspaces**: Tenant workloads run in dedicated namespaces with resource limits.
3.  **Billing Collector**: Tracks token usage metrics for billing.

---

## 3. Implementation (30%)

### Code Structure
```
tenant_platform/
├── app/
│   ├── api/
│   │   └── billing.py       # Manages tenant billing records
│   ├── services/
│   │   └── router.py        # Validates headers and routes requests
│   └── main.py              # Application entry point
```

### Ingress & Billing Router API
```python
# app/main.py
from fastapi import FastAPI, Header, HTTPException
import sys

app = FastAPI(title="Multi-Tenant Router API")

@app.post("/api/v1/tenant/route")
def route_tenant_call(x_tenant_id: str = Header(None)):
    print(f"Ingress Gateway - Validating headers for tenant ID: '{x_tenant_id}'")
    
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing required X-Tenant-ID header.")
        
    valid_tenants = ["bank-a", "bank-b", "bank-c"]
    if x_tenant_id not in valid_tenants:
        raise HTTPException(status_code=403, detail="Unauthorized tenant ID.")
        
    # Route request details
    return {
        "tenant_id": x_tenant_id,
        "target_namespace": f"ns-{x_tenant_id}",
        "database_schema": f"{x_tenant_id}_db_schema",
        "routing_status": "SUCCESS"
    }
```

---

## 4. DevOps & Operations (15%)

### Kubernetes Namespaces & Quotas
Configure Resource Quotas in tenant namespaces to prevent "noisy neighbors" from hogging cluster resources:
```yaml
# quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
  namespace: ns-bank-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

---

## 5. AI FDE Perspective (15%)

### Discovery & ROI
*   **Discovery Question**: "What data isolation standards do your clients require?" (Determines the database multi-tenancy model).
*   **Adoption Strategy**: Implement self-service workspaces with pre-configured access rights to accelerate tenant onboarding.
*   **ROI Metric**: Reduce tenant onboarding timelines from weeks to minutes.

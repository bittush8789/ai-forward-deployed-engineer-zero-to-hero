# Module 8: Multi-Tenant AI SaaS Platforms, Data Isolation & Metering

## 1. Theory (60%)

### What is Multi-Tenancy?
Multi-Tenancy is an architectural model where a single software instance serves multiple customers (tenants) while isolating their data and configurations.

```
+-------------------------------------------------------------------------------------------------+
|                                        Multi-Tenant Models                                      |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |  Shared Database  |      |  Separate Schema  |      | Separate Database |                   |
|   | (Tenant ID Column)|      |  (Tenant Schema)  |      | (Isolated Nodes)  |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|    Simple but risk of        Moderate isolation         Strongest isolation                     |
|    accidental exposure       in a shared database       but high hosting cost                   |
+-------------------------------------------------------------------------------------------------+
```

### Database Multi-Tenancy Models
*   **Shared Database (Logical Isolation)**: All tenants share the same database tables. Data is isolated using a `tenant_id` column. Simple to manage but carries a risk of accidental data exposure.
*   **Separate Schema**: Tenants share the database server but have dedicated schemas. Moderate isolation.
*   **Separate Database (Physical Isolation)**: Each tenant has a dedicated database server, providing the strongest isolation but at higher hosting costs.

### System Isolation Levels
*   **Data Isolation**: Encrypting and restricting access to tenant databases and files.
*   **Compute Isolation**: Running tenant workloads in dedicated namespaces or node groups to prevent resource contention.
*   **Network Isolation**: Enforcing network policies to block traffic between tenant namespaces.

### Platform Security
*   **Authentication (SSO)**: Enforcing Single Sign-On (SSO) using identity providers (like Keycloak).
*   **Access Control (RBAC)**: Enforcing role-based access policies to control user permissions.
*   **Audit Logging**: Logging all user interactions and state changes to maintain compliance.

### Usage Metering & Billing
*   Tracking tenant token consumption and compute usage to calculate billing allocations and enforce resource quotas.

---

## 2. Practical (40%)

### Build: Enterprise AI SaaS Platform
We will design a multi-tenant platform to serve three banking clients (**Bank A**, **Bank B**, **Bank C**):
1.  **Kubernetes Namespaces**: Running tenant workloads in isolated namespaces (`bank-a`, `bank-b`, `bank-c`).
2.  **Separate Databases**: Deploying dedicated PostgreSQL instances for each tenant.
3.  **Tenant Ingress**: Configuring Istio virtual services to route traffic to the appropriate namespace based on the client ID header.
4.  **Keycloak SSO**: Enforcing token validation and tenant role mapping.
5.  **Token Metering**: Using Redis to track token consumption for billing.

```
+-------------------------------------------------------------------------------------------------+
|                                      SaaS Platform Topology                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Istio Ingress Gateway                                  |   |
|   |   - Inspects client headers and routes traffic to the target namespace                  |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       | (Tenant Header: Bank A)                         | (Tenant Header: Bank B) |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |               Namespace: bank-a         |     |               Namespace: bank-b         |   |
|   |   - Serving API (FastAPI)               |     |   - Serving API (FastAPI)               |   |
|   |   - Database (PostgreSQL Schema A)      |     |   - Database (PostgreSQL Schema B)      |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Log usage)                                    |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Redis Cache                                         |   |
|   |   - Tracks tenant token consumption in real-time to enforce billing quotas              |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Hands-On Task: Tenant Traffic Routing Script
Write a Python script simulating an API gateway that validates headers and routes traffic to tenant namespaces:
```python
# /tmp/tenant_router.py
import sys

def route_tenant_request(headers: dict):
    print("=== Processing Incoming Client Request ===")
    
    # 1. Extract tenant ID from headers
    tenant_id = headers.get("X-Tenant-ID")
    if not tenant_id:
        print("Block: Missing X-Tenant-ID header. Rejecting request.")
        sys.exit(1)
        
    # 2. Simulate validation against database
    valid_tenants = ["bank-a", "bank-b", "bank-c"]
    if tenant_id not in valid_tenants:
        print(f"Block: Invalid Tenant ID '{tenant_id}'. Rejecting request.")
        sys.exit(2)
        
    # 3. Route request to target namespace
    print(f"Routing request to Kubernetes Namespace: '{tenant_id}'")
    print(f"Enforcing isolated DB connections for {tenant_id}.")
    print("==========================================\n")
    sys.exit(0)

if __name__ == '__main__':
    # Test valid tenant routing
    route_tenant_request({"X-Tenant-ID": "bank-a"})
```
Run the routing validation:
```bash
python3 /tmp/tenant_router.py
```

### Case Study: Salesforce Custom Database Schema
Salesforce uses a single, shared database engine to serve millions of tenants. By using metadata tables and runtime query rewrites that automatically append tenant filters, they enforce data isolation while keeping database maintenance simple.

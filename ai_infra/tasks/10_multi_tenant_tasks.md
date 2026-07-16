# Practice Tasks: Module 10 - Tenant Quota Management

This document outlines step-by-step tasks to configure namespace resource limits for tenant isolation.

---

## Task 1: Create Resource Quota Config
*   **Goal**: Create a configuration defining compute boundaries for a tenant namespace.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `tenant_limits.yaml`:
       ```yaml
       tee /tmp/tenant_limits.yaml << 'EOF'
       apiVersion: v1
       kind: ResourceQuota
       metadata:
         name: tenant-quota
         namespace: tenant-a
       spec:
         hard:
           requests.cpu: "2"
           requests.memory: 4Gi
           requests.nvidia.com/gpu: "1"
       EOF
       ```
*   **Verification**:
    Verify the resource quota limits are configured:
    ```bash
    cat /tmp/tenant_limits.yaml | grep -i "requests.nvidia.com/gpu"
    ```

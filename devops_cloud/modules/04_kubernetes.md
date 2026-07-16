# Module 4: Production Kubernetes Infrastructure

## 1. Architecture Deep Dive

Kubernetes is a declarative, state-reconciliation system designed to orchestrate containerized applications. It separates cluster operations into the **Control Plane** and **Worker Nodes**.

```
+---------------------------------------------------------------------------------------------------+
|                                           Control Plane                                           |
|   +-------------------------------------------------------------------------------------------+   |
|   |                                    kube-apiserver                                         |   |
|   |    - Exposes the REST API, validates configuration, and updates state                     |   |
|   +----+-------------------|---------------------------------|---------------------------+----+   |
|        |                   |                                 |                           |        |
|        v (Read/Write)      v                                 v                           v        |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
|   |    etcd    |  |  kube-scheduler |               |kube-controller-manager|  |cloud-controller| |
|   | - KV store |  | - Places pods   |               | - Enforces state      |  |  - Integrates  | |
|   | - Raft     |  |   on nodes      |               |   (Deployment, etc.)  |  |    cloud API   | |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
+--------|-------------------|---------------------------------|---------------------------|--------+
         |                   | (APIs over HTTPS)               |                           |
         |                   +------------------+--------------+                           |
         |                                      |                                          |
         v (Node communication)                 v                                          v
+--------|--------------------------------------|------------------------------------------|--------+
|        |                                 Worker Nodes                                    |        |
|   +----v-------+                         +----v-------+                             +----v---+    |
|   |   kubelet  |                         | kube-proxy |                             | Container|  |
|   | - Node agent|                        | - IPVS/    |                             | Runtime|    |
|   | - Runs pods|                         |   Iptables |                             | (cri-o)|    |
|   +------------+                         +------------+                             +--------+    |
+---------------------------------------------------------------------------------------------------+
```

### Control Plane Components
*   **kube-apiserver**: The central gatekeeper. All components (kubectl, scheduler, controllers) communicate solely with the API server over HTTPS. It writes state to etcd.
*   **etcd**: A distributed, consistent key-value store. It serves as the single source of truth for the entire cluster.
*   **kube-scheduler**: Watches for newly created Pods with no assigned node, and selects the best node based on resource constraints, affinity/anti-affinity rules, and taints.
*   **kube-controller-manager**: Runs controller processes in a continuous loop to reconcile the actual state of the cluster with the desired state (e.g., ensuring the correct number of pods are running).

### Worker Node Components
*   **kubelet**: An agent that runs on each node in the cluster. It ensures that containers described in PodSpecs are running and healthy.
*   **kube-proxy**: Manages network routing rules on nodes. It operates in two main modes:
    *   *iptables mode*: Sequential evaluation of rules. High latency when scaling to thousands of services.
    *   *IPVS mode*: Uses hash tables. High performance, routing scale-independent connection processing.
*   **Container Runtime**: The engine that runs containers (e.g., `containerd` or `CRI-O`).
*   **Container Network Interface (CNI)**: Allocates IP addresses to pods and routes traffic between them (e.g., Calico, Flannel, Cilium).

---

## 2. Internal Working

### Pod Lifecycle
A Pod moves through distinct phases:
1.  **Pending**: The Pod API object has been created in etcd, but it has not been scheduled or its images are still downloading.
2.  **Running**: The Pod has been bound to a node, and all containers have been created. At least one container is currently starting or running.
3.  **Succeeded**: All containers in the Pod have terminated successfully (exit code 0) and will not be restarted.
4.  **Failed**: All containers have terminated, and at least one container has exited with a non-zero status.
5.  **Unknown**: The API server cannot communicate with the node's kubelet (typically due to a network partition).

### Service Discovery & CoreDNS
*   **Service Abstraction**: Pods are ephemeral. A `Service` provides a stable IP address (ClusterIP) and DNS entry.
*   **CoreDNS**: Acts as the cluster DNS server. When a pod makes a request to `my-service.my-namespace.svc.cluster.local`, CoreDNS resolves it to the service's ClusterIP.
*   **Routing**: `kube-proxy` configures the host kernel's packet filtering (IPVS or iptables) to intercept traffic to the ClusterIP and load-balance it across the service's active Pod endpoints.

---

## 3. Production Use Cases

### High-Availability Web Services
Deploying web APIs across multiple availability zones using deployments, services, ingress, and horizontal autoscaling to handle variable user traffic without downtime.

### GPU-Enabled Model Serving
Orchestrating model inference pods (e.g., vLLM or Triton) on dedicated GPU node pools. Pods are assigned using tolerations and node affinity to avoid running standard CPU workloads on expensive GPU hardware.

---

## 4. Security Best Practices

### Role-Based Access Control (RBAC)
Enforce the principle of least privilege. Do not use admin credentials for CI/CD pipelines. Create service accounts with limited access.
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### Network Policies
By default, all pods can talk to all other pods in a Kubernetes cluster. Use network policies to isolate sensitive database workloads from frontend pods.

---

## 5. Scalability Patterns

### Autoscaling
*   **Horizontal Pod Autoscaler (HPA)**: Scales the number of pod replicas based on CPU, memory, or custom Prometheus metrics.
*   **Cluster Autoscaler (CA)**: Automatically adds or removes nodes from the cluster when pods cannot schedule due to resource shortages.
*   **Karpenter**: A modern alternative to Cluster Autoscaler. It provisions right-sized nodes in seconds based on pending pod requirements, bypassing cloud provider node group limitations.

---

## 6. Reliability Patterns

### Probes
*   **Startup Probe**: Checks if the application inside the container has started. Other probes are disabled until this succeeds.
*   **Liveness Probe**: Determines if the container needs to be restarted. If it fails, kubelet kills the container and applies the restart policy.
*   **Readiness Probe**: Determines if a container is ready to accept network traffic. If it fails, the endpoints controller removes the pod's IP from all matching services.

### Pod Disruption Budgets (PDB)
PDBs limit the number of pods that can be down simultaneously during voluntary disruptions (like node upgrades or draining):
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: api-server
```

---

## 7. Cost Optimization

### Resource Requests & Limits Right-Sizing
*   **Requests**: What the scheduler uses to place pods. Under-provisioning requests causes resource starvation. Over-provisioning leads to low node utilization and wasted cloud spend.
*   **Limits**: The maximum resources a pod can consume. If a pod exceeds its memory limit, it is OOM killed.
*   **Recommendation**: Use the Vertical Pod Autoscaler (VPA) in recommendation mode to monitor real-world utilization and adjust resource settings.

---

## 8. Hands-On Labs

### Lab 8.1: Multi-Replica Application Deployment
We will deploy a 3-replica Python API service.
```yaml
# flask-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  labels:
    app: flask-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api
        image: python:3.11-slim
        command: ["python", "-m", "http.server", "8080"]
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  selector:
    app: flask-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```
Apply commands:
```bash
kubectl apply -f flask-deployment.yaml
kubectl get deployments
kubectl get pods -o wide
```

### Lab 8.2: NGINX Ingress & TLS Setup
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: api.enterprise.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 80
```
Apply:
```bash
kubectl apply -f ingress.yaml
```

### Lab 8.3: ConfigMap & Secret Integration
```yaml
# config-secret.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DB_HOST: "postgres-service.database.svc.cluster.local"
  LOG_LEVEL: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  # Value: supersecretpassword (base64 encoded)
  DB_PASSWORD: c3VwZXJzZWNyZXRwYXNzd29yZA==
```
Mounting these into the Deployment:
```yaml
# Fragment to add under container spec
env:
  - name: DATABASE_HOST
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: DB_HOST
  - name: DATABASE_PASS
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: DB_PASSWORD
```

### Lab 8.4: HPA CPU-Based Autoscaling
```bash
# 1. Autoscale the deployment when CPU usage exceeds 50%
kubectl autoscale deployment flask-api --cpu-percent=50 --min=3 --max=10

# 2. View active HPAs
kubectl get hpa
```

### Lab 8.5: Pod Interrogation & Troubleshooting
```bash
# Get detailed description of a pod (events, scheduling decisions, issues)
kubectl describe pod -l app=flask-api

# View container output logs
kubectl logs -l app=flask-api --tail=100

# Open an interactive shell inside a running container
kubectl exec -it $(kubectl get pods -l app=flask-api -o jsonpath='{.items[0].metadata.name}') -- /bin/sh
```

### Lab 8.6: Resource Limit Enforcement
```yaml
# Spec limit validation
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### Lab 8.7: Cluster Node Pressure Diagnostics
```bash
# Check CPU/Memory utilization of all worker nodes
kubectl top nodes

# Check resource consumption of all running pods
kubectl top pods -A
```

### Lab 8.8: Rolling Update & Rollback execution
```bash
# 1. Update the image of a deployment
kubectl set image deployment/flask-api flask-api=python:3.11-alpine

# 2. Monitor rolling update status
kubectl rollout status deployment/flask-api

# 3. View rollout history
kubectl rollout history deployment/flask-api

# 4. Rollback to the previous version
kubectl rollout undo deployment/flask-api
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Pod Stuck in Pending
*   **Symptom**: `kubectl get pods` shows a pod in the `Pending` state indefinitely.
*   **Root Cause**: The scheduler cannot find a node that satisfies the pod's resource requests, node selectors, taints, or affinity rules.
*   **Resolution Strategy**:
    ```bash
    # 1. Inspect the events section at the bottom of the output
    kubectl describe pod <pending-pod-name>
    
    # Common messages:
    # "0/3 nodes are available: 3 Insufficient cpu." -> Scale cluster or reduce requests.
    # "1 node(s) had untolerated taint" -> Add matching toleration or target different node.
    ```

### Task 9.2: Pod Stuck in CrashLoopBackOff
*   **Symptom**: Pod starts, runs for a few seconds, terminates, and repeats the cycle.
*   **Root Cause**: The application inside the container is crashing on startup. Common causes include missing environment variables, configuration errors, or database connection failures.
*   **Resolution Strategy**:
    ```bash
    # 1. Retrieve the logs of the crashed container
    kubectl logs <pod-name>
    
    # 2. If it crashed before logging, view logs of the previous instance
    kubectl logs <pod-name> --previous
    
    # 3. Check for structural command issues
    kubectl describe pod <pod-name>
    ```

### Task 9.3: Service Unreachable (No Endpoints)
*   **Symptom**: Traffic to the service IP times out, or returns a 503 error.
*   **Root Cause**: The service selector does not match the labels on any running pods, or the pods are failing their readiness probes.
*   **Resolution Strategy**:
    ```bash
    # 1. Check if the Service has active endpoints mapped to it
    kubectl get endpoints <service-name>
    
    # 2. If endpoints list is empty, verify service selector labels match pod labels:
    kubectl get pods --show-labels
    
    # 3. Verify pods are running and healthy (ready status should be 1/1, not 0/1)
    kubectl get pods
    ```

---

## 10. Real Production Incidents

### Case Study: Cascading Readiness Probe Failure
*   **Incident**: An e-commerce API service experienced a sudden spike in traffic. The load caused response times to slow down. The readiness probe, configured with a short timeout (1s) and high failure threshold, began to fail.
*   **Cascading Effect**: Kubernetes removed the "unhealthy" pods from the service endpoint list. This routed all traffic to the remaining healthy pods, overloading them and causing their readiness probes to fail too. Within minutes, all pods were removed from the service, resulting in a complete outage.
*   **Remediation**:
    *   Optimized readiness probe configurations to decouple health status from response latency (checking a lightweight static endpoint like `/healthz` rather than running a heavy database query).
    *   Tuned timeouts and failure thresholds to prevent rapid endpoint removal.
    *   Configured HPAs to trigger autoscaling before CPU saturation hit readiness thresholds.

---

## 11. Interview Questions

### Q1: Explain the control plane reconciliation loop.
*   **Answer**: Kubernetes uses controller loops to reconcile the actual state of the cluster with the desired state specified in manifests.
    *   The controller queries the API server for the current state of a resource (e.g., how many replicas of a pod are running).
    *   It compares this with the desired state (e.g., replica count set to 3).
    *   If they don't match, the controller makes API calls to create or delete resources to align the states.
    *   The loop repeats continuously.

### Q2: What is the difference between iptables and IPVS routing modes in kube-proxy?
*   **Answer**:
    *   **iptables mode**: `kube-proxy` writes sequential firewall rules for every service in the cluster. The kernel evaluates these rules one-by-one. In large clusters with thousands of services, packet filtering slows down.
    *   **IPVS mode**: Uses IP Virtual Server, a transport-layer load-balancing mechanism built into the Linux kernel. It stores routing rules in efficient hash tables, ensuring high-performance routing that is independent of service scale.

### Q3: How do you perform a safe backup and restore of an etcd cluster?
*   **Answer**:
    *   **Backup**: Use `etcdctl` to capture a snapshot of the database state:
        ```bash
        ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
          --cacert=/etc/kubernetes/pki/etcd/ca.crt \
          --cert=/etc/kubernetes/pki/etcd/server.crt \
          --key=/etc/kubernetes/pki/etcd/server.key \
          snapshot save /tmp/etcd-backup.db
        ```
    *   **Restore**: Stop the API server and restore the snapshot onto the etcd nodes:
        ```bash
        ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
          --data-dir=/var/lib/etcd-from-backup
        ```
        Then, update etcd configuration to point to the new data directory and restart the API server.

### Q4: Why does a StatefulSet require a Headless Service?
*   **Answer**: A Headless Service (a Service with `clusterIP: None`) does not assign a ClusterIP. Instead, it returns the A records (IPs) of all matching pods directly via DNS.
    *   This is required for StatefulSets because each pod has a stable network identity (e.g., `pod-0`, `pod-1`).
    *   It allows clients or cluster peers to communicate directly with specific members of the StatefulSet (critical for database clusters like Cassandra or Elasticsearch to form quorums), rather than routing through a random load balancer.

### Q5: How do CNI plugins implement overlay networking?
*   **Answer**: CNI plugins create a virtual network overlaying the physical network.
    *   Each pod gets a unique IP address across the cluster.
    *   When pod A on node 1 sends a packet to pod B on node 2, the CNI encapsulates the packet (using protocols like VXLAN or Geneve) inside a host-level network packet.
    *   This packet is sent across the physical host network to node 2, where the CNI decapsulates it and delivers the original packet to pod B.

---

## 12. Enterprise Case Studies

### Scaling Kubernetes at OpenAI
OpenAI operates massive Kubernetes clusters to train deep learning models. Their workloads stretch the limits of standard Kubernetes scheduling, often scaling to over 7,500 nodes.
*   **etcd Scaling**: They optimized etcd disk I/O performance using local NVMe drives to prevent control plane bottlenecks during massive pod deployments.
*   **Custom Scheduler**: They customized scheduler behaviors to handle heavy GPU requirements and enforce strict physical node-affinity rules, ensuring model training steps execute with minimal latency.

---

## 13. System Design Discussions

### Secure, Multi-Tenant EKS Cluster Architecture
*   **Objective**: Design a secure, production-ready AWS EKS cluster.
*   **Architecture Considerations**:
    *   **Network Isolation**: Deploy EKS control plane endpoints in private subnets. Disable public API endpoints; require access via an AWS Bastion Host or VPN connection.
    *   **Compute Isolation**: Group workloads into dedicated Node Groups using AWS EC2 Auto Scaling Groups. Assign stateful databases to high-I/O node groups, and stateless APIs to spot instance groups.
    *   **IAM Integration**: Use EKS Pod Identities or IAM Roles for Service Accounts (IRSA) to assign AWS permissions to specific pods, avoiding hardcoded AWS access keys inside container images.
    *   **Security Standards**: Deploy network policies using the Amazon VPC CNI to restrict traffic between namespaces.

---

## 14. AI Platform Perspective

### Scheduling GPU Inference Workloads
Running large language models requires scheduling workloads on GPU-enabled nodes.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llama-inference
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: llama-inference
    spec:
      containers:
      - name: vllm-engine
        image: vllm/vllm-openai:latest
        resources:
          limits:
            nvidia.com/gpu: "1" # Request 1 physical GPU
            memory: "16Gi"
            cpu: "4"
      # Toleration allows running on GPU-tainted nodes
      tolerations:
      - key: "sku"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
      # Affinity ensures the pod lands on H100 hardware
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: "nvidia.com/gpu.product"
                operator: "In"
                values:
                - "NVIDIA-H100-SXM5-80GB"
```
The node selector/affinity restricts the workload to NVIDIA H100 GPU nodes. The toleration allows the pod to be scheduled on those nodes, which are tainted to prevent standard CPU workloads from using their resources.

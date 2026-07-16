# Module 9: Declarative Continuous Delivery with ArgoCD

## 1. Architecture Deep Dive

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It monitors Git repositories containing desired infrastructure state and reconciles it with live Kubernetes clusters.

```
+---------------------------------------------------------------------------------------------------+
|                                          Git Repository                                           |
|   - Contains Kubernetes manifests, Helm charts, or Kustomize templates                            |
|   - Serves as the single source of truth                                                          |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (Webhook / 3-minute Polling loop)
+------------------------------------+--------------------------------------------------------------+
|                                           ArgoCD                                                  |
|   +-------------------------------------------------------------------------------------------+   |
|   |   Application Controller                                                                  |   |
|   |   - Compares desired state in Git against live cluster state                              |   |
|   |   - Identifies drift and executes sync operations to reconcile differences                |   |
|   +----+-------------------|---------------------------------|---------------------------+----+   |
|        |                   |                                 |                           |        |
|        v                   v                                 v                           v        |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
|   | API Server |  | Repo Server     |               | Redis Cache           |  | Dex Identity   | |
|   | - Web UI   |  | - Pulls Git     |               | - Stores manifest     |  | - Handles      | |
|   | - CLI API  |  |   manifests     |               |   rendered state      |  |   SSO / OIDC   | |
|   +------------+  +-----------------+               +-----------------------+  +----------------+ |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (Kubernetes APIs)
+------------------------------------+--------------------------------------------------------------+
|                                   Target Clusters                                                 |
|          Local Cluster / Namespace | Remote Production Cluster | Remote Staging Cluster            |
+---------------------------------------------------------------------------------------------------+
```

### ArgoCD Architectural Components
*   **argocd-server**: Exposes the Web UI, CLI interface, and API. It handles user authentication, RBAC policy enforcement, and project management.
*   **argocd-repo-server**: Maintains local caches of Git repositories. It compiles raw Kubernetes manifests, Helm templates, or Kustomize configurations into plain YAML.
*   **argocd-application-controller**: A Kubernetes operator that continuously monitors running applications, compares their live state against desired Git state, and executes sync actions to resolve drift.
*   **argocd-dex-server**: An integrated identity provider (Dex) that bridges authentication to external OAuth2/OIDC systems (such as Okta, GitHub, or Active Directory).

---

## 2. Internal Working

### Reconciliation Loop & Three-Way Diff
The Application Controller executes a continuous reconciliation loop:
1.  **Read desired state**: Queries `argocd-repo-server` to fetch the compiled manifests from Git.
2.  **Read live state**: Queries the destination cluster's API to fetch the active status of resources.
3.  **Perform Three-Way Diff**: Calculates differences between:
    *   The state stored in **Git** (Desired).
    *   The state returned by the **Kubernetes API** (Live).
    *   The state stored in **ArgoCD's cache** (representing the last synced state, which helps identify modifications made by Kubernetes admission controllers).
4.  If a drift is found, the application status changes to `OutOfSync`.

### Resource Tracking Mechanics
ArgoCD maps cluster resources to Git applications by injecting a tracking label or annotation:
*   Label: `app.kubernetes.io/instance: <application-name>`
*   Annotation: `argocd.argoproj.io/tracking-id: <application-name>:<group>/<kind>:<namespace>/<name>`

---

## 3. Production Use Cases

### GitOps Application Delivery
Automating the deployment of microservices by committing code changes to Git. Once a pull request is merged, ArgoCD pulls the changes and deploys them to target Kubernetes clusters without manual intervention.

### Configuration Drift Correction
Preventing unauthorized changes. If a user manually edits a deployment replica count in the Kubernetes dashboard, ArgoCD detects the drift and reverts the cluster state to match the configuration stored in Git.

---

## 4. Security Best Practices

### Multi-Tenant Project Isolation (Argo Projects)
Do not allow all applications to write to any namespace. Use `AppProjects` to restrict:
*   Destination clusters and namespaces.
*   The types of resources that can be deployed (e.g., blocking ClusterRoles or Namespaces).
*   Git source repositories.

### RBAC SSO Integration
Map identity groups to ArgoCD roles using Dex policies:
```ini
# argocd-rbac-cm configmap
g, MLOps-Team, role:admin
g, Frontend-Devs, role:readonly
```

---

## 5. Scalability Patterns

### The App-of-Apps Pattern
Instead of manually creating individual applications in the UI, define a root Application that points to a directory containing other Application manifests. This allows managing all cluster workloads through a single root configuration.

### ApplicationSets
Automate application generation across multiple clusters and environments using templates and generators (such as Git directory generators or Cluster generators):
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: web-appset
spec:
  generators:
    - list:
        elements:
          - cluster: staging-cluster
            url: https://10.0.0.10:6443
          - cluster: prod-cluster
            url: https://10.0.0.20:6443
  template:
    metadata:
      name: '{{cluster}}-web-app'
    # spec configurations...
```

---

## 6. Reliability Patterns

### Sync Policies (Self-Heal & Prune)
Configure automated recovery behaviors:
```yaml
syncPolicy:
  automated:
    prune: true     # Delete resources that are removed from the Git repository
    selfHeal: true  # Reapply Git configuration if live resources are modified manually
```

### Git Webhook Notifications
By default, ArgoCD polls Git repositories every 3 minutes. For instant deployments, configure webhooks in GitHub/GitLab to notify ArgoCD immediately on commit:
*   Payload URL: `https://<argocd-host>/api/webhook`

---

## 7. Cost Optimization

### Cleaning Up Orphaned Resources
Enable `prune` in sync policies. This ensures that when a service is removed from the Git repository, its running pods, services, and routing rules are deleted from the cluster, preventing orphaned resources and reducing cloud costs.

---

## 8. Hands-On Labs

### Lab 8.1: Installing ArgoCD
```bash
# 1. Create namespace
kubectl create namespace argocd

# 2. Apply official release manifests
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Expose the server API using port forwarding
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
```

### Lab 8.2: Retrieving Admin Password and CLI Login
```bash
# 1. Fetch autogenerated admin password
ADMIN_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode)
echo "Default password: $ADMIN_PASSWORD"

# 2. Login via CLI
argocd login localhost:8080 --username admin --password "$ADMIN_PASSWORD" --insecure

# 3. Update admin password
argocd account update-password
```

### Lab 8.3: Creating a GitOps Application
Create an application that pulls manifests from a public repo.
```yaml
# app-dev.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/argoproj/argocd-example-apps.git'
    targetRevision: HEAD
    path: guestbook
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
Apply commands:
```bash
kubectl apply -f app-dev.yaml
argocd app get guestbook-dev
```

### Lab 8.4: Sync Strategy Modifications
```bash
# Set manual sync status check
argocd app set guestbook-dev --sync-policy none

# Re-enable auto-sync with self-heal and pruning
argocd app set guestbook-dev --sync-policy automated --auto-prune --self-heal
```

### Lab 8.5: Multi-Cluster Registration
Register a remote Kubernetes cluster with ArgoCD to manage deployments.
```bash
# 1. Fetch current kubeconfig contexts
kubectl config get-contexts

# 2. Register remote context (e.g., target-staging)
argocd cluster add target-staging
```

### Lab 8.6: Performing Rollbacks
If a deployment fails, you can roll back to a previous revision:
```bash
# 1. View history of revisions
argocd app history guestbook-dev

# 2. Rollback to revision 1 (disables auto-sync temporarily)
argocd app rollback guestbook-dev 1
```

### Lab 8.7: App-of-Apps Deployment
```yaml
# root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-application
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/gitops-infra-repo.git'
    targetRevision: HEAD
    path: apps # Contains application manifests pointing to frontend, backend, database
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: argocd
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Application Stuck in OutOfSync Loop
*   **Symptom**: ArgoCD constantly refreshes and displays `OutOfSync` status for a resource, even after running sync successfully.
*   **Root Cause**: Conflict between desired state in Git and mutation changes made in the cluster (such as mutating webhooks modifying defaults, or controllers like Horizontal Pod Autoscalers dynamically scaling replicas).
*   **Resolution Strategy**:
    *   Inspect the diff in the ArgoCD UI to identify the conflicting attribute.
    *   Configure ArgoCD to ignore the specific attribute in the application definition:
        ```yaml
        spec:
          ignoreDifferences:
            - group: apps
              kind: Deployment
              jsonPointers:
                - /spec/replicas # Ignore replica changes managed by HPA
        ```

### Task 9.2: Git Connection Timeouts
*   **Symptom**: Application displays a warning: `ComparisonError: rpc error: code = Unknown desc = error clone: ... Connection timed out`.
*   **Root Cause**: The repository server cannot connect to the Git URL due to missing credentials, proxy settings, or network routing issues.
*   **Resolution Strategy**:
    *   Verify repository credentials (SSH key or Personal Access Token):
        ```bash
        argocd repo add git@github.com:my-org/my-repo.git --ssh-private-key-path ~/.ssh/id_ed25519
        ```
    *   Check repo-server logs to diagnose connectivity:
        ```bash
        kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server -c argocd-repo-server
        ```

### Task 9.3: Target Namespace Not Found
*   **Symptom**: Deployment fails with `Namespace target-namespace not found`.
*   **Root Cause**: The destination namespace does not exist in the target cluster, and the application is not configured to create it automatically.
*   **Resolution Strategy**:
    *   Create the namespace manually.
    *   *Alternative*: Configure the application sync policy to create the namespace automatically:
        ```yaml
        syncPolicy:
          syncOptions:
            - CreateNamespace=true
        ```

---

## 10. Real Production Incidents

### Case Study: The Auto-Pruning Outage
*   **Incident**: An operations engineer temporarily moved a folder containing database manifests out of the sync path in a Git repository to test Kustomize configuration changes. Because auto-pruning was enabled, ArgoCD deleted the production database StatefulSet and its matching PVC storage volumes, resulting in a 4-hour service outage.
*   **Remediation**:
    *   Updated the reclaim policy on production PersistentVolumes from `Delete` to `Retain`.
    *   Blocked critical resources (such as Namespaces, CRDs, and StatefulSets) from being pruned automatically using annotations:
        ```yaml
        metadata:
          annotations:
            argocd.argoproj.io/sync-options: Prune=false
        ```

---

## 11. Interview Questions

### Q1: What is GitOps, and what are its core principles?
*   **Answer**: GitOps is an operational framework that takes DevOps best practices (such as version control, collaboration, compliance, and CI/CD) and applies them to infrastructure automation.
    *   **Declarative system definition**: The desired state of the system is defined in Git.
    *   **Versioned desired state**: Changes are proposed and approved in Git.
    *   **Automated state delivery**: Approved changes are applied to the system automatically.
    *   **Continuous state reconciliation**: Tools monitor the system and revert any changes that deviate from the configuration stored in Git.

### Q2: How does ArgoCD calculate differences between Git and running clusters?
*   **Answer**: The repository server pulls manifests from Git and compiles them into raw YAML. The controller fetches the live state of these resources from the cluster and uses a three-way diff calculation to identify differences. It ignores modifications made by admission controllers using cache metadata.

### Q3: What is the difference between Auto-Sync and Self-Heal in ArgoCD?
*   **Answer**:
    *   **Auto-Sync**: Automatically applies changes to the cluster when new commits are merged into the monitored Git branch.
    *   **Self-Heal**: Re-applies the Git configuration to the cluster if a resource is modified manually (creating drift) inside the cluster.

### Q4: Explain the App-of-Apps deployment pattern.
*   **Answer**: The App-of-Apps pattern allows managing multiple applications through a single root configuration. You define a root ArgoCD Application that points to a directory in a Git repository. This directory contains manifests for other Application resources (which point to services like frontend, backend, or databases). Applying the root Application deploys and tracks all other applications.

### Q5: How do you register private Git repositories in ArgoCD?
*   **Answer**: You can register private repositories using the ArgoCD UI, CLI, or by declaring Kubernetes Secrets in the `argocd` namespace. The secrets must include specific labels:
    ```yaml
    metadata:
      labels:
        argocd.argoproj.io/secret-type: repository
    ```
    The secret data contains the repository URL and access credentials (such as an SSH private key or HTTPS access token).

---

## 12. Enterprise Case Studies

### GitOps Migration at Ticketmaster
Ticketmaster migrated its deployment pipelines from traditional Jenkins push steps to ArgoCD GitOps configurations. They centralized cluster management and reduced deployment errors. By storing cluster configurations in Git repositories, operations teams can audit changes and deploy applications across multiple staging and production clusters.

---

## 13. System Design Discussions

### Designing a Centralized Multi-Tenant GitOps Platform
*   **Objective**: Design a centralized GitOps CD platform managing deployments across thousands of clusters.
*   **Architecture Considerations**:
    *   **Scalability**: Deploy ArgoCD in a management cluster. Offload workload reconciliation using controller sharding to distribute cluster tasks across multiple pods.
    *   **Security**: Implement the principle of least privilege using AppProjects. Limit access to target cluster namespaces and prevent repositories from deploying cluster-wide resources (like ClusterRoles or CRDs).
    *   **OIDC Integration**: Connect Dex authentication to Okta or Active Directory groups.

---

## 14. AI Platform Perspective

### GitOps for MLOps: Deploying Triton Inference Clusters
GitOps simplifies managing machine learning infrastructure by tracking deployments (like Triton Inference Server, Ray, or MLflow) in Git repositories.

```yaml
# GitOps Application to deploy Triton Inference Server
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: triton-serving-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/mlops-manifests.git'
    targetRevision: main
    path: base/triton-server
    helm:
      values: |
        replicaCount: 5
        modelRepositoryPath: "s3://my-prod-models/v1"
        resources:
          limits:
            nvidia.com/gpu: 2
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: ml-serving
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
This allows MLOps teams to manage model repository paths, replica counts, and GPU limits through pull requests, ensuring deployment changes are reviewed and audited.

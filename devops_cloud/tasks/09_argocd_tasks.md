# Practice Tasks: Module 9 - ArgoCD GitOps

This document outlines step-by-step tasks to practice ArgoCD Application provisioning, sync policies, and self-healing deployments.

---

## Task 1: Application Sync Configuration
*   **Goal**: Deploy an ArgoCD Application using manifests stored in a public Git repository.
*   **Step-by-Step Instructions**:
    1. Verify your connection to the Kubernetes cluster and that the `argocd` namespace is running.
    2. Create a local file named `argocd-app.yaml`:
       ```yaml
       apiVersion: argoproj.io/v1alpha1
       kind: Application
       metadata:
         name: live-guestbook
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
       Write this file to disk:
       ```bash
       mkdir -p /tmp/argocd-lab
       tee /tmp/argocd-lab/argocd-app.yaml << 'EOF'
       apiVersion: argoproj.io/v1alpha1
       kind: Application
       metadata:
         name: live-guestbook
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
       EOF
       ```
    3. Deploy the application configuration to your cluster:
       ```bash
       kubectl apply -f /tmp/argocd-lab/argocd-app.yaml
       ```
*   **Verification**:
    Verify the application status has transitioned to synced and healthy:
    ```bash
    kubectl get applications -n argocd live-guestbook
    kubectl get pods -l app=guestbook
    ```

---

## Task 2: Self-Healing and Drift Rectification
*   **Goal**: Manually edit the deployment inside Kubernetes and verify ArgoCD automatically reverts the drift back to the Git source configuration.
*   **Step-by-Step Instructions**:
    1. Manually scale down the guestbook deployment using `kubectl`:
       ```bash
       kubectl scale deployment guestbook-ui --replicas=0
       ```
    2. Immediately verify the replica count is updated in Kubernetes:
       ```bash
       kubectl get deployment guestbook-ui
       ```
    3. Monitor ArgoCD logs. The Application Controller should detect the drift and scale the deployment back up to match the Git configuration (typically 1 replica).
*   **Verification**:
    Wait 10-20 seconds and check the replica count. It should be restored:
    ```bash
    kubectl get deployment guestbook-ui
    ```
    Clean up the application:
    ```bash
    kubectl delete -f /tmp/argocd-lab/argocd-app.yaml
    ```

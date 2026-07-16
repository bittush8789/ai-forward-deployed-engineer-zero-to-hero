# Practice Tasks: Module 5 - Helm Packaging

This document outlines step-by-step tasks to practice Helm chart creation, values configuration, deployment overrides, and rollback options.

---

## Task 1: Scaffolding a Custom Chart
*   **Goal**: Create a new Helm chart, configure dependencies, and lint templates.
*   **Step-by-Step Instructions**:
    1. Open a terminal and run `helm create` to scaffold a chart:
       ```bash
       cd /tmp
       helm create helm-app-demo
       ```
    2. Edit the default metadata file `Chart.yaml`:
       ```bash
       nano helm-app-demo/Chart.yaml
       ```
       Update values to reflect application details (e.g., version, description).
    3. Add a dependency configuration for Redis in `Chart.yaml`:
       ```yaml
       dependencies:
         - name: redis
           version: 17.0.0
           repository: https://charts.bitnami.com/bitnami
       ```
    4. Fetch the dependency packages:
       ```bash
       helm dependency update ./helm-app-demo
       ```
    5. Run the linter to verify there are no syntax errors:
       ```bash
       helm lint ./helm-app-demo
       ```
*   **Verification**:
    Verify that the dependency archive files are downloaded and located inside the `charts/` folder:
    ```bash
    ls -l ./helm-app-demo/charts
    ```

---

## Task 2: Multi-Environment Values Overrides
*   **Goal**: Define environment-specific configuration files and install the Helm chart with value overrides.
*   **Step-by-Step Instructions**:
    1. Create a dev-specific configuration file named `values-dev.yaml`:
       ```yaml
       # /tmp/values-dev.yaml
       replicaCount: 1
       image:
         tag: "3.11-alpine"
       service:
         type: NodePort
       redis:
         enabled: false # Disable Redis dependency in dev environment
       ```
       Write this file:
       ```bash
       tee /tmp/values-dev.yaml << 'EOF'
       replicaCount: 1
       image:
         tag: "3.11-alpine"
       service:
         type: NodePort
       redis:
         enabled: false
       EOF
       ```
    2. Deploy the application to the `dev` namespace using the custom values overrides:
       ```bash
       kubectl create namespace dev || true
       helm install my-dev-release ./helm-app-demo -f /tmp/values-dev.yaml -n dev
       ```
*   **Verification**:
    Verify that only 1 replica pod has been created in the `dev` namespace, and no Redis pods are running:
    ```bash
    kubectl get pods -n dev
    ```

---

## Task 3: Upgrades and Rollback Mechanics
*   **Goal**: Upgrade the Helm deployment and execute a rollback.
*   **Step-by-Step Instructions**:
    1. Perform a live deployment upgrade, changing replica parameters:
       ```bash
       helm upgrade my-dev-release ./helm-app-demo -f /tmp/values-dev.yaml --set replicaCount=3 -n dev
       ```
    2. View the history of the release:
       ```bash
       helm history my-dev-release -n dev
       ```
    3. Rollback to the initial deployment revision:
       ```bash
       helm rollback my-dev-release 1 -n dev
       ```
*   **Verification**:
    Verify that the replica count has returned to 1 pod in the `dev` namespace:
    ```bash
    kubectl get deployment my-dev-release-helm-app-demo -n dev -o jsonpath='{.spec.replicas}'
    ```
    Clean up the deployment release:
    ```bash
    helm uninstall my-dev-release -n dev
    ```

# Practice Tasks: Module 4 - Kubernetes Infrastructure

This document outlines step-by-step tasks to practice Kubernetes deployment, service mapping, configuration secrets, and pod debugging.

---

## Task 1: Deploy a Multi-Replica Application
*   **Goal**: Create a Kubernetes deployment running 3 replicas of an API service and expose it using a ClusterIP Service.
*   **Step-by-Step Instructions**:
    1. Create a manifest file named `flask-deploy.yaml`:
       ```yaml
       apiVersion: apps/v1
       kind: Deployment
       metadata:
         name: flask-deployment
         namespace: default
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
             - name: api-container
               image: python:3.11-slim
               command: ["python", "-m", "http.server", "8080"]
               ports:
               - containerPort: 8080
               resources:
                 requests:
                   cpu: "100m"
                   memory: "64Mi"
                 limits:
                   cpu: "200m"
                   memory: "128Mi"
       ---
       apiVersion: v1
       kind: Service
       metadata:
         name: flask-service
         namespace: default
       spec:
         selector:
           app: flask-api
         ports:
         - protocol: TCP
           port: 80
           targetPort: 8080
         type: ClusterIP
       ```
       Write this file to disk:
       ```bash
       mkdir -p /tmp/k8s-lab
       tee /tmp/k8s-lab/flask-deploy.yaml << 'EOF'
       apiVersion: apps/v1
       kind: Deployment
       metadata:
         name: flask-deployment
         namespace: default
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
             - name: api-container
               image: python:3.11-slim
               command: ["python", "-m", "http.server", "8080"]
               ports:
               - containerPort: 8080
               resources:
                 requests:
                   cpu: "100m"
                   memory: "64Mi"
                 limits:
                   cpu: "200m"
                   memory: "128Mi"
       ---
       apiVersion: v1
       kind: Service
       metadata:
         name: flask-service
         namespace: default
       spec:
         selector:
           app: flask-api
         ports:
         - protocol: TCP
           port: 80
           targetPort: 8080
         type: ClusterIP
       EOF
       ```
    2. Deploy the manifests:
       ```bash
       kubectl apply -f /tmp/k8s-lab/flask-deploy.yaml
       ```
*   **Verification**:
    Verify that 3 pods are running and mapped to the service:
    ```bash
    kubectl get deployments flask-deployment
    kubectl get pods -l app=flask-api
    kubectl get endpoints flask-service
    ```

---

## Task 2: ConfigMaps and Secret Injection
*   **Goal**: Map environment variables and database passwords to your pods using ConfigMaps and Secrets.
*   **Step-by-Step Instructions**:
    1. Create a ConfigMap and Secret manifest:
       ```yaml
       # /tmp/k8s-lab/config-secret.yaml
       apiVersion: v1
       kind: ConfigMap
       metadata:
         name: app-config
       data:
         LOG_LEVEL: "DEBUG"
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
       Write this file to disk:
       ```bash
       tee /tmp/k8s-lab/config-secret.yaml << 'EOF'
       apiVersion: v1
       kind: ConfigMap
       metadata:
         name: app-config
       data:
         LOG_LEVEL: "DEBUG"
       ---
       apiVersion: v1
       kind: Secret
       metadata:
         name: app-secret
       type: Opaque
       data:
         DB_PASSWORD: c3VwZXJzZWNyZXRwYXNzd29yZA==
       EOF
       ```
    2. Apply the config and secrets:
       ```bash
       kubectl apply -f /tmp/k8s-lab/config-secret.yaml
       ```
    3. Update the deployment manifest to mount these configurations:
       ```yaml
       # Add this section to flask-deploy.yaml container spec
       env:
         - name: APP_LOG_LEVEL
           valueFrom:
             configMapKeyRef:
               name: app-config
               key: LOG_LEVEL
         - name: DB_PASSWORD
           valueFrom:
             secretKeyRef:
               name: app-secret
               key: DB_PASSWORD
       ```
       Apply updates:
       ```bash
       kubectl apply -f /tmp/k8s-lab/flask-deploy.yaml
       ```
*   **Verification**:
    Verify the variables inside one of the running pods:
    ```bash
    POD_NAME=$(kubectl get pods -l app=flask-api -o jsonpath="{.items[0].metadata.name}")
    kubectl exec -it "$POD_NAME" -- env | grep -E "APP_LOG_LEVEL|DB_PASSWORD"
    ```

---

## Task 3: Rolling Updates and Rollbacks
*   **Goal**: Update the container image of your deployment, monitor the update process, and execute a rollback.
*   **Step-by-Step Instructions**:
    1. Update the container image tag:
       ```bash
       kubectl set image deployment/flask-deployment api-container=python:3.11-alpine
       ```
    2. Monitor the rolling update progress:
       ```bash
       kubectl rollout status deployment/flask-deployment
       ```
    3. View the deployment history:
       ```bash
       kubectl rollout history deployment/flask-deployment
       ```
    4. Roll back to the previous deployment configuration:
       ```bash
       kubectl rollout undo deployment/flask-deployment
       ```
*   **Verification**:
    Verify that the deployment has returned to using the previous python image:
    ```bash
    kubectl describe deployment/flask-deployment | grep Image
    ```

# Apache Airflow Setup Guide

This guide provides step-by-step instructions to configure and run Apache Airflow both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

The recommended way to run Apache Airflow locally is using **Docker Compose**. This ensures all dependencies (PostgreSQL database, Redis broker, scheduler, web server, and worker) run in isolated containers matching production environments.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine (Linux).
- Allocate at least **4 GB RAM** (ideally 8 GB) to Docker.

### Step-by-Step Installation

1. **Create a Directory**:
   ```powershell
   mkdir airflow-local
   cd airflow-local
   ```

2. **Download the Official Docker Compose file**:
   ```powershell
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
   ```

3. **Prepare Directories and Environment**:
   Create the folders where Airflow reads DAGs, stores plugins, and logs:
   ```powershell
   mkdir dags logs plugins config
   # Create a .env file setting the Airflow User ID (default 50000 on Linux, can remain default on Windows)
   echo "AIRFLOW_UID=50000" > .env
   ```

4. **Initialize the Metadata Database**:
   Run the db init container to create tables and create a default admin user (username: `airflow`, password: `airflow`):
   ```powershell
   docker compose up airflow-init
   ```

5. **Start Apache Airflow**:
   Start all services in detached mode:
   ```powershell
   docker compose up -d
   ```

6. **Verify the Installation**:
   - Open your browser and navigate to `http://localhost:8080`.
   - Log in using credentials: Username `airflow` and Password `airflow`.
   - Place your DAG scripts in the `./dags` folder; Airflow will parse them in real-time.

---

## 2. Production Setup

In production, managing raw Docker Compose clusters is highly discouraged due to high availability and scaling challenges. Choose either a **Managed Cloud Service** or deploy on **Kubernetes (Helm)**.

### Option A: Managed Cloud Services (Recommended)
Cloud providers host managed, auto-scaling instances of Airflow:
- **AWS (Amazon MWAA)**: Managed Workflows for Apache Airflow. Integrates with AWS IAM, CloudWatch logs, and S3 (where you store your DAG files).
- **GCP (Cloud Composer)**: Built on top of Google Kubernetes Engine (GKE) and integrated with Cloud Logging and IAM.

**AWS MWAA Deployment Steps**:
1. Create an S3 bucket named `mwaa-airflow-assets-<account-id>`.
2. Create folders `dags/` and `requirements/` inside the bucket.
3. Upload your DAGs and a `requirements.txt` listing Python libraries.
4. Open the AWS MWAA console, create a new environment, select the Airflow version, and point the environment settings to your S3 folder paths.
5. AWS handles worker scaling, database backups, and patches automatically.

### Option B: Cloud-Native Kubernetes Deployment (Helm)
For absolute control over compute resources, deploy Airflow on a Kubernetes cluster (e.g., EKS, GKE, AKS) using the official Helm Chart.

1. **Add the Airflow Helm Repository**:
   ```bash
   helm repo add apache-airflow https://airflow.apache.org
   helm repo update
   ```

2. **Create a Namespace**:
   ```bash
   kubectl create namespace airflow
   ```

3. **Configure custom overrides (`values.yaml`)**:
   Create a custom config override file to configure the Kubernetes Executor and link it to your external database via a secret:
   ```yaml
   # values.yaml
   executor: "KubernetesExecutor" # Auto-spins up a pod per task execution
   postgresql:
     enabled: false # Disable internal PostgreSQL container deployment
   data:
     metadataSecretName: "airflow-metadata-secret" # Refers to K8s secret holding connection string
   ```

   Before running the deployment, create the Kubernetes secret in your namespace containing the connection string:
   ```bash
   kubectl create secret generic airflow-metadata-secret \
       --from-literal=connection=postgresql://airflow:SecurePassword123@rds-postgres-db.internal:5432/airflow_db \
       -n airflow
   ```

4. **Install the Chart**:
   ```bash
   helm install airflow apache-airflow/airflow -n airflow -f values.yaml
   ```

5. **Expose the Web Server**:
   Configure an Ingress resource or LoadBalancer service in Kubernetes to route external traffic to your webserver securely using SSL certificates.

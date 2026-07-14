# Data Quality & Governance Setup Guide

This guide provides step-by-step instructions to configure and run Data Quality, Observability, and Cataloging tools both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

In local development, you configure validation rules using **Great Expectations** and **Soda SQL**, and run a local instance of **DataHub** to search schemas.

### Prerequisites
- Install [Python 3.8+](https://www.python.org/downloads/).
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Allocate at least **8 GB RAM** to Docker to run the DataHub catalog container stack.

### Step-by-Step Installation

#### 1. Setup Great Expectations (Python CLI)
1. **Install Great Expectations**:
   ```bash
   pip install great_expectations
   ```
2. **Initialize context**:
   Create the metadata folders inside your python directory:
   ```bash
   great_expectations init
   ```
   This generates a `great_expectations/` configuration directory containing your checkpoints, profiles, and assertions.

#### 2. Setup Soda SQL (Python CLI)
1. **Install Soda Core**:
   ```bash
   pip install soda-core-postgres # Installs Soda Core with PostgreSQL database connector
   ```
2. **Configure Database Connection (`configuration.yml`)**:
   Create a connection configuration file:
   ```yaml
   # configuration.yml
   data_source postgres_warehouse:
     type: postgres
     host: localhost
     username: warehouse_admin
     password: SecurePassword123
     database: warehouse_db
     schema: public
   ```
3. **Write and Execute Check Files**:
   Define validation rules in YAML and run checks:
   ```bash
   soda scan -d postgres_warehouse -c configuration.yml checks/orders.yml
   ```

#### 3. Setup DataHub (Local Catalog Container Stack)
1. **Install DataHub CLI**:
   ```bash
   pip install 'acryl-datahub[all]'
   ```
2. **Launch the Container Stack**:
   Start DataHub (launches MySQL, Elasticsearch, Kafka, Schema Registry, and Web UI containers):
   ```bash
   datahub docker quickstart
   ```
3. **Access the Catalog UI**:
   - Open your browser and navigate to `http://localhost:9002`.
   - Credentials: Username `admin`, Password `admin`.

---

## 2. Production Setup

In production, you utilize scalable, resilient deployments (Kubernetes Helm) to run metadata catalogs and configure automated observability streams.

### Option A: Deploying DataHub on Kubernetes (Helm)
To host a centralized metadata catalog for the entire enterprise:

1. **Add the DataHub Helm Repository**:
   ```bash
   helm repo add datahub https://helm.datahubproject.io/
   helm repo update
   ```

2. **Create custom configuration (`values.yaml`)**:
   Create a override config file to hook DataHub to production managed services instead of deploying internal database containers:
   ```yaml
   # values.yaml
   global:
     sql:
       datasource:
         host: "rds-mysql-catalog.internal"
         port: 3306
         username: "datahub"
         password: "SecurePassword123"
     elasticsearch:
       host: "opensearch-cluster.internal"
       port: 443
   ```

3. **Install the Chart**:
   ```bash
   helm install datahub-prereqs datahub/datahub-prerequisites -f values.yaml -n data-governance --create-namespace
   helm install datahub datahub/datahub -f values.yaml -n data-governance
   ```

### Option B: Production Data Observability (Monte Carlo Integration)
Data Observability platforms like Monte Carlo connect directly to your database engines to monitor health metrics.

1. **Register the Storage / Compute Engine**:
   - Open the **Monte Carlo Console**.
   - Navigate to **Integrations -> Data Sources** and select **Snowflake** or **Google BigQuery**.
   - Provide database access credentials with read-only query permissions to information schemas.
2. **Install CLI and Configure Monitors**:
   Use the Monte Carlo CLI to configure monitoring definitions in code:
   ```bash
   pip install montecarlo
   # Configure authentication credentials
   montecarlo configure
   # Run automated anomaly detection
   montecarlo monitor import --file monitors.yml
   ```
   Monte Carlo's ML models will automatically train on the database's query and row history, alerting the engineering team via Slack if volume drops, freshness breaches SLAs, or schemas change.

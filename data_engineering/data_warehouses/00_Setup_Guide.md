# Data Warehouses Setup Guide

This guide provides step-by-step instructions to configure and run Data Warehouses both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

While you cannot run a massive multi-cluster warehouse like Snowflake locally, you can set up highly capable local OLAP alternatives for development:
- **DuckDB**: An in-process SQL OLAP database engine designed for fast local query development and file inspections (Parquet, CSV, JSON).
- **PostgreSQL**: Set up in an OLAP-like layout to test dimensional models, dbt models, and SQL scripts.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Install [Python 3.8+](https://www.python.org/downloads/).

### DuckDB Setup (Python Flow)
1. **Install DuckDB**:
   ```bash
   pip install duckdb
   ```
2. **Execute Local OLAP Query on Parquet**:
   ```python
   import duckdb
   # DuckDB can query raw S3 files or local Parquet files instantly in-memory
   con = duckdb.connect(database=':memory:')
   con.execute("SELECT * FROM read_parquet('dags/data/*.parquet') LIMIT 5")
   print(con.fetchall())
   ```

### PostgreSQL OLAP Environment Setup (via Docker)
1. **Start PostgreSQL Container**:
   ```bash
   docker run --name pg-warehouse -e POSTGRES_DB=warehouse_db -e POSTGRES_USER=warehouse_admin -e POSTGRES_PASSWORD=SecurePassword123 -p 5432:5432 -d postgres:15
   ```
2. **Verify Connections**:
   - Use any GUI client (like DBeaver or pgAdmin) to connect to `localhost:5432` with database `warehouse_db` and user `warehouse_admin`.
   - You can now write and test DDL schemas, Star Schemas, and CTE queries locally.

---

## 2. Production Setup

In production, you utilize serverless or decoupled cloud architectures that scale compute dynamically without server administration.

### Option A: Snowflake Deployment (Recommended)
Snowflake decouples storage (S3) from compute (Virtual Warehouses).

**Deployment and Scaling Configuration**:
1. Sign up for a Snowflake account.
2. **Configure Storage Integration**: Create an IAM Policy in AWS that grants Snowflake access to your S3 buckets, and map it inside Snowflake using Storage Integrations:
   ```sql
   CREATE OR REPLACE STORAGE INTEGRATION s3_integration
     TYPE = EXTERNAL_STAGE
     STORAGE_PROVIDER = 'S3'
     ENABLED = TRUE
     STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake_access_role'
     STORAGE_ALLOWED_LOCATIONS = ('s3://enterprise-datalake-gold/');
   ```
3. **Configure Virtual Warehouses**: Create compute clusters isolated by business domain, and set auto-suspend and auto-resume policies to control costs:
   ```sql
   CREATE OR REPLACE WAREHOUSE ETL_WH
     WAREHOUSE_SIZE = 'X-LARGE'
     AUTO_SUSPEND = 60 -- Suspend compute after 60 seconds of inactivity
     AUTO_RESUME = TRUE
     INITIALLY_SUSPENDED = TRUE;

   CREATE OR REPLACE WAREHOUSE BI_ANALYST_WH
     WAREHOUSE_SIZE = 'MEDIUM'
     AUTO_SUSPEND = 60
     AUTO_RESUME = TRUE
     INITIALLY_SUSPENDED = TRUE;
   ```

### Option B: Google BigQuery Deployment (Serverless)
Google BigQuery is a fully serverless warehouse that scales processing dynamically.

**BigQuery Optimization Configuration**:
1. Open the Google Cloud Console and select **BigQuery**.
2. **Create a Dataset**: Select the region matching your storage buckets (e.g., `US`).
3. **Create Partitioned and Clustered Tables**: Ensure massive tables are partitioned by day and clustered by high-frequency filter keys:
   ```sql
   CREATE OR REPLACE TABLE my_project.enterprise_gold.fact_sales
   (
     transaction_id STRING,
     customer_id STRING,
     sale_amount NUMERIC,
     transaction_date DATE
   )
   PARTITION BY transaction_date
   CLUSTER BY customer_id;
   ```
4. Set up IAM Roles (`BigQuery Data Viewer`, `BigQuery Job User`) to restrict data access to authorized BI tools and applications.

# Data Lakes Setup Guide

This guide provides step-by-step instructions to configure and run Data Lakes both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

In local development, you emulate AWS S3 storage using **MinIO** (an open-source S3-compatible object store) and configure **LakeFS** locally to enable git-like versioning on top of your local bucket directories.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Step-by-Step Installation

1. **Create a `docker-compose.yaml` file**:
   This configuration runs both MinIO (emulating S3 storage) and LakeFS (metadata version control layer).

   ```yaml
   version: '3.8'
   services:
     minio:
       image: minio/minio:RELEASE.2023-05-18T00-12-52Z
       container_name: minio-s3
       ports:
         - "9000:9000" # MinIO API
         - "9001:9001" # MinIO Web Console
       environment:
         MINIO_ROOT_USER: minioadmin
         MINIO_ROOT_PASSWORD: minioadminpassword
       command: server /data --console-address ":9001"
       volumes:
         - minio_data:/data

     lakefs:
       image: treeverse/lakefs:0.100.0
       container_name: lakefs-git
       ports:
         - "8000:8000"
       environment:
         LAKEFS_DATABASE_CONNECTION_STRING: "local://temp" # In-memory database for testing
         LAKEFS_AUTH_ENCRYPT_SECRET_KEY: "super-secret-key-must-be-long-32chars"
         LAKEFS_BLOCKSTORE_TYPE: "s3"
         LAKEFS_BLOCKSTORE_S3_ENDPOINT: "http://minio:9000"
         LAKEFS_BLOCKSTORE_S3_FORCE_PATH_STYLE: "true"
         LAKEFS_BLOCKSTORE_S3_CREDENTIALS_ACCESS_KEY_ID: "minioadmin"
         LAKEFS_BLOCKSTORE_S3_CREDENTIALS_SECRET_ACCESS_KEY: "minioadminpassword"
       command: run
       depends_on:
         - minio

   volumes:
     minio_data:
   ```

2. **Start the containers**:
   ```bash
   docker compose up -d
   ```

3. **Configure MinIO Buckets**:
   - Navigate to `http://localhost:9001` in your browser.
   - Login: User `minioadmin`, Password `minioadminpassword`.
   - Click **Buckets -> Create Bucket** and name it `datalake-bucket`.

4. **Initialize LakeFS**:
   - Navigate to `http://localhost:8000` in your browser.
   - Complete the setup wizard to create an administrator user.
   - Save the generated Access Key ID and Secret Access Key.
   - Click **Create Repository**. Name it `enterprise-lake`, set the Storage Namespace to `s3://datalake-bucket/main`, and submit.
   - You can now commit, branch, and merge data changes using the LakeFS UI or Python client.

---

## 2. Production Setup

In production, you utilize native cloud object stores (AWS S3) and secure access controls using metadata governance engines.

### Cloud Data Lake Components (AWS Setup)
A production AWS Data Lake architecture uses:
1. **Amazon S3**: Cheap, durable object storage serving as the physical file registry.
2. **AWS Glue Catalog**: Manages metadata schemas and partitions dynamically.
3. **AWS Lake Formation**: Enforces granular access control policies (RBAC/ABAC) on Glue tables.

### S3 Security & Configuration Steps
1. **Create the S3 Buckets**:
   Create separate buckets representing your Medallion zones:
   - `s3://enterprise-datalake-bronze-<account-id>`
   - `s3://enterprise-datalake-silver-<account-id>`
   - `s3://enterprise-datalake-gold-<account-id>`

2. **Enforce Encryption and Block Public Access**:
   Ensure all buckets have default encryption enabled (SSE-KMS) and block all public access paths:
   ```bash
   # Block all public read/write permissions
   aws s3api put-public-access-block \
       --bucket enterprise-datalake-bronze-<account-id> \
       --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
   ```

3. **Register Storage with AWS Lake Formation**:
   Rather than writing complex S3 bucket policies, register the S3 paths directly inside AWS Lake Formation.
   - Open the **AWS Lake Formation Console**.
   - Navigate to **Register and Ingest -> Data Lake Locations** and register your S3 bucket.
   - Grant permissions dynamically using SQL-like statements:
     ```sql
     -- Conceptual representation of Lake Formation grant permissions
     GRANT SELECT ON database_silver.users_table TO ROLE 'data_analyst_role';
     ```
   - This decouples IAM policy management from physical S3 directories, allowing you to grant, revoke, and audit data access from a central security panel.

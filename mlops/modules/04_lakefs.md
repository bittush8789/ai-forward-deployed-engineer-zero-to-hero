# Module 4: Data Lake Versioning & Governance with LakeFS

## 1. Architecture Deep Dive

LakeFS is an open-source data version control tool designed for data lakes. It provides Git-like operations (branching, committing, merging, and reverting) over object storage platforms (such as AWS S3, GCS, Azure Blob, or MinIO) at petabyte scale.

```
+-------------------------------------------------------------------------------------------------+
|                                           Data Consumer                                         |
|    - Spark Jobs, Presto/Trino Queries, Python Scripts, MLOps Pipelines                         |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (S3 Gateway API / lakectl CLI)
+-----------------------------------------------+-------------------------------------------------+
|                                            LakeFS Server                                        |
|    - Exposes an S3-compatible Gateway API and REST API endpoints                                |
|    - Manages authorization, branch routing, and metadata transactions                           |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (SQL Metadata Store)                            v (Object APIs)
+---------------------------------------+-------------------------------------------------+-------+
|                            Database (PostgreSQL)                                        |       |
|    - Stores commit manifests, branches, metadata pointers, and transaction logs             |       |
+-----------------------------------------------------------------------------------------+       |
                                                                                                  v
+-------------------------------------------------------------------------------------------------+
|                                     Underlying Data Lake                                        |
|                     AWS S3 | Google Cloud Storage | Azure Blob | Local MinIO                     |
+-------------------------------------------------------------------------------------------------+
```

### Metadata Store vs. Object Storage
*   **Metadata Store**: A PostgreSQL database that tracks the commit history, branch references, and pointers to the physical location of files in object storage.
*   **Underlying Data Lake**: The physical object storage where files are written. LakeFS does not duplicate files; it manages pointer mappings in the database.

---

## 2. Internal Working

### Zero-Copy Cloning & Manifest Trees
When you create a new branch in LakeFS:
1.  **Metadata Clones**: LakeFS copies the pointer references in the PostgreSQL database instead of duplicating physical files.
2.  **Isolated Changes**: Write operations on the new branch create new files in object storage and update pointers on that branch. The original branch remains unchanged.
3.  **Merge Reconciliation**: Merging branches updates the metadata pointers in the parent branch.

---

## 3. Production Use Cases

### Isolated Data Pipeline Testing
Data engineers can create a branch from the main data lake branch, run data transformation pipelines, and validate results in isolation without affecting production data.

### Instant Data Lake Rollbacks
If a pipeline writes corrupted data to production, you can roll back the database pointers to a previous commit, restoring the data lake to a stable state in seconds.

---

## 4. Governance Considerations

### Pre-Merge Hook Validation
Configure automated data quality checks (such as schema validation or PII detection) to run before a branch is merged into the main data lake branch:
```yaml
# Example pre-merge hook configuration
name: SchemaValidation
on:
  pre-merge:
    branches:
      - main
hooks:
  - id: run-schema-check
    type: webhook
    properties:
      url: http://data-validator.internal/validate
```

---

## 5. Security Best Practices

### Access Policies & Token Configuration
*   Disable direct access to the underlying object storage bucket. Force all data access to route through LakeFS using custom access keys and role-based permissions.
*   Integrate LakeFS authorization with enterprise identity providers (OIDC/SAML).

---

## 6. Scalability Patterns

### Metadata Partitioning
For petabyte-scale data lakes containing millions of files, database query latency can slow down.
*   Partition the PostgreSQL metadata tables based on repository ID or branch.
*   Deploy PostgreSQL read replicas to handle read-only queries from analytics engines.

---

## 7. Reliability Patterns

### Database Transaction Recovery
Deploy PostgreSQL with high availability and automated backup procedures. Ensure the database backup is synchronized with the object storage bucket state.

---

## 8. Cost Optimization

### Zero-Copy Storage Efficiencies
Zero-copy cloning prevents physical data duplication, keeping storage costs low even when running multiple parallel development pipelines. Configure lifecycle rules on the underlying storage bucket to delete orphaned files created during failed pipeline runs.

---

## 9. Hands-On Labs

### Lab 9.1: Setting up LakeFS with local MinIO on Ubuntu
Run these commands to configure LakeFS and MinIO locally.
```bash
# 1. Install and start MinIO (Object Storage)
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server /tmp/minio-data --console-address :9090 &

# 2. Create the LakeFS configuration file
mkdir -p ~/.lakefs
cat << 'EOF' > ~/.lakefs/config.yaml
database:
  connection_string: postgresql://mlflow_user:mlflow_pass@localhost/mlflow_db?sslmode=disable
storage:
  blockstore_type: s3
  s3:
    endpoint_url: http://localhost:9000
    aws_access_key_id: minioadmin
    aws_secret_access_key: minioadmin
auth:
  encrypt_secret_key: "super-secret-encryption-key-must-be-long"
EOF

# 3. Start LakeFS Server
# (Download lakefs binary and execute setup)
wget https://github.com/treeverse/lakeFS/releases/download/v1.0.0/lakefs_1.0.0_linux_amd64.tar.gz
tar -xzf lakefs_1.0.0_linux_amd64.tar.gz
./lakefs --config ~/.lakefs/config.yaml run &
```

### Lab 9.2: Data Branching and Merging via `lakectl`
Configure credentials and run Git-like operations on your data.
```bash
# 1. Configure lakectl credentials
# (Retrieve access key and secret key from LakeFS UI on http://localhost:8000)
export LAKECTL_SERVER_URL="http://localhost:8000"
export LAKECTL_ACCESS_KEY_ID="my-access-key"
export LAKECTL_SECRET_ACCESS_KEY="my-secret-key"

# 2. Create a new data repository
./lakectl repo create lakefs://my-data-repo s3://my-lakefs-bucket

# 3. Create a development branch
./lakectl branch create lakefs://my-data-repo/dev-branch --source lakefs://my-data-repo/main

# 4. Upload a dataset to the development branch
echo "id,name" > /tmp/users.csv
./lakectl fs upload /tmp/users.csv lakefs://my-data-repo/dev-branch/users.csv

# 5. Commit changes
./lakectl commit lakefs://my-data-repo/dev-branch -m "Upload raw users list"

# 6. Merge development branch into main
./lakectl merge lakefs://my-data-repo/dev-branch lakefs://my-data-repo/main
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Merge Conflicts in Parallel Pipelines
*   **Symptom**: `lakectl merge` fails with `Conflict: ... merge conflict detected`.
*   **Root Cause**: Two parallel pipelines modified the same file path on different branches and attempted to merge back to main.
*   **Resolution Strategy**:
    *   Identify the conflicting file paths.
    *   Resolve conflicts manually by choosing the correct version of the file on a development branch.
    *   Commit and re-run the merge operation.

### Task 10.2: Database Connection Failures
*   **Symptom**: LakeFS server crashes or fails to start with `error connecting to database: connection refused`.
*   **Root Cause**: The PostgreSQL database is offline or the connection string is incorrect.
*   **Resolution Strategy**:
    *   Verify the PostgreSQL service is active:
        ```bash
        sudo systemctl status postgresql
        ```
    *   Verify credentials by logging in manually:
        ```bash
        psql -h localhost -U mlflow_user -d mlflow_db
        ```

---

## 11. Real Production Incidents

### Case Study: Buggy Pipeline Corrupting Production Data
*   **Incident**: A data scientist modified a production pipeline script but forgot to test it locally. The script wrote corrupted records directly to the `main` data lake branch, breaking downstream dashboard and reporting services.
*   **Remediation**:
    *   Executed a rollback to the last stable commit:
        ```bash
        ./lakectl commit revert lakefs://my-data-repo/main <stable-commit-id>
        ```
    *   This instantly restored the data lake pointers to the stable state, resolving the outage while the team debugged the script.

---

## 12. Interview Questions

### Q1: What is zero-copy cloning in LakeFS?
*   **Answer**: Zero-copy cloning allows creating isolated branches of a data lake without copying physical files. LakeFS duplicates the metadata pointers in the PostgreSQL database instead, saving storage space and execution time.

### Q2: How does LakeFS provide an S3-compatible gateway?
*   **Answer**: LakeFS exposes an S3-compatible gateway API that translates standard S3 client requests (such as `GetObject` or `PutObject`) into metadata lookups and physical file operations on the underlying storage bucket.

### Q3: Explain the purpose of pre-merge hooks in LakeFS.
*   **Answer**: Pre-merge hooks are automated checks (such as schema validation or data quality tests) that run before a branch is merged into the main branch, preventing corrupted data from reaching production.

### Q4: How does LakeFS handle transactional safety during concurrent writes?
*   **Answer**: LakeFS uses a PostgreSQL database to manage metadata updates as transactions, ensuring ACID compliance and preventing concurrent write conflicts.

### Q5: What is the risk of using fine-grained ACLs in S3 when routing traffic through LakeFS?
*   **Answer**: Routing traffic through LakeFS means S3 client requests are authenticated using LakeFS credentials. Fine-grained S3 ACLs can block access; instead, manage access permissions within LakeFS.

---

## 13. Enterprise Case Studies

### Data Governance at Windward
Windward, a maritime data analytics company, uses LakeFS to version multi-terabyte datasets. By creating isolated branches for data validation pipelines and using pre-merge hooks to enforce data quality standards, they reduced manual database checks and improved data delivery reliability.

---

## 14. AI FDE Perspective

### Integrating LakeFS with Apache Spark Data Pipelines
As an AI Forward Deployed Engineer (FDE), you often configure distributed processing engines to interface with LakeFS:
```python
# Configure Spark to route S3 traffic through LakeFS Gateway
spark.conf.set("fs.s3a.endpoint", "http://lakefs.internal.corp:8000")
spark.conf.set("fs.s3a.access.key", "my-access-key")
spark.conf.set("fs.s3a.secret.key", "my-secret-key")

# Query data from a specific branch version
df = spark.read.parquet("s3a://my-data-repo/dev-branch/processed_data/")
```
This allows data science teams to utilize Spark processing power over versioned branches of the data lake.

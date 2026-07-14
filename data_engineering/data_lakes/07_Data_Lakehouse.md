# Module 6.7: Data Lakehouse

Welcome to **Data Lakehouse**. Historically, data was stored in Data Lakes (cheap, raw, slow queries) and duplicated into Data Warehouses (expensive, fast, SQL-only). The **Lakehouse** paradigm eliminates this duplication by introducing a metadata layer on top of object storage. This enables ACID transactions, schema enforcement, and time travel directly on raw Parquet data using formats like **Delta Lake**, **Apache Iceberg**, and **Apache Hudi**.

---

## 1. Detailed Theory

### What is a Lakehouse?
A Lakehouse is a data management architecture that combines the low-cost, flexible storage of a Data Lake with the structure, ACID transactions, and query optimizations of a Data Warehouse. It allows BI tools and machine learning systems to query the same data files on S3/GCS.

### Core Features
- **ACID Transactions**: Multiple workers can write to a table concurrently. If a write fails, it is rolled back completely, preventing data corruption.
- **Schema Enforcement**: Blocks writes that contain columns not defined in the table schema, preventing dirty data from polluting production tables.
- **Time Travel**: Accessing historical snapshots of the dataset using version IDs or timestamps.

### Table Format Features
1. **Delta Lake**:
   - **MERGE**: Upserts records (inserts new rows and updates existing rows) in one atomic transaction.
   - **OPTIMIZE**: Compacts small partition files into optimal large files.
   - **Z-Ordering**: Clusters records on specified columns to allow the query engine to skip reading entire files.
2. **Apache Iceberg**:
   - **Partition Evolution**: Allows changing the partition layout (e.g., from daily to hourly) without rewriting historical data.
   - **Schema Evolution**: Safely adding, dropping, or renaming columns.
3. **Apache Hudi**:
   - **Merge-on-Read**: Optimizes streaming upserts by writing changes to small log files and merging them during read operations.

---

## 2. Architecture Diagram: Lakehouse Format Interface

```mermaid
flowchart TD
    subgraph "Query Engines (Spark, Presto, Flink)"
        SQL[SQL Query: SELECT * FROM users]
    end
    
    subgraph "Lakehouse Metadata Layer (Delta/Iceberg)"
        Log[Transaction Log / Metadata Manifests]
    end
    
    subgraph "Physical Object Storage (S3 / GCS)"
        F1[part-001.parquet]
        F2[part-002.parquet]
        F3[part-003.parquet (Stale version)]
    end
    
    SQL --> Log
    Log -->|Resolves Active Files| F1
    Log -->|Resolves Active Files| F2
    Log -.->|Skips stale file| F3
```

---

## 3. Production Use Cases

1. **Enterprise Lakehouse Platform**: Building a transactional lakehouse where streaming checkout events are upserted into customer profiles using Delta `MERGE`. Periodically, an `OPTIMIZE` command runs to compact small files and index the tables on `customer_id` using `Z-ORDER`.
2. **Historical Data Auditing**: Accessing the state of a customer database exactly as it was on a specific date to validate historical financial reports.

---

## 4. Real Company Examples

- **Netflix**: Built Apache Iceberg to solve query performance bottlenecks on S3, allowing them to manage schema changes and partition updates dynamically without rewriting petabytes of data.

---

## 5. Coding Examples

### Delta Lake MERGE and OPTIMIZE in PySpark

```python
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Initialize SparkSession with Delta Lake extensions
spark = SparkSession.builder \
    .appName("LakehouseOps") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 1. Load Staging DataFrame
staging_df = spark.read.parquet("s3://enterprise-datalake/raw/staging_users/")

# 2. Reference Target Delta Table
# If table doesn't exist, save staging_df to initialize it
target_path = "s3://enterprise-datalake/processed/users/"
delta_table = DeltaTable.forPath(spark, target_path)

# 3. Perform Transactional MERGE (Upsert)
delta_table.alias("t") \
    .merge(
        source=staging_df.alias("s"),
        condition="t.user_id = s.user_id"
    ) \
    .whenMatchedUpdate(set={
        "email": "s.email",
        "updated_at": "s.updated_at"
    }) \
    .whenNotMatchedInsert(values={
        "user_id": "s.user_id",
        "email": "s.email",
        "created_at": "s.created_at",
        "updated_at": "s.updated_at"
    }) \
    .execute()

# 4. Optimize storage: Compact small files and index on user_id
delta_table.optimize().zorder("user_id").execute()
```

---

## 6. Hands-on Labs

**Lab: Time Travel Execution**
**Objective**: Read historical versions.
**Instructions**:
Write the PySpark syntax to load version `5` of a Delta Table located at `s3://bucket/table` and print its row count. (Hint: Use `option("versionAsOf", "5")`).

---

## 7. Assignments

**Assignment: Schema Evolution Rules**
Compare how **Delta Lake** and **Apache Iceberg** handle schema evolution (e.g., renaming a column from `first_name` to `fname`). How does the metadata layer prevent the need to rewrite the underlying Parquet files?

---

## 8. Interview Questions

1. **What is a Data Lakehouse?**
   *Answer Hint: A data management architecture that brings data warehouse capabilities (ACID transactions, schema enforcement, indexing) directly to cheap object storage data lakes, eliminating the need to duplicate data between lakes and warehouses.*
2. **What does Z-Ordering do in Delta Lake?**
   *Answer Hint: Z-Ordering is a multidimensional clustering technique that co-locates related information in the same set of files. This allows query engines to skip reading irrelevant files based on the query filter, speeding up performance.*

---

## 9. Best Practices (FDE Standards)

- **Z-Order on High-Query Keys**: Always apply `Z-ORDER` on columns frequently used in query joins or filters (e.g., `user_id`, `timestamp`).
- **Enforce Schemas**: Never turn off schema enforcement in production Delta tables unless explicitly designing for schema evolution.

---

## 10. Common Mistakes

- **Failing to VACUUM**: Forgetting to run `VACUUM` on active Delta tables, leaving hundreds of gigabytes of historical stale Parquet files in S3 and increasing storage bills.
- **Concurrent Merges**: Attempting to run parallel merge jobs targeting the same partition, leading to `ConcurrentAppendException` errors.

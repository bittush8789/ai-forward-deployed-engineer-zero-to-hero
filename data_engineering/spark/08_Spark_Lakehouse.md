# Module 4.8: Spark + Data Lakehouse

Welcome to **Spark + Data Lakehouse**. Modern data architectures combine the low-cost scalability of Data Lakes (S3/GCS) with the transaction guarantees of Data Warehouses. This is accomplished using open table formats: **Delta Lake**, **Apache Iceberg**, and **Apache Hudi**. In this module, you'll learn how to write Spark code that implements ACID transactions, schema evolution, and time travel.

---

## 1. Detailed Theory

### What is a Table Format?
A table format is a way to organize raw files (usually Parquet) to present them as a single structured table. Without a table format, a folder containing Parquet files has no transaction safety: if two processes write to it at the same time, the data becomes corrupted.

### The Three Competitors
1. **Delta Lake** (Created by Databricks): Uses a JSON transaction log (`_delta_log`) alongside Parquet files. Deeply integrated with Spark and Databricks.
2. **Apache Iceberg** (Created by Netflix): Uses hierarchical metadata files (Manifest Lists and Manifests) instead of directory names, allowing for fast partition evolution and file-level layout optimization.
3. **Apache Hudi** (Created by Uber): Designed specifically for low-latency streaming inserts, updates (Merge-on-Read), and incremental queries.

### Core Features of Delta Lake
- **ACID Transactions**: Mutual exclusion of writes. If a write fails midway, all changes are rolled back.
- **Time Travel (Versioning)**: You can query the table exactly as it looked at a specific version or timestamp (e.g., "how did this dataset look yesterday?").
- **OPTIMIZE & Z-Ordering**: Compacting small files into larger ones (`OPTIMIZE`) and clustering records on specific columns (`Z-Ordering`) to enable file skipping during queries.

---

## 2. Architecture Diagram: Delta Lake Layout

```mermaid
flowchart TD
    subgraph "Delta Table Directory (S3/GCS)"
        subgraph "_delta_log (Transaction Log)"
            V000[000000.json\nAdds part-1]
            V001[000001.json\nAdds part-2, deletes part-1]
        end
        
        subgraph "Data Files"
            P1[part-1.parquet\nVersion 0]
            P2[part-2.parquet\nVersion 1 (Updated)]
        end
    end
    
    %% Engine reads _delta_log first to see which Parquet files are active!
```

---

## 3. Production Use Cases

1. **Enterprise Data Auditing**: Reconstructing a historical model training dataset exactly as it was on January 1st to comply with audit requirements.
2. **Streaming Upserts**: Streaming transaction events from Kafka and using Delta `MERGE` to update user balances in a database-like table on S3 in real-time.

---

## 4. Real Company Examples

- **Netflix**: Moved their entire petabyte-scale data warehouse catalog to Apache Iceberg to solve slow metadata queries (like directory listings on AWS S3).
- **Walmart**: Uses Delta Lake on top of their cloud storage to guarantee data reliability and transaction consistency for their global sales analytics platforms.

---

## 5. Coding Examples

### Time Travel and Merge Operations in Delta Lake

```python
from pyspark.sql import SparkSession

# 1. Initialize Spark Session with Delta Provider configurations
spark = SparkSession.builder \
    .appName("DeltaLakeShowcase") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 2. Write DataFrame as a Delta Table
df = spark.read.json("raw_data.json")
df.write.format("delta").save("s3://lakehouse/customers")

# 3. Read specific historical version (Time Travel)
historical_df = spark.read \
    .format("delta") \
    .option("versionAsOf", "0") \
    .load("s3://lakehouse/customers")

# 4. Performing a MERGE (Upsert) using SQL
# Register Delta table in metastore
spark.sql("CREATE TABLE IF NOT EXISTS customers USING DELTA LOCATION 's3://lakehouse/customers'")

# Run SQL Merge to update active flags
merge_sql = """
    MERGE INTO customers AS t
    USING staging_customers AS s
    ON t.id = s.id
    WHEN MATCHED THEN
        UPDATE SET t.email = s.email, t.is_active = s.is_active
    WHEN NOT MATCHED THEN
        INSERT (id, email, is_active) VALUES (s.id, s.email, TRUE)
"""
spark.sql(merge_sql)

# 5. Optimize performance: Compact files
spark.sql("OPTIMIZE customers")
```

---

## 6. Hands-on Labs

**Lab: OPTIMIZE & Vacuum**
**Objective**: Clean up historical files.
**Instructions**:
Write an explanation of what the `VACUUM` command does in a Delta table. Why must you be careful when setting the retention threshold to less than 7 days (168 hours)? (Hint: Think about active writers).

---

## 7. Assignments

**Assignment: Table Format Comparison**
Choose between Delta Lake and Apache Iceberg. Write a technical memo detailing how the format handles **Schema Evolution** (adding/renaming columns) and **Partition Evolution** (changing the partition scheme of a table without rewriting the historical data).

---

## 8. Interview Questions

1. **How does Delta Lake achieve ACID compliance on simple S3/GCS object storage?**
   *Answer Hint: Through a centralized transaction log folder (`_delta_log`). Any writer must write a new serialized JSON log file (e.g., `000001.json`) using optimistic concurrency control. Readers parse the log files first to see which Parquet files are currently active and consistent.*
2. **What is Time Travel in Delta Lake?**
   *Answer Hint: Because Delta Lake preserves old parquet files when modifications occur and records all changes in the transaction log, you can query historical versions of the dataset by specifying the version number or timestamp in the reader configuration.*

---

## 9. Best Practices (FDE Standards)

- **Compact regularly**: Run `OPTIMIZE` on active tables to group tiny streaming partition files into optimal ~1GB files to prevent query degradation.
- **Run VACUUM to manage storage costs**: Delta Lake keeps old versions of files forever. Run `VACUUM` to delete physical files older than a set threshold (e.g., 30 days) to recover storage costs.

---

## 10. Common Mistakes

- **Deleting files directly on disk**: Deleting Parquet files inside the Delta table folder manually. This breaks the transaction log, causing read operations to crash. Always use `VACUUM` or SQL `DELETE` commands.
- **Concurrent write conflicts**: Attempting to run multiple parallel jobs that delete or write to the same partition, resulting in a `ConcurrentAppendException` or `WriteConflictException`.

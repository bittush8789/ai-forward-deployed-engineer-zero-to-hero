# Module 4.13: Production Spark Engineering

Welcome to **Production Spark Engineering**. Deploying Spark applications in enterprise environments requires deep execution knowledge of performance tuning, cluster sizing, monitoring, and security. In this module, you will learn how to analyze Spark execution plans, debug out-of-memory errors, secure data access, and monitor workloads.

---

## 1. Detailed Theory

### Performance Tuning & Query Plan Analysis
To optimize Spark jobs, you must inspect the execution plan:
- Use `.explain(True)` to print the query plan.
- Look for **Exchange** (shuffles). If you see multiple Exchanges, check if you can optimize with broadcast joins, bucketing, or partition pruning.
- **Data Skew Optimization**: If one partition contains 100x more data than others, one executor will drag the entire job. Solve this by **salting** (adding random integer keys to distribute data).
- **Memory Tuning**: Balancing storage memory (for caching) and execution memory (for joins/aggregations) in `spark.executor.memory`.

### Scalability & Resource Allocation
- **Dynamic Allocation**: Allows Spark to dynamically request executors from the Cluster Manager when tasks build up, and release them when idle to save costs.
- **Cluster Sizing Rule of Thumb**:
  - Keep executor cores to 4 - 6 per executor (higher numbers cause HDFS/storage write congestion).
  - Allocate memory based on partition size (aim for 2GB - 4GB per executor core).

### Monitoring (Spark UI & Prometheus)
- **Spark UI**: The central visual console (accessible on port 4040) showing Stage execution DAGs, task duration charts, and executor logs.
- **OpenTelemetry / Prometheus**: Exporting cluster metrics to Grafana dashboards for centralized enterprise observability.

---

## 2. Architecture Diagram: Executor Memory Allocation

```mermaid
subgraph "Executor JVM Memory (spark.executor.memory)"
    subgraph "JVM Overhead (10%)"
        Overhead[Off-Heap Memory / Tungsten]
    end
    
    subgraph "Spark Memory (60% of Executor memory)"
        Storage[Storage Memory\nCached Data & Broadcasts]
        Execution[Execution Memory\nShuffle Joins & Aggregations]
    end
    
    subgraph "User Memory (40%)"
        User[User Memory\nCustom Python/UDF Objects]
    end
end
```

---

## 3. Production Use Cases

1. **Enterprise Performance Auditing**: Profiling a daily aggregation job that runs for 4 hours. By analyzing the Spark UI, you identify a data skew on a null grouping key, apply salting, and reduce execution time to 15 minutes.
2. **Dynamic Autoscaling (Kubernetes)**: Running an ad-hoc SQL query on a serverless Spark pool. Spark automatically provisions 50 executors to process the query and shuts them down 60 seconds after completion.

---

## 4. Real Company Examples

- **Netflix**: Monitors all their Spark jobs globally using custom Prometheus/Grafana dashboards, detecting resource-inefficient pipelines automatically and alerting owners.
- **Stripe**: Secures their Spark clusters using Kerberos encryption and RBAC policies, ensuring financial data remains strictly isolated.

---

## 5. Coding Examples

### Implementing Salting to Solve Data Skew

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("DataSkewFix").getOrCreate()

# 1. Load skewed dataset (e.g., millions of records have user_id = 'GUEST')
large_skewed_df = spark.read.parquet("s3://raw-activity/")
lookup_df = spark.read.parquet("s3://users/")

# 2. Apply Salting to the large table: add a random salt column (0 to 3)
salted_large_df = large_skewed_df.withColumn(
    "salt", 
    F.concat(F.col("user_id"), F.lit("_"), F.randint(0, 3))
)

# 3. Explode the lookup table: replicate each user row 4 times (with salt suffixes)
exploded_lookup_df = lookup_df.withColumn(
    "salts", 
    F.array([F.lit(i) for i in range(4)])
).select(
    "*", 
    F.explode(F.col("salts")).alias("salt_suffix")
).withColumn(
    "salt", 
    F.concat(F.col("user_id"), F.lit("_"), F.col("salt_suffix"))
)

# 4. Perform the Join on the salted key (distributes the 'GUEST' load across 4 executors)
optimized_join_df = salted_large_df.join(
    exploded_lookup_df, 
    on="salt", 
    how="inner"
).drop("salt", "salt_suffix")

optimized_join_df.write.parquet("s3://clean-activity/")
```

---

## 6. Hands-on Labs

**Lab: Spark UI Profiling**
**Objective**: Identify slow stages in the Spark UI.
**Instructions**:
Write out the steps you would take to find which task in a Spark job is taking the longest time using the Spark UI. (Hint: Details tab -> Stages -> Task Metrics timeline).

---

## 7. Assignments

**Assignment: Cluster Configuration Calculation**
You have a 1TB CSV dataset. You are sizing a Spark cluster on YARN with nodes having 64GB RAM and 16 Cores.
Calculate:
1. The number of executors per node (keeping cores/executor <= 5).
2. The memory allocation for each executor.
3. The target partition count for the input dataset.

---

## 8. Interview Questions

1. **What is Data Skew and how do you resolve it?**
   *Answer Hint: Data skew is when data is unevenly distributed across partitions, causing a few executors to process significantly more data than others. Resolve it by salting the join/groupby keys (appending a random suffix to distribute the key) or using Broadcast joins to avoid shuffles.*
2. **What does the Executor memory overhead parameter do?**
   *Answer Hint: It allocates memory outside of the standard Spark JVM memory pool (off-heap memory) for thread stacks, network buffers, and Tungsten engine operations to prevent the operating system/container manager (YARN/Kubernetes) from killing the container.*

---

## 9. Best Practices (FDE Standards)

- **Do Not Allocate > 5 Cores per Executor**: Allocating 10-16 cores to a single executor causes heavy garbage collection pauses and decreases disk/network write efficiency. Use multiple smaller executors instead.
- **Enable Garbage Collection Logging**: Always enable GC logging in JVM parameters to quickly identify if memory problems are caused by Java Garbage Collection cycles.

---

## 10. Common Mistakes

- **Swallowing executor logs**: Sizing a cluster with insufficient memory, causing YARN/Kubernetes to kill containers silently (reported as exit code 137 / Out of Memory) without logging stack traces to the Spark UI logs.
- **Unsalted null joins**: Performing joins on tables containing millions of null keys. Spark treats all nulls as identical keys, sending all null rows to a single executor and causing an OOM. (Always filter out or salt nulls before joining).

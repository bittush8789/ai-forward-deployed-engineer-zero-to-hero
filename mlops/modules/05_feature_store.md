# Module 5: Feature Stores (Feast & Tecton)

## 1. Architecture Deep Dive

A Feature Store is a centralized repository that manages the injection, transformation, storage, and serving of machine learning features. It decouples feature engineering from model training and deployment.

```
+-------------------------------------------------------------------------------------------------+
|                                           Data Sources                                          |
|                Parquet Files | Data Warehouses (Snowflake, Trino) | Kafka Streams               |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Feature Ingestion / materialization)
+-----------------------------------------------+-------------------------------------------------+
|                                           Feature Store                                         |
|   +-------------------------------------------+---------------------------------------------+   |
|   |         Offline Store (Historical)        |           Online Store (Low Latency)        |   |
|   |   - Database / storage (Parquet, SQL)     |   - Key-Value Store (Redis, DynamoDB)       |   |
|   |   - Used for training dataset generation  |   - Used for sub-millisecond serving        |   |
|   +-------------------------------------------+---------------------------------------------+   |
+------------------------+------------------------------------------------------+-----------------+
                         |                                                      |
                         v (Historical Queries)                                 v (Online SDK / REST)
+------------------------+----------------------+      +------------------------+-----------------+
|                    Model Training             |      |                   Real-Time Inference    |
|       - Generates training datasets           |      |       - Fetches latest feature state     |
|         using point-in-time joins            |      |         for inference predictions        |
+-----------------------------------------------+      +------------------------------------------+
```

### Offline Store vs. Online Store
*   **Offline Store**: Holds historical data (often stored in data warehouses like Snowflake or flat Parquet files) used to generate training datasets.
*   **Online Store**: A low-latency key-value database (like Redis, DynamoDB, or Bigtable) that stores the latest value of each feature for sub-millisecond serving during model inference.

---

## 2. Internal Working

### Point-in-Time Joins (Avoiding Data Leakage)
A common issue in machine learning is **data leakage**: including features in the training dataset that would not be available at the time of inference.
*   Feature stores execute Point-in-Time Joins (or "time-travel" queries) to ensure that for any historical training event, the features retrieved are the latest values available *before* the event timestamp, preventing future data from leaking into training datasets.

---

## 3. Production Use Cases

### Real-Time Fraud Detection Serving
Retrieving user profile features (such as transaction counts in the past 10 minutes) from the online store (Redis) with sub-millisecond latency to evaluate fraud models during checkout transactions.

### Reusable Feature Catalog
Maintaining a centralized catalog of computed features, allowing different teams to reuse existing features for new models, reducing duplicate data pipeline costs.

---

## 4. Feature Governance & Lineage

### Cataloging & Tracking Feature Usage
Feast and Tecton manage feature metadata schemas. By tracking feature definitions in Git, teams can audit changes, search for features by owner or description, and track which models consume which features.

---

## 5. Security Best Practices

### Access Control Policies
*   Disable public access to online feature store databases (like Redis).
*   Use IAM roles and network policies to restrict access to the online store to authorized inference pods.

---

## 6. Scalability Patterns

### Redis Clustering for High-Throughput Serving
For high-throughput serving (e.g., thousands of requests per second), scale the online store using a **Redis Cluster** to distribute the read/write load across multiple database nodes.

---

## 7. Reliability Patterns

### Online-Offline Synchronization Validation
Configure automated monitoring on synchronization jobs (materialization) to detect ingestion failures and ensure the online store is updated with fresh feature values.

---

## 8. Cost Optimization

### Setting Time-To-Live (TTL) Configurations
Configure Time-To-Live (TTL) settings on online features:
```python
# Feast Feature View definition configuration
driver_hourly_stats = FeatureView(
    name="driver_hourly_stats",
    ttl=timedelta(days=90), # Expire features older than 90 days from the online store
    # configurations...
)
```
This automatically deletes stale features from Redis, optimizing memory footprint and reducing database hosting costs.

---

## 9. Hands-On Labs

### Lab 9.1: Building a Feature Store with Feast on Ubuntu
Run these commands to install Feast, define feature schemas, and ingest data.
```bash
# 1. Install Feast and Redis dependencies
pip install feast redis

# 2. Start a Redis container to act as the online store
docker run -d --name feast-redis -p 6379:6379 redis:alpine

# 3. Create a Feast workspace directory
mkdir -p /tmp/feast-lab && cd /tmp/feast-lab
feast init my_feature_repository
cd my_feature_repository
```
Update `/tmp/feast-lab/my_feature_repository/feature_store.yaml` to use Redis:
```yaml
project: my_feature_repository
registry: data/registry.db
provider: local
offline_store:
  type: file
online_store:
  type: redis
  connection_string: localhost:6379
```

### Lab 9.2: Defining Features and Materializing Data
Create a feature definition file:
```python
# /tmp/feast-lab/my_feature_repository/features.py
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Define raw parquet file source
driver_stats_source = FileSource(
    path="/tmp/feast-lab/my_feature_repository/data/driver_stats.parquet",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

# Define entity
driver = Entity(name="driver_id", value_type=Int64, description="driver id")

# Define feature view
driver_stats_view = FeatureView(
    name="driver_stats",
    entities=[driver],
    ttl=timedelta(days=90),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
    ],
    online=True,
    source=driver_stats_source,
)
```
Write features to disk, apply configurations, and synchronize data to Redis:
```bash
# Create dummy data using Feast helper script
python3 -c "import os; os.system('feast apply')"
# Synchronize data to the online store (Redis)
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Data Leakage during Historical Joins
*   **Symptom**: The model achieves 99% accuracy during offline training but performs poorly (e.g., 50% accuracy) in live production testing.
*   **Root Cause**: Features were retrieved using incorrect entity timestamps during training dataset generation, leaking future data into training files.
*   **Resolution Strategy**:
    *   Inspect historical join commands:
        ```python
        # Verify timestamp mapping in entity dataframes
        training_df = store.get_historical_features(
            entity_df=entity_df, # Ensure entity_df contains correct event timestamps
            features=["driver_stats:conv_rate"]
        ).to_df()
        ```
    *   Verify features are retrieved using point-in-time timestamps.

### Task 10.2: Redis Out-Of-Memory Errors
*   **Symptom**: Serving requests fail with `OOM command not allowed when used memory > 'maxmemory'`.
*   **Root Cause**: Stale features are not expiring from Redis because the feature view definition is missing a TTL configuration or the Redis eviction policy is misconfigured.
*   **Resolution Strategy**:
    *   Inspect Redis memory usage:
        ```bash
        docker exec -it feast-redis redis-cli info memory
        ```
    *   Configure the Redis eviction policy to `allkeys-lru` in `/etc/redis/redis.conf`:
        ```ini
        maxmemory-policy allkeys-lru
        ```

---

## 11. Real Production Incidents

### Case Study: Silent Sync Job Failure
*   **Incident**: An enterprise feature store deployed a nightly cron job to synchronize features from an offline data warehouse to an online Redis database. The synchronization script failed silently due to an expired database password. Model inference services continued to consume stale features, leading to degraded prediction accuracy for several days before the anomaly was detected.
*   **Remediation**:
    *   Configured alerting on synchronization job status.
    *   Implemented checks in the inference code to verify feature freshness using timestamps.

---

## 12. Interview Questions

### Q1: Why do we need a Feature Store in production machine learning?
*   **Answer**: A Feature Store decouples feature engineering from model training and deployment. It provides a centralized catalog for feature sharing and reuse, and ensures consistency between offline training data and online inference features, preventing data leakage.

### Q2: What is a point-in-time join, and why is it critical?
*   **Answer**: A point-in-time join retrieves the latest value of a feature available *before* a specific historical event timestamp, preventing future data from leaking into the training dataset.

### Q3: Explain the difference between Feast and Tecton.
*   **Answer**:
    *   **Feast**: An open-source, client-side library. It manages metadata configurations and orchestrates copying data from offline to online stores, but does not run computation pipelines itself.
    *   **Tecton**: An enterprise platform. It runs and schedules feature computation pipelines, supports real-time stream ingestion, and provides advanced governance and access control features.

### Q4: How do you configure a feature store to serve features with low latency?
*   **Answer**: Use a low-latency key-value database (like Redis) as the online store, deploy it in a cluster configuration close to the inference services, and set appropriate TTLs to optimize memory usage.

### Q5: What is the risk of using long TTLs in the online store?
*   **Answer**: Long TTLs can cause the online store to accumulate stale data, leading to memory exhaustion and high hosting costs. Mitigate by setting appropriate TTLs based on feature freshness requirements.

---

## 13. Enterprise Case Studies

### Uber Michelangelo Feature Store
Uber developed **Michelangelo Palette**, a centralized feature store that manages feature pipelines across multiple engineering teams. By standardizing feature definitions and sharing calculated metrics (such as driver ratings and trip completion times) across models, they reduced duplicate data processing runs, saving infrastructure costs.

---

## 14. AI FDE Perspective

### Deploying Feast in On-Premises Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Offline Data Access**: If cloud databases are blocked, configure local PostgreSQL or Parquet files on shared network drives to serve as the offline store.
*   **Online Database Connection**: Deploy a local Redis instance and configure connection strings using custom network ports and passwords:
    ```yaml
    online_store:
      type: redis
      connection_string: redis://:pass@internal-redis.corp.local:6379
    ```
Ensure connection details are stored securely using local key vaults or environment variables.

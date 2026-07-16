# Module 10: Production Vector Database Operations

## 1. Theory (50%)

### Scalability

#### Horizontal Scaling
Add more query/serving nodes to distribute search load. Most vector databases (Milvus, Weaviate) support horizontal scaling by partitioning collections across nodes.

```
+--------------------------------------------------------------------------------------------------+
|                                Production Cluster Topology                                       |
|                                                                                                  |
|   +------------------+     +------------------+     +------------------+                         |
|   |   Query Node 1   |     |   Query Node 2   |     |   Query Node 3   |                         |
|   |  (Region: us-e1) |     |  (Region: us-w2) |     |  (Region: eu-w1) |                         |
|   +--------+---------+     +--------+---------+     +--------+---------+                         |
|            |                        |                        |                                   |
|            +------------------------+------------------------+                                   |
|                                     |                                                            |
|                             +-------+-------+                                                    |
|                             | Object Storage|                                                    |
|                             | (S3 / MinIO)  |                                                    |
|                             +---------------+                                                    |
+--------------------------------------------------------------------------------------------------+
```

#### Replication
Write vector data to multiple nodes simultaneously so that if one node fails, other nodes continue serving search queries without data loss.

#### Sharding
Distribute large collections across shards based on a partition key (e.g., tenant ID, document type) to prevent single-node bottlenecks.

---

### Reliability

#### Backups
Schedule regular index snapshots to object storage (S3/MinIO). Most vector databases support native snapshot APIs.

| Frequency | Scope | Target |
|---|---|---|
| Hourly | WAL / incremental | S3 bucket |
| Daily | Full index snapshot | S3 bucket with versioning |
| Weekly | Cross-region copy | Secondary region bucket |

#### Disaster Recovery
Restore from an S3 snapshot to a clean cluster node during outages. Test the restore procedure quarterly.

```bash
# Example: Milvus bulk import restore from S3
milvus-backup restore \
  --collection enterprise_knowledge \
  --backup-name daily_backup_20260716 \
  --storage s3://my-milvus-backups/
```

#### Failover
Configure health checks on load balancers to detect unresponsive query nodes and automatically re-route traffic to healthy replicas.

---

### Security

#### RBAC
Assign database roles to service accounts with minimum required permissions:
- `reader`: Execute search queries only.
- `writer`: Insert and update vectors.
- `admin`: Manage schemas, collections, and access policies.

#### Encryption
- **At-rest**: Enable AES-256 server-side encryption on the object storage bucket.
- **In-transit**: Enforce TLS 1.3 between the application and the vector database node.

#### Tenant Isolation
Use namespaces (Pinecone), collections (ChromaDB), or tenant classes (Weaviate) to isolate customer data at the database layer.

---

### Monitoring Metrics

| Metric | Description | Alert Threshold |
|---|---|---|
| Query Latency (p99) | 99th percentile search time | > 200ms |
| Recall@K | Fraction of relevant results in top-K | < 0.85 |
| Throughput (QPS) | Queries per second served | < target baseline |
| Index Size Growth | Rate of storage growth | > 20% per week |
| Error Rate | Query failures / total queries | > 0.1% |

---

## 2. Practical (50%)

### Monitoring Setup with Prometheus
Export vector database metrics to Prometheus and view them in Grafana.

```yaml
# prometheus.yml (scrape config example)
scrape_configs:
  - job_name: "milvus"
    static_configs:
      - targets: ["milvus-metrics:9091"]
  - job_name: "weaviate"
    static_configs:
      - targets: ["weaviate:2112"]
```

### Backup Strategy Script
```python
# /tmp/backup_strategy_check.py
import sys
import datetime

def simulate_backup_schedule():
    """Validates backup schedule configuration and reports plan."""
    now = datetime.datetime.utcnow()

    schedule = [
        {"type": "Incremental WAL",   "frequency": "Hourly",  "retention_days": 7},
        {"type": "Full Snapshot",     "frequency": "Daily",   "retention_days": 30},
        {"type": "Cross-Region Copy", "frequency": "Weekly",  "retention_days": 90},
    ]

    print("=== Vector DB Backup Schedule Validation ===")
    print(f"Current UTC Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")

    for job in schedule:
        print(f"  Type      : {job['type']}")
        print(f"  Frequency : {job['frequency']}")
        print(f"  Retention : {job['retention_days']} days")
        print(f"  Status    : CONFIGURED")
        print()

    print("Backup schedule verified successfully.")
    sys.exit(0)

if __name__ == "__main__":
    simulate_backup_schedule()
```

Run the script:
```bash
python3 /tmp/backup_strategy_check.py
```

### Disaster Recovery Test Checklist
```bash
# 1. Identify latest valid snapshot
milvus-backup list --storage s3://my-milvus-backups/

# 2. Restore snapshot to staging cluster
milvus-backup restore \
  --collection enterprise_knowledge \
  --backup-name <snapshot_name> \
  --storage s3://my-milvus-backups/

# 3. Validate restored record count
python3 -c "
client = connect_milvus()
count = client.count('enterprise_knowledge')
print(f'Restored records: {count}')
assert count > 0, 'DR test FAILED: empty collection'
print('DR test PASSED')
"

# 4. Run sample query and verify results
# 5. Promote staging to production if validated
```

### Capacity Planning Formula
```
Target Storage = (avg_vector_dim * 4 bytes) * total_vectors * replication_factor
               + (avg_metadata_size_bytes * total_vectors)

Example:
  1536 dim * 4 bytes = 6144 bytes/vector
  10M vectors        = ~58 GB raw vectors
  + metadata (512B)  = ~5 GB metadata
  * 3x replication   = ~189 GB total
```

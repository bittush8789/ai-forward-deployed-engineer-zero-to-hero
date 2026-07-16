# 03 MongoDB

## Theory & Architecture (Ubuntu Setup)
- **Installation**: `sudo apt-get update && sudo apt-get install -y mongodb-org`.
- **Service Management**: `sudo systemctl enable mongod && sudo systemctl start mongod`.
- **Architecture**: MongoDB is a **document‑oriented** NoSQL store using a **primary‑secondary replica set** model. Data lives as BSON documents, indexed via B‑Tree structures.
- **Key Components**: `mongod` (primary/secondary), `mongos` (sharding router), `config server` (metadata for sharding).

## Production Internals
- **Connection Pooling**: Handled by drivers; for Python use `pymongo.MongoClient(maxPoolSize=100)`.
- **Sharding**: Horizontal scaling via `sh.enableSharding("<db>")` and shard keys.
- **Backup & Recovery**: `mongodump` / `mongorestore` for logical backups; `fsync` + snapshot for physical backups.

## Business Use Cases
- Storing semi‑structured LLM chat logs.
- Catalog of product metadata for e‑commerce.
- Event sourcing streams for analytics.

## Schema Design Example
```js
// Example document for model metrics
{
  "metric_id": ObjectId(),
  "model_id": "c1f2e3a4-5678-90ab-cdef-1234567890ab",
  "metric_key": "accuracy",
  "value": 0.93,
  "ts": ISODate("2024-01-15T12:34:56Z")
}
```

## Query Design & Optimization
- Create **compound indexes** on frequently queried fields:
```js
db.model_metrics.createIndex({ model_id: 1, metric_key: 1 })
```
- Use **covered queries** to avoid fetching the full document.

## Performance Tuning (Ubuntu)
```bash
# Increase WiredTiger cache size (e.g., 4GB)
sudo sed -i "s/^#storage.engineConfig.cacheSizeGB:.*/storage.engineConfig.cacheSizeGB: 4/" /etc/mongod.conf
sudo systemctl restart mongod
```

## Scalability Patterns
- **Replica Sets** for high availability (primary + secondary).
- **Sharding** for write‑heavy workloads, using a hashed shard key for uniform distribution.

## Security Considerations
- Enable **TLS/SSL** (`net.tls.mode: requireTLS`).
- Use **SCRAM‑SHA‑256** authentication.
- **Role‑Based Access Control** (RBAC) for fine‑grained permissions.

## Monitoring Strategy
- **mongostat** and **mongotop** for real‑time metrics.
- **Prometheus MongoDB exporter**.
- Alerts for replication lag and oplog size.

## Hands‑On Lab (Ubuntu)
1. Install MongoDB and start the service.
2. Create a `model_metrics` collection and insert 500k synthetic documents using the Python script `mongodb_demo.py`.
3. Create a compound index and run an aggregation query.
4. Set up a secondary node for replication.

## Real Production Incident
*Incident*: Oplog overflow caused replication lag after a bulk import. *Resolution*: Increased `oplogSizeMB`, throttled import rate, and applied indexed import.

## Interview Questions
- How does MongoDB achieve atomicity at the document level?
- Explain the difference between a **replica set** and a **sharded cluster**.
- What is the purpose of the **oplog**?

## Enterprise Case Study
**AdTech Corp.** uses MongoDB to store billions of user event logs, leveraging sharding on `event_type` and a TTL index for automatic expiration, achieving sub‑second query latency.

## AI FDE Perspective
Front‑end services query MongoDB via a **GraphQL API** that aggregates recent chat messages. Use read‑through caching (Redis) for low‑latency UI updates.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import os
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime

# Connect to local MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['ai_platform']
metrics = db['model_metrics']

# Insert a sample document
doc = {
    "metric_id": str(uuid4()),
    "model_id": str(uuid4()),
    "metric_key": "accuracy",
    "value": 0.95,
    "ts": datetime.utcnow()
}
metrics.insert_one(doc)
print('Inserted sample metric into MongoDB.')
client.close()
```
Save as `mongodb_demo.py` in `databases/projects/` and run `python3 mongodb_demo.py`.

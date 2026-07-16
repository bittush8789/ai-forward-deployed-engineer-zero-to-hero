# 06 Neo4j

## Theory & Architecture (Ubuntu Setup)
- **Installation**: Use Docker for a quick Ubuntu‑compatible setup.
  ```bash
  sudo apt-get update && sudo apt-get install -y docker.io
  sudo systemctl start docker && sudo systemctl enable docker
  docker pull neo4j:5
  docker run -p 7474:7474 -p 7687:7687 -d --name neo4j5 \
    -e NEO4J_AUTH=neo4j/securepassword neo4j:5
  ```
- **Service Management**: Manage the container with `docker start/stop/restart`.
- **Architecture**: Neo4j is a **native graph database** that stores data as **nodes**, **relationships**, and **properties**. It uses a **property graph model** with ACID transactions and a **single‑writer lock** per transaction.
- **Key Components**: **Bolt protocol** (port 7687) for drivers, **HTTP API** (port 7474), **Cypher query engine**, **transaction log**, **store files**.

## Production Internals
- **Clustering**: Causal clustering with **core members** (leader election) and **read replicas** for scale‑out reads.
- **Backup & Recovery**: `neo4j-admin backup` for online backups; restore with `neo4j-admin restore`.
- **Monitoring**: Expose metrics via **Prometheus exporter** (`neo4j_exporter`).

## Business Use Cases
- Knowledge graphs for LLM retrieval augmentation.
- Recommendation engines (e.g., product‑to‑product).
- Network analysis for cybersecurity.

## Schema Design Example
```cypher
// Create constraints (equivalent to indexes)
CREATE CONSTRAINT unique_model IF NOT EXISTS ON (m:Model) ASSERT m.id IS UNIQUE;
CREATE CONSTRAINT unique_metric IF NOT EXISTS ON (mt:Metric) ASSERT mt.id IS UNIQUE;

// Sample nodes and relationship
CREATE (m:Model {id: randomUUID(), name: 'gpt-x', version: 'v1.0', createdAt: datetime()});
CREATE (mt:Metric {id: randomUUID(), key: 'accuracy', value: 0.95, ts: datetime()});
CREATE (m)-[:HAS_METRIC]->(mt);
```

## Query Design & Optimization
- Use **profile** and **explain** to view execution plans.
- Leverage **relationship directionality** and **node labels** for selective scans.
```cypher
PROFILE MATCH (m:Model)-[:HAS_METRIC]->(mt:Metric)
WHERE m.name = 'gpt-x' AND mt.key = 'accuracy'
RETURN m, mt
```
- **Indexes** on frequently filtered properties (`Model.id`, `Metric.key`).

## Performance Tuning (Ubuntu)
```bash
# Increase heap size (e.g., 4G) in neo4j.conf
sudo docker exec -it neo4j5 bash -c "echo 'dbms.memory.heap.initial_size=4g' >> /var/lib/neo4j/conf/neo4j.conf"
sudo docker exec -it neo4j5 bash -c "echo 'dbms.memory.heap.max_size=4g' >> /var/lib/neo4j/conf/neo4j.conf"
# Restart container
docker restart neo4j5
```

## Scalability Patterns
- **Causal clustering**: 3 core members + read replicas for fault tolerance.
- **Read‑only replicas** to offload analytical queries.
- **Neo4j Fabric** for federated queries across multiple databases.

## Security Considerations
- Enable **TLS** (`dbms.connector.bolt.tls_level=REQUIRED`).
- Use **role‑based access control** (`dbms.security.auth_enabled=true`).
- Restrict **Bolt** access to internal network only.

## Monitoring Strategy
- **neo4j-admin stats** for internal metrics.
- **Prometheus exporter** for CPU, heap, query latency.
- Alerts for **gc pauses**, **transaction log size**, **cluster health**.

## Hands‑On Lab (Ubuntu)
1. Run the Neo4j Docker container.
2. Execute the Cypher schema script using `cypher-shell` (`docker exec -it neo4j5 cypher-shell -u neo4j -p securepassword`).
3. Run the Python script `neo4j_demo.py` (see `databases/projects/`) to create nodes, relationships, and perform a query.
4. Observe the query plan using `EXPLAIN`.

## Real Production Incident
*Incident*: Transaction deadlock due to concurrent writes on the same node. *Resolution*: Implemented **optimistic concurrency** with `transaction timeout` and re‑tried failed transactions.

## Interview Questions
- How does Neo4j ensure ACID compliance for graph operations?
- Explain the difference between **core members** and **read replicas** in causal clustering.
- What is the purpose of **Fabric**?

## Enterprise Case Study
**SearchCo** uses Neo4j to model product relationships and complement Elasticsearch vector search, enabling context‑aware recommendations with sub‑50 ms latency.

## AI FDE Perspective
Front‑end UI calls a GraphQL façade that translates to Cypher queries, retrieving related entities for contextual AI suggestions. Caches results in Redis for repeated UI interactions.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
from neo4j import GraphDatabase
import uuid
import os

# Connect to the Neo4j Bolt endpoint
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "securepassword"))

def create_model_and_metric(tx, model_id, metric_id):
    tx.run(
        """
        MERGE (m:Model {id: $model_id})
        SET m.name = 'gpt-x', m.version = 'v1.0', m.createdAt = datetime()
        MERGE (mt:Metric {id: $metric_id})
        SET mt.key = 'accuracy', mt.value = 0.95, mt.ts = datetime()
        MERGE (m)-[:HAS_METRIC]->(mt)
        """,
        model_id=model_id,
        metric_id=metric_id,
    )

with driver.session() as session:
    model_id = str(uuid.uuid4())
    metric_id = str(uuid.uuid4())
    session.write_transaction(create_model_and_metric, model_id, metric_id)
    print(f"Created Model {model_id} with Metric {metric_id}")

# Query example
with driver.session() as session:
    result = session.run(
        """
        MATCH (m:Model)-[:HAS_METRIC]->(mt:Metric)
        WHERE m.name = 'gpt-x' AND mt.key = 'accuracy'
        RETURN m.id AS model_id, mt.value AS accuracy
        """
    )
    for record in result:
        print(f"Model {record['model_id']} has accuracy {record['accuracy']}")

driver.close()
```
Save as `neo4j_demo.py` in `databases/projects/` and run `python3 neo4j_demo.py`.

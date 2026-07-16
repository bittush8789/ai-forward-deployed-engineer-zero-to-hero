# 05 Elasticsearch

## Theory & Architecture (Ubuntu Setup)
- **Installation**: Use Docker for a quick setup on Ubuntu.
  ```bash
  sudo apt-get update && sudo apt-get install -y docker.io
  sudo systemctl start docker && sudo systemctl enable docker
  docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.0
  docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" --name es8 docker.elastic.co/elasticsearch/elasticsearch:8.12.0
  ```
- **Service Management**: The container can be managed with `docker start`, `docker stop`, and `docker restart`.
- **Architecture**: Elasticsearch is a **distributed search and analytics engine** built on top of Lucene. Data is stored in **indices** made of **shards**, each replicated for high availability.
- **Key Components**: **Cluster Manager**, **Data Nodes**, **Ingest Nodes**, **Coordinating Nodes**, **Lucene segments**.

## Production Internals
- **Indexing Pipeline**: Documents pass through **ingest processors** (pipeline) before being written to a shard.
- **Replication**: Primary shards replicate to replica shards (default 1 replica). Failover is automatic.
- **Backup & Recovery**: Use **snapshot/restore** APIs; snapshots can be stored on S3, Azure Blob, or local filesystem.

## Business Use Cases
- Vector similarity search for RAG and LLM retrieval.
- Full‑text search for SaaS document portals.
- Real‑time analytics dashboards for AI model monitoring.

## Schema Design Example
```json
PUT /ai_models
{
  "mappings": {
    "properties": {
      "model_id": { "type": "keyword" },
      "name": { "type": "text" },
      "version": { "type": "keyword" },
      "created_at": { "type": "date" },
      "embedding": { "type": "dense_vector", "dimensions": 768 }
    }
  }
}
```

## Query Design & Optimization
- **BM25** for classic full‑text relevance.
- **k‑NN** (approximate nearest neighbor) for vector search:
```json
GET /ai_models/_search
{
  "size": 5,
  "query": {
    "knn": {
      "embedding": {
        "vector": [0.12, 0.45, ...],
        "k": 5
      }
    }
  }
}
```
- Use **routing** to target specific shards for faster queries.

## Performance Tuning (Ubuntu)
```bash
# Increase JVM heap (e.g., 4GB)
sudo docker exec -it es8 /bin/bash -c "echo 'ES_JAVA_OPTS=\"-Xms4g -Xmx4g\"' >> /usr/share/elasticsearch/config/jvm.options"
# Set refresh interval to 30s for bulk indexing
curl -XPUT 'localhost:9200/ai_models/_settings' -H 'Content-Type: application/json' -d '{"index" : {"refresh_interval" : "30s"}}'
```

## Scalability Patterns
- **Horizontal scaling** by adding data nodes; shards are rebalanced automatically.
- **Cross‑cluster search** to query remote clusters.
- **Index lifecycle management (ILM)** to roll over, shrink, and delete old indices.

## Security Considerations
- Enable **TLS** for transport and HTTP (`xpack.security.enabled=true`).
- Use **API keys** or **basic auth** for client authentication.
- Apply **role‑based access control (RBAC)** to restrict index privileges.

## Monitoring Strategy
- **Elastic Stack** (Kibana) for UI dashboards.
- **Elasticsearch Exporter** for Prometheus metrics.
- Alerts for **cluster health**, **node disk watermarks**, **search latency**.

## Hands‑On Lab (Ubuntu)
1. Pull and run the Elasticsearch Docker container.
2. Create the `ai_models` index with the mapping above using `curl`.
3. Run the Python script `es_demo.py` (see `databases/projects/`) to bulk‑index 10 k synthetic vectors.
4. Perform a k‑NN search and observe latency.
5. Take a snapshot to a local directory and restore it.

## Real Production Incident
*Incident*: Cluster yellow state after a node restart due to missing replica allocation. *Resolution*: Adjust `cluster.routing.allocation.enable` and increased replica count, then performed a rolling restart.

## Interview Questions
- What is the role of a **primary shard** vs a **replica shard**?
- How does Elasticsearch store vector embeddings and perform k‑NN search?
- Explain **index lifecycle management** and why it matters.

## Enterprise Case Study
**AI‑Search Inc.** stores LLM embeddings in Elasticsearch, using 8 data nodes and 2 replica shards per index. They achieve sub‑30 ms vector search latency for 1 M‑scale document corpus.

## AI FDE Perspective
Front‑end UI components query the Elasticsearch k‑NN endpoint via a thin REST layer, caching the top‑k results in Redis for ultra‑low latency UI rendering.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import os
import json
import random
from elasticsearch import Elasticsearch, helpers

# Connect to local Elasticsearch container
es = Elasticsearch(['http://localhost:9200'], timeout=30)

# Ensure the index exists (create if missing)
index_name = 'ai_models'
if not es.indices.exists(index=index_name):
    mapping = {
        "mappings": {
            "properties": {
                "model_id": {"type": "keyword"},
                "name": {"type": "text"},
                "version": {"type": "keyword"},
                "created_at": {"type": "date"},
                "embedding": {"type": "dense_vector", "dimensions": 768}
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")

# Generate synthetic documents
def gen_docs(num):
    for _ in range(num):
        yield {
            "_index": index_name,
            "_id": str(random.randint(1, 1_000_000)),
            "_source": {
                "model_id": f"model-{random.randint(1,100)}",
                "name": "gpt-x",
                "version": "v1.0",
                "created_at": "2024-01-01T00:00:00Z",
                "embedding": [random.random() for _ in range(768)]
            }
        }

# Bulk index 10k documents
helpers.bulk(es, gen_docs(10000))
print('Indexed 10k synthetic embeddings.')

# Perform a k‑NN search
query_vec = [random.random() for _ in range(768)]
resp = es.search(
    index=index_name,
    body={
        "size": 5,
        "query": {"knn": {"embedding": {"vector": query_vec, "k": 5}}}
    }
)
print('Top‑5 nearest neighbors:')
for hit in resp['hits']['hits']:
    print(hit['_id'], hit['_score'])
```
Save as `es_demo.py` in `databases/projects/` and run `python3 es_demo.py`.

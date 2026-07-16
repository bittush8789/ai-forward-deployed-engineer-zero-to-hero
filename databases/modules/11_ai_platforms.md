# 11 AI Platform Integration

## Theory & Architecture (Ubuntu Setup)
- **Installation**: All required services are already covered in previous modules. Ensure Docker is installed for Elasticsearch and Neo4j:
  ```bash
  sudo apt-get update && sudo apt-get install -y docker.io
  ```
- **Data Flow Overview**:
  1. **Metadata Store** – PostgreSQL holds model versioning, experiment logs, and relational data.
  2. **Cache Layer** – Redis caches recent inference results and rate‑limits API calls.
  3. **Vector Store** – Elasticsearch stores dense embeddings for Retrieval‑Augmented Generation (RAG).
  4. **Graph Store** – Neo4j models relationships between entities, enabling contextual reasoning.
  5. **Document Store** – MongoDB keeps semi‑structured chat logs and event streams.
- **Orchestration** – A thin Python orchestration layer (`ai_platform_orchestrator.py`) ties these components together, exposing a simple REST endpoint for front‑end services.

## Production Internals
- **Transactional Guarantees** – Use PostgreSQL for ACID‑critical writes. Other stores employ *eventual consistency*; orchestrator writes to PostgreSQL first, then asynchronously propagates to Redis, Elasticsearch, Neo4j, and MongoDB.
- **Idempotency** – All write operations include a UUID request ID; duplicate submissions are ignored.
- **Observability** – Unified logging (JSON) sent to a central ELK stack; traces collected via OpenTelemetry.
- **Failover Strategy** – If any downstream store is unavailable, the orchestrator falls back to cached data and queues the write for later retry.

## Business Use Cases
- End‑to‑end LLM inference pipeline with real‑time prompt caching.
- Knowledge‑graph‑augmented search for enterprise document portals.
- Multi‑tenant SaaS platform where each tenant’s data lives across the five stores.

## Hands‑On Lab (Ubuntu)
1. Ensure all services are running (PostgreSQL, Redis, Elasticsearch container, Neo4j container, MongoDB).
2. Run the orchestration script `ai_platform_orchestrator.py` (located in `databases/projects/`). It will:
   - Insert a new model record into PostgreSQL.
   - Cache a dummy inference result in Redis.
   - Index a synthetic embedding into Elasticsearch.
   - Create a node/relationship in Neo4j.
   - Store a chat log document in MongoDB.
   - Print a summary of all operations.
3. Verify each store individually (e.g., `psql`, `redis-cli`, `curl` to Elasticsearch, `cypher-shell`, `mongo`).

## Real Production Incident
*Incident*: During a rolling upgrade, the orchestrator attempted writes to Elasticsearch before it was ready, causing `cluster_block_exception`. *Resolution*: Added a health‑check retry loop with exponential backoff before indexing vectors.

## Interview Questions
- How would you guarantee *exactly‑once* semantics across heterogeneous stores?
- Explain the trade‑offs of storing embeddings in Elasticsearch vs. a dedicated vector DB.
- What monitoring metrics are critical for a multi‑store AI platform?
- How does Neo4j’s causal clustering affect write latency?

## AI FDE Perspective
Front‑end UI components call the orchestrator via `/api/v1/inference`. The orchestrator returns cached results instantly (Redis) while asynchronously persisting the full payload across the backend stores. UI engineers rely on consistent response schemas regardless of the underlying storage.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import os, json, uuid, time
import psycopg2
import redis
from elasticsearch import Elasticsearch, helpers
from pymongo import MongoClient
from neo4j import GraphDatabase

# --- PostgreSQL (metadata) ---
pg_conn = psycopg2.connect(dbname='postgres', user=os.getenv('USER'))
pg_cur = pg_conn.cursor()
model_id = str(uuid.uuid4())
pg_cur.execute(
    "INSERT INTO ai_models (model_id, name, version) VALUES (%s, %s, %s)",
    (model_id, 'gpt-x', 'v1.0')
)
pg_conn.commit()
print('PostgreSQL: model metadata inserted')
pg_cur.close()
pg_conn.close()

# --- Redis (cache) ---
redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.setex(f'inference:{model_id}', 300, json.dumps({'result': 'cached answer'}))
print('Redis: cached inference stored')

# --- Elasticsearch (vector store) ---
es = Elasticsearch(['http://localhost:9200'])
index = 'ai_models'
if not es.indices.exists(index=index):
    es.indices.create(index=index, body={
        "mappings": {"properties": {"embedding": {"type": "dense_vector", "dimensions": 768}}}
    })
    print('Elasticsearch: index created')
# Index a synthetic embedding
embedding = [float(i)/768 for i in range(768)]
es.index(index=index, id=model_id, body={"embedding": embedding})
print('Elasticsearch: embedding indexed')

# --- Neo4j (graph) ---
neo_uri = 'bolt://localhost:7687'
neo_driver = GraphDatabase.driver(neo_uri, auth=('neo4j', 'securepassword'))

def create_graph(tx, mid):
    tx.run(
        """MERGE (m:Model {id: $mid}) SET m.name = 'gpt-x' RETURN m""",
        mid=mid)

with neo_driver.session() as session:
    session.write_transaction(create_graph, model_id)
print('Neo4j: model node created')
neo_driver.close()

# --- MongoDB (document store) ---
mongo_client = MongoClient('mongodb://localhost:27017/')
chat_coll = mongo_client['ai_platform']['chat_logs']
chat_coll.insert_one({
    "model_id": model_id,
    "user": "alice",
    "message": "How does reinforcement learning work?",
    "timestamp": time.time()
})
print('MongoDB: chat log inserted')

print('All components updated successfully.')
```
Save as `ai_platform_orchestrator.py` in `databases/projects/` and run `python3 ai_platform_orchestrator.py`.

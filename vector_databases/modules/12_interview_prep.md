# Module 12: Interview Preparation - Vector Databases, RAG and AI Search

---

## Pinecone Interview Questions

### Q1: What is the difference between an Index and a Namespace in Pinecone?
**Answer:**
- An **Index** is the top-level Pinecone resource that holds all vectors and defines the embedding dimension, distance metric, and pod configuration.
- A **Namespace** is a logical partition *within* an index used to isolate groups of vectors. Queries are scoped to a specific namespace, enabling multi-tenancy without creating separate indexes.

**Key distinction**: You pay for one index but can have unlimited namespaces. Namespaces are ideal for separating tenant data (e.g., `namespace="bank-a"`) without duplicating infrastructure costs.

---

### Q2: How does Pinecone's Serverless differ from Pod-based architecture?
**Answer:**
- **Pod-based**: Fixed compute pods (s1, p1, p2) that you provision upfront. You pay for the pod capacity regardless of query volume.
- **Serverless**: Compute scales automatically on demand and decouples storage (cloud object storage) from compute (ephemeral query nodes). You pay only for storage and query units consumed.

**When to use which**: Serverless is best for variable, unpredictable workloads. Pod-based gives predictable latency for consistent high-throughput applications.

---

### Q3: How does Metadata Filtering work in Pinecone?
**Answer:**
Pinecone stores key-value metadata alongside each vector. At query time, you can append a filter expression to restrict the search to only vectors matching certain metadata values.

```python
# Only retrieve vectors where dept = "claims"
index.query(
    vector=query_embedding,
    filter={"dept": {"$eq": "claims"}},
    top_k=5
)
```

**Important**: Metadata filtering happens *before* the similarity search narrows results, so it is a pre-filter, not a post-filter.

---

## ChromaDB Interview Questions

### Q4: What is a ChromaDB Collection and how does it differ from a Pinecone Namespace?
**Answer:**
- A ChromaDB **Collection** is the primary data container holding documents, their vector embeddings, and metadata. Each collection is independent and has its own embedding function.
- A Pinecone **Namespace** is a lightweight partition *within* a shared index — they share the same dimension and distance metric.

**Practical difference**: ChromaDB collections are more isolated and configurable (each can use a different embedding model). Pinecone namespaces are lightweight partitions that share the parent index's configuration.

---

### Q5: How does ChromaDB handle persistence?
**Answer:**
By default, ChromaDB runs in-memory. To persist data to disk, you initialize the client with a `persist_directory`:

```python
import chromadb
client = chromadb.PersistentClient(path="/data/chroma")
```

ChromaDB serializes the collection index and metadata to the specified directory using SQLite and parquet files.

---

## Weaviate Interview Questions

### Q6: How does Weaviate Hybrid Search work?
**Answer:**
Weaviate Hybrid Search combines BM25 keyword search with dense vector search using Reciprocal Rank Fusion (RRF):

1. BM25 ranks results by keyword term frequency.
2. Dense vector search ranks results by cosine similarity.
3. RRF normalizes both rank lists and merges them: `score = 1 / (60 + rank)`.
4. Results are sorted by the combined RRF score.

The `alpha` parameter controls the balance:
- `alpha=0` → pure BM25 (keyword only).
- `alpha=1` → pure vector (semantic only).
- `alpha=0.5` → equal weighting (default).

---

### Q7: How do you design a Weaviate Schema for Multi-Tenancy?
**Answer:**
Enable the `multiTenancyConfig` on the class definition and use tenant-scoped API calls:

```python
# Create class with multi-tenancy enabled
client.schema.create_class({
    "class": "PolicyDocument",
    "multiTenancyConfig": {"enabled": True}
})
# Add tenants
client.schema.add_class_tenants("PolicyDocument", [{"name": "bank-a"}, {"name": "bank-b"}])
# Insert with tenant scope
client.data_object.create(
    {"content": "Policy details..."},
    "PolicyDocument",
    tenant="bank-a"
)
```

This ensures complete data isolation between tenants within a single Weaviate instance.

---

## Milvus Interview Questions

### Q8: What are the four node types in Milvus and what does each do?
**Answer:**
| Node | Role |
|---|---|
| **Root Coord** | Manages metadata, schema, and coordinates write operations |
| **Query Node** | Loads collection segments into memory and serves search queries |
| **Data Node** | Receives write operations, flushes segments to object storage |
| **Index Node** | Builds vector indices (IVF, HNSW) from raw segments |

Decoupling these roles enables independent horizontal scaling — add more Query Nodes for read-heavy workloads, more Data Nodes for write-heavy ingestion.

---

### Q9: What are the different Index Types in Milvus and when do you use each?
**Answer:**
| Index | Speed | Accuracy | Memory | Use Case |
|---|---|---|---|---|
| FLAT | Slow | 100% | Low | Small datasets, exact search |
| IVF_FLAT | Fast | ~95% | Medium | Medium datasets |
| IVF_SQ8 | Faster | ~90% | Low | Memory-constrained clusters |
| HNSW | Very fast | ~97% | High | Large datasets, low latency |
| IVF_PQ | Fastest | ~85% | Very low | Billion-scale, memory critical |

---

## FAISS Interview Questions

### Q10: Explain IVF, HNSW, and PQ indexes in FAISS.
**Answer:**
- **IVF (Inverted File)**: Uses k-means to partition vectors into N clusters. At search time, only the nearest clusters are scanned (controlled by `nprobe`). Lower `nprobe` = faster but lower recall.
- **HNSW (Hierarchical Navigable Small World)**: Graph-based index where each vector is connected to its nearest neighbors across multiple layers. Very fast search but requires high memory to store the graph.
- **PQ (Product Quantization)**: Compresses each vector by splitting it into sub-vectors and quantizing each sub-vector. Trades accuracy for dramatic memory savings (4-16x compression).

**Best practice**: Use `IndexIVFPQ` for billion-scale datasets where memory is the primary constraint.

---

## Retrieval and RAG Interview Questions

### Q11: What is the difference between Semantic Search and Hybrid Search?
**Answer:**
- **Semantic Search**: Uses only dense vector embeddings to match meaning. Fails on exact keyword matches (e.g., "Regulation 4.2.1.b" may not match if the phrasing differs).
- **Hybrid Search**: Combines BM25 (keyword) and dense vector search using RRF. Captures both exact keyword matches AND semantic intent, improving recall for enterprise use cases.

**Rule of thumb**: Always use Hybrid Search in production RAG systems for enterprise documents, as they often contain IDs, codes, and exact terminology that semantic search misses.

---

### Q12: What is Chunking and what chunk size should you use?
**Answer:**
Chunking splits documents into smaller segments before embedding. The optimal chunk size depends on the use case:

| Use Case | Chunk Size | Overlap |
|---|---|---|
| Q&A over policies | 256-512 tokens | 50 tokens |
| Long-form summarization | 1024 tokens | 100 tokens |
| Code retrieval | Function/class boundaries | None |
| Tabular data | Row groups | None |

**Key insight**: Smaller chunks improve precision (less irrelevant noise per chunk) but reduce context completeness. Larger chunks provide more context but dilute the semantic signal of the embedding.

---

## System Design Interview Questions

### Q13: Design the Retrieval Layer for a ChatGPT-like System
**Approach:**
1. **Ingestion Pipeline**: Document crawler --> chunker (512 tokens) --> embedding worker (text-embedding-3-large) --> Pinecone namespace per user/tenant.
2. **Query Pipeline**: User query --> embedding --> Pinecone vector search (top-20) + Elasticsearch BM25 (top-20) --> RRF merge (top-10) --> Cohere rerank (top-3) --> GPT-4o prompt.
3. **Caching**: Cache frequently queried vector results in Redis (TTL 1 hour) to reduce vector DB load.
4. **RBAC**: Append user role to metadata filter in every vector query.

---

### Q14: Design an Enterprise Multi-Tenant RAG Platform
**Approach:**
1. **Tenant Isolation**: Separate Pinecone namespace (or Weaviate tenant class) per customer.
2. **Ingestion**: Tenant-specific Kafka topics route document events to isolated embedding workers.
3. **Query Gateway**: FastAPI validates JWT, extracts tenant ID, appends namespace/metadata filter to queries.
4. **Monitoring**: Track per-tenant QPS, latency, and token consumption in Prometheus.
5. **Billing**: Export token usage metrics to a billing database for per-tenant invoicing.

---

### Q15: Design a Vector Database Disaster Recovery Plan
**Approach:**
1. **Hourly**: Snapshot WAL (write-ahead log) to S3 with 7-day retention.
2. **Daily**: Full collection snapshot to S3 with 30-day retention and cross-region copy.
3. **Recovery RTO Target**: 30 minutes (restore snapshot + validate + promote).
4. **DR Test**: Monthly restore drill to a staging cluster with record count validation query.
5. **Failover**: Use a load balancer health check to auto-route to secondary cluster if primary fails.

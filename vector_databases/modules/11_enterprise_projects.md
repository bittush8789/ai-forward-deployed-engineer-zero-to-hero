# Module 11: Enterprise Projects - Portfolio Blueprints

## Project 1: Enterprise Knowledge Assistant (LangChain + Pinecone + OpenAI)

### Business Problem
Enterprise teams spend hours searching scattered PDF policies and SOPs. An AI knowledge assistant reduces search time from hours to seconds.

### Architecture
```
User Query
    --> FastAPI Gateway (RBAC validation)
    --> Embedding Service (text-embedding-3-small)
    --> Pinecone Namespace Query (dept filter in metadata)
    --> Cohere Rerank (top 5 --> top 2)
    --> OpenAI GPT-4o (RAG prompt injection)
    --> Response with citations
```

### Key Implementation Points
- **Namespaces**: Separate Pinecone namespace per department (e.g., `claims`, `underwriting`, `legal`).
- **Metadata Filtering**: Append `{"dept": user.department}` to every query to enforce RBAC at the retrieval layer.
- **Audit Logging**: Write `(user_id, query, chunk_ids, response_snippet, timestamp)` to PostgreSQL.
- **Chunking**: Use recursive character splitter at 512 tokens with 50-token overlap.

### Tech Stack
- LangChain for orchestration
- Pinecone for vector storage
- OpenAI for embeddings and generation
- FastAPI for the REST gateway
- PostgreSQL for audit logs
- Docker + Kubernetes for deployment

---

## Project 2: Enterprise Search Platform (Weaviate + Elasticsearch + FastAPI)

### Business Problem
Enterprise search must handle both semantic intent and exact keyword matches (e.g., contract IDs, regulation codes). A single search approach fails to cover both use cases.

### Architecture
```
User Query
    --> Query Planner (route to semantic OR hybrid)
    --> Weaviate (semantic vector search)
    --> Elasticsearch (BM25 keyword search)
    --> RRF Combiner (normalize and merge rankings)
    --> Cohere Rerank
    --> FastAPI Response
```

### Key Implementation Points
- **Hybrid Routing**: Detect if the query contains exact codes or IDs and increase BM25 weight (alpha < 0.3). For conceptual queries, increase vector weight (alpha > 0.7).
- **Schema Design**: Weaviate `SearchDocument` class with properties: `content`, `source`, `document_type`, `tenant_id`.
- **Elasticsearch Index**: Separate BM25 index mirroring Weaviate data for keyword-specific fallback searches.

### Tech Stack
- Weaviate for vector/hybrid search
- Elasticsearch for keyword search
- FastAPI for the REST gateway
- Docker Compose for local dev

---

## Project 3: Insurance Knowledge Copilot (ChromaDB + OpenAI + RAG)

### Business Problem
Insurance underwriters and claims adjusters need instant access to policy manuals, regulatory documents, and claim history to make accurate decisions.

### Architecture
```
Document Upload (PDF/Word)
    --> DocParser (PyMuPDF/Unstructured)
    --> Chunker (512 tokens, 50 overlap)
    --> Embedding (text-embedding-3-small)
    --> ChromaDB collection (persistent local storage)
    --> Query --> RAG response
```

### Key Implementation Points
- **Local-First**: ChromaDB runs in-process, enabling deployment in secure environments without cloud dependencies.
- **Multi-Collection Design**: Separate ChromaDB collections per document category: `policy_manuals`, `regulatory_docs`, `claim_forms`.
- **Metadata Schema**: `{"doc_type": "policy", "effective_date": "2025-01-01", "jurisdiction": "CA"}`.

### Tech Stack
- ChromaDB for local vector storage
- OpenAI for embeddings and generation
- FastAPI for the REST gateway
- PyMuPDF for PDF parsing

---

## Project 4: AI Agent Memory Platform (FAISS + Redis + LangGraph)

### Business Problem
AI agents executing multi-step workflows lose context between conversation turns. An agent memory platform provides short-term working memory and long-term episodic memory.

### Architecture
```
Agent Turn N
    --> Short-Term Memory (Redis, last 10 turns)
    --> Long-Term Memory (FAISS index of past episodes)
    --> Memory Retriever (fetch relevant past context)
    --> LangGraph Agent State (merged context)
    --> Tool Execution
    --> Memory Writer (update Redis + FAISS)
```

### Key Implementation Points
- **Memory Tiers**: Redis handles last-N turn history (fast). FAISS handles vector search across all past episodes (slower but unlimited scale).
- **FAISS Index Type**: Use `IndexHNSWFlat` for fast approximate search across episode embeddings.
- **Memory Decay**: Prune Redis entries older than 1 hour; archive to FAISS for long-term retention.

### Tech Stack
- FAISS for long-term episodic memory
- Redis for short-term working memory
- LangGraph for agent state management
- FastAPI for the memory API

---

## Project 5: Large Scale Enterprise RAG Platform (Milvus + Kubernetes + vLLM)

### Business Problem
Fortune 500 enterprises need a scalable RAG platform that can index millions of enterprise documents and serve hundreds of concurrent users with sub-200ms query latency.

### Architecture
```
Document Ingestion (Kafka)
    --> Embedding Workers (GPU pods, vLLM embedding endpoint)
    --> Milvus Cluster (distributed, 3 query nodes, 3 data nodes)
    --> Query Gateway (FastAPI, Kubernetes HPA)
    --> Reranker (BGE Reranker, GPU pod)
    --> vLLM Serving (LLaMA-3 70B, tensor parallel)
    --> Response
```

### Key Implementation Points
- **Scale Target**: 50 million vector records, 500 QPS, p99 latency under 200ms.
- **Milvus Partitioning**: Partition by `tenant_id` to enable per-tenant data isolation within shared collections.
- **HPA Policy**: Scale query gateway pods based on CPU utilization (target 60%).
- **GPU Scheduling**: Use Kubernetes node selectors to schedule vLLM and embedding pods on GPU nodes.

### Tech Stack
- Milvus for distributed vector storage
- vLLM for high-throughput LLM and embedding serving
- Kubernetes (EKS) for orchestration
- Kafka for document ingestion events
- ArgoCD for GitOps deployment
- Prometheus + Grafana for monitoring

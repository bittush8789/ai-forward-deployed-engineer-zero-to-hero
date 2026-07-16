# Project 1: Enterprise RAG Platform (Knowledge Assistant)

## 1. Theory (20%)

### Business Problem
Large enterprises struggle to find information across thousands of scattered documents, Standard Operating Procedures (SOPs), policies, wikis, and PDFs. Employees waste hours searching, slowing down decision cycles and customer support response times.

```
+-------------------------------------------------------------------------------------------------+
|                                    Hybrid Retrieval Process                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       User Query                                        |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Semantic Search)                               v (Keyword Match)       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |          Dense Retrieval (Vector)       |     |          Sparse Retrieval (BM25)        |   |
|   |   - Matches semantic meaning            |     |   - Matches exact keywords              |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Reciprocal Rank Fusion - RRF)                 |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Rerank Engine (Cohere)                              |   |
|   |   - Evaluates and re-orders combined search results for optimal relevance                 |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Architectural Trade-offs
*   **Vector Search vs Hybrid Search**: Vector search alone misses exact keyword matches (like serial numbers or SKU codes). We select Hybrid Search (combining vector embeddings with BM25 keyword matching) and apply Cohere Rerank to optimize result relevance.

---

## 2. System Design (20%)

### High-Level Design (HLD)
The system consists of:
1.  **Ingestion Pipeline**: Asynchronously extracts text from PDFs and stores document chunks.
2.  **Embedding Worker**: Vectorizes text chunks and writes them to Pinecone/Qdrant.
3.  **Retrieval Gateway**: FastAPI backend that processes queries, runs hybrid searches, and calls the LLM.

### Security Design
*   **RBAC**: Append user group filters directly to the vector queries to ensure users only retrieve authorized documents.
*   **Audit Logging**: Log user IDs, queries, retrieved chunk IDs, and model parameters to PostgreSQL.

---

## 3. Implementation (30%)

### Code Structure
```
rag_platform/
├── app/
│   ├── api/
│   │   └── gateway.py       # Query processing & RAG orchestrator
│   ├── services/
│   │   ├── ingest.py        # Chunking & Embedding writer
│   │   └── retrieve.py      # Hybrid search client
│   └── main.py              # FastAPI app initialization
```

### Retrieval & Orchestration API
```python
# app/api/gateway.py
from fastapi import FastAPI, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time

app = FastAPI(title="Enterprise RAG API")
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    # Simulating Token & Group extraction
    return {"user": "alice", "groups": ["claims-reader"]}

@app.post("/api/v1/query")
def run_rag_query(query: str, auth = Depends(verify_token)):
    print(f"Auditing RAG call for {auth['user']} in {auth['groups']}")
    start = time.time()
    
    # Mock context retrieval
    retrieved_chunks = [
        {"id": "doc_101", "text": "Claim threshold limit is $5000.", "source": "SOP_12.pdf"}
    ]
    
    # Mock LLM generation
    response = "The claim threshold is $5000 according to SOP_12.pdf."
    
    return {
        "query": query,
        "response": response,
        "citations": retrieved_chunks,
        "latency_sec": time.time() - start
    }
```

---

## 4. DevOps & Operations (15%)

### Kubernetes Deployment
Deploy the RAG service to Kubernetes, configuring autoscaling based on query load:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-gateway
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: gateway
        image: rag-gateway:latest
        ports:
        - containerPort: 8000
```

---

## 5. AI FDE Perspective (15%)

### Business Value & ROI
*   **Baseline**: Employees spent an average of 30 minutes searching policies manually.
*   **Post-AI**: Search times reduced to seconds, saving 15 hours per employee monthly.
*   **Annual Savings**: For a 1000-user department, this saves 180,000 operational hours annually.

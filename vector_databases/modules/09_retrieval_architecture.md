# Module 9: Retrieval Architecture - End-to-End RAG Pipeline Design

## 1. Theory (50%)

### What is Retrieval Architecture?
Retrieval Architecture is the end-to-end pipeline that transforms raw documents into retrievable knowledge, enabling LLMs to answer questions grounded in factual data.

```
+--------------------------------------------------------------------------------------------------+
|                                   End-to-End Retrieval Pipeline                                  |
|                                                                                                  |
|   [Document]                                                                                     |
|       |                                                                                          |
|       v  (1. Chunking)                                                                           |
|   [Text Chunks]  <-- Split docs into 256-1024 token segments with overlap                       |
|       |                                                                                          |
|       v  (2. Embedding)                                                                          |
|   [Dense Vectors]  <-- Convert chunks to vectors using embedding model                          |
|       |                                                                                          |
|       v  (3. Indexing)                                                                           |
|   [Vector DB]  <-- Store vectors with metadata (source, dept, page)                             |
|       |                                                                                          |
|       v  (4. Query)                                                                              |
|   [Retriever]  <-- Query DB using user question embedding + metadata filters                    |
|       |                                                                                          |
|       v  (5. Reranking)                                                                          |
|   [Reranker]  <-- Re-score top-k retrieved chunks for relevance                                 |
|       |                                                                                          |
|       v  (6. Generation)                                                                         |
|   [LLM]  <-- Inject context chunks into prompt and generate answer                              |
+--------------------------------------------------------------------------------------------------+
```

### Core Components

#### 1. Chunking Strategies
| Strategy | Chunk Size | Overlap | Best For |
|---|---|---|---|
| Fixed-size | 512 tokens | 50 tokens | General documents |
| Sentence-based | Variable | 1-2 sentences | Q&A, summaries |
| Semantic (topic) | Variable | None | Research papers |
| Recursive character | 1024 tokens | 100 tokens | Code, PDFs |

#### 2. Metadata Injection
Tag every chunk with metadata to enable filtered retrieval:
- `source`: Document name / URL
- `department`: Owner department (for RBAC)
- `page_number`: Original page
- `created_at`: Ingestion timestamp

#### 3. Reranking
A second-pass model (Cohere Rerank, BGE Reranker) re-scores the top-k retrieved chunks to eliminate false positives before passing context to the LLM.

### Enterprise Topics
- **Retrieval Evaluation**: Measure retrieval quality using Context Precision, Context Recall, and Faithfulness (Ragas).
- **Chunking Optimization**: Test chunk sizes systematically — smaller chunks improve precision, larger chunks improve context completeness.
- **Metadata-Driven RBAC**: Append user department to vector queries to restrict retrieved context to authorized documents.

---

## 2. Practical (50%)

### Build an End-to-End Retrieval Pipeline
```python
# /tmp/retrieval_pipeline.py
import sys
import hashlib

# ---- Step 1: Mock Document Chunker ----
def chunk_document(text: str, chunk_size: int = 100, overlap: int = 20):
    """Split text into overlapping chunks by character count."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks


# ---- Step 2: Mock Embedding Generator ----
def generate_embedding(text: str) -> list:
    """Return a deterministic fake embedding based on text hash."""
    h = int(hashlib.md5(text.encode()).hexdigest(), 16)
    return [(h >> i & 0xFF) / 255.0 for i in range(8)]


# ---- Step 3: Mock Vector Store ----
class SimpleVectorStore:
    def __init__(self):
        self.store = []

    def upsert(self, chunk_id: str, text: str, embedding: list, metadata: dict):
        self.store.append({
            "id": chunk_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata
        })

    def search(self, query_embedding: list, top_k: int = 3, filter_dept: str = None):
        """Cosine similarity mock search with optional metadata filter."""
        import math

        def cosine(a, b):
            dot = sum(x*y for x,y in zip(a, b))
            norm_a = math.sqrt(sum(x**2 for x in a))
            norm_b = math.sqrt(sum(x**2 for x in b))
            return dot / (norm_a * norm_b + 1e-9)

        scored = []
        for item in self.store:
            if filter_dept and item["metadata"].get("dept") != filter_dept:
                continue
            score = cosine(query_embedding, item["embedding"])
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]


# ---- Step 4: Mock Reranker ----
def rerank(results: list, query: str) -> list:
    """Simple keyword-based reranker (simulates Cohere Rerank)."""
    keywords = query.lower().split()
    scored = []
    for item in results:
        score = sum(1 for kw in keywords if kw in item["text"].lower())
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored]


# ---- Main Pipeline ----
if __name__ == "__main__":
    # 1. Source document
    document = (
        "The claims processing policy sets a threshold of $5000 for automatic approvals. "
        "Claims exceeding this limit must be reviewed by a senior adjuster. "
        "Underwriting guidelines require risk scores above 70 to be escalated. "
        "All policy documents are subject to annual compliance reviews."
    )

    # 2. Chunk document
    chunks = chunk_document(document, chunk_size=80, overlap=15)
    print(f"[Chunking] Generated {len(chunks)} chunks.\n")

    # 3. Build vector store
    store = SimpleVectorStore()
    for i, chunk in enumerate(chunks):
        emb = generate_embedding(chunk)
        store.upsert(
            chunk_id=f"chunk_{i}",
            text=chunk,
            embedding=emb,
            metadata={"source": "policy_v4.pdf", "dept": "claims", "chunk_index": i}
        )
    print(f"[Indexing] Stored {len(store.store)} vectors.\n")

    # 4. Query
    user_query = "What is the claims threshold for automatic approval?"
    query_emb = generate_embedding(user_query)
    top_results = store.search(query_emb, top_k=3, filter_dept="claims")
    print(f"[Retrieval] Retrieved {len(top_results)} chunks.")

    # 5. Rerank
    reranked = rerank(top_results, user_query)
    print("[Reranking] Reranked results by keyword relevance.\n")

    # 6. Show context to inject into LLM
    print("=== Context for LLM Prompt ===")
    for i, item in enumerate(reranked[:2], 1):
        print(f"[{i}] {item['text'].strip()}")
        print(f"     Source: {item['metadata']['source']} | Dept: {item['metadata']['dept']}")

    sys.exit(0)
```

Run the pipeline:
```bash
python3 /tmp/retrieval_pipeline.py
```

Expected output:
```
[Chunking] Generated 5 chunks.
[Indexing] Stored 5 vectors.
[Retrieval] Retrieved 3 chunks.
[Reranking] Reranked results by keyword relevance.

=== Context for LLM Prompt ===
[1] The claims processing policy sets a threshold of $5000 for automatic approvals.
     Source: policy_v4.pdf | Dept: claims
[2] Claims exceeding this limit must be reviewed by a senior adjuster.
     Source: policy_v4.pdf | Dept: claims
```

### Project: Enterprise Retrieval Engine
Build a FastAPI retrieval service that accepts a user query, fetches context from a vector database, reranks results using Cohere, and returns formatted context blocks ready for LLM injection.

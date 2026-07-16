# Module 6: Hybrid Search - Keywords (BM25) & Vector Integration

## 1. Theory (50%)

### Search Models
Hybrid Search combines keyword-based search with vector-based semantic search to improve search results.

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

### Retrieval Types
*   **Sparse Retrieval (BM25)**: Matches exact keywords (e.g., product codes or names) using term frequency-inverse document frequency formulas.
*   **Dense Retrieval (Embeddings)**: Matches semantic meaning, enabling search without exact keyword matches.
*   **Reciprocal Rank Fusion (RRF)**: Normalizes and combines the rankings from both sparse and dense searches to create a single result set.

### Enterprise Topics
*   **Reranking**: Using a secondary transformer model (like Cohere Rerank) to evaluate and re-order the combined search results for optimal relevance.
*   **Recall Optimization**: Balancing query expansion and filtering to ensure the search captures all relevant documents.

---

## 2. Practical (50%)

### Ingress & Query Script
Write a Python script to simulate sparse search, dense search, RRF scoring, and reranking:
```python
# /tmp/hybrid_search_demo.py
import sys

def mock_bm25_search(query: str) -> list:
    # Sparse keyword matching
    return ["doc_1", "doc_3"]

def mock_dense_search(query: str) -> list:
    # Dense vector matching
    return ["doc_2", "doc_1"]

def reciprocal_rank_fusion(sparse_ranks: list, dense_ranks: list) -> list:
    print("Combining results using RRF...")
    scores = {}
    
    # Calculate RRF scores: 1 / (60 + rank)
    for rank, doc in enumerate(sparse_ranks, start=1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (60.0 + rank))
    for rank, doc in enumerate(dense_ranks, start=1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (60.0 + rank))
        
    # Sort by score descending
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in sorted_docs]

if __name__ == '__main__':
    query = "claims policy limits"
    
    # 1. Run sparse and dense searches
    sparse = mock_bm25_search(query)
    dense = mock_dense_search(query)
    
    print(f"Sparse results: {sparse}")
    print(f"Dense results: {dense}")
    
    # 2. Combine results using RRF
    combined = reciprocal_rank_fusion(sparse, dense)
    print(f"Combined RRF Rankings: {combined}")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/hybrid_search_demo.py
```

### Project: Enterprise Knowledge Search Engine
Build a hybrid search engine that queries Weaviate for semantic matches and Elasticsearch for exact keyword matches, combining rankings using RRF.

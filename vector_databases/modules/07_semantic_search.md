# Module 7: Semantic Search - Context Matching & Query Expansion

## 1. Theory (50%)

### Fundamentals
Semantic Search uses vector embeddings to understand the context and intent behind user queries, enabling search without exact keyword matches.

```
+-------------------------------------------------------------------------------------------------+
|                                    Semantic Search Pipeline                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       User Query                                        |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Generate Embedding)                                |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  Embedding Model                                        |   |
|   |   - Vectorizes query to capture semantic meaning                                        |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Search Index)                                      |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                   Vector Database                                       |   |
|   |   - Runs similarity search to retrieve closest context documents                        |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Search Pipeline
1.  **Vectorization**: The query is converted into a vector embedding.
2.  **Similarity Search**: The vector database searches for the closest matches using metrics like Cosine Similarity or L2 distance.
3.  **Ranking**: The matches are returned, ranked by similarity scores.

### Enterprise Topics
*   **Query Expansion**: Rewriting the query (using an LLM) to include synonyms and additional context, improving search accuracy.
*   **Search Quality Evaluation**: Tracking search quality using metrics like Mean Reciprocal Rank (MRR) and Normalized Discounted Cumulative Gain (NDCG).

---

## 2. Practical (50%)

### Ingress & Query Script
Write a Python script to simulate vector generation, similarity scoring, and query expansion:
```python
# /tmp/semantic_search_demo.py
import sys
import numpy as np

def cosine_similarity(v1: list, v2: list) -> float:
    # Cosine formula: (v1 dot v2) / (||v1|| * ||v2||)
    a = np.array(v1)
    b = np.array(v2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

if __name__ == '__main__':
    # 1. Define query and document vectors
    query_vector = [0.1, 0.2, 0.3]
    doc_1_vector = [0.11, 0.21, 0.31] # high semantic similarity
    doc_2_vector = [0.9, 0.1, 0.05]   # low semantic similarity
    
    # 2. Measure cosine similarity
    sim_1 = cosine_similarity(query_vector, doc_1_vector)
    sim_2 = cosine_similarity(query_vector, doc_2_vector)
    
    print(f"Similarity with Document 1: {sim_1:.4f}")
    print(f"Similarity with Document 2: {sim_2:.4f}")
    
    if sim_1 > 0.95:
        print("Document 1 is semantically relevant.")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/semantic_search_demo.py
```

### Project: Enterprise Semantic Search Platform
Build a semantic search engine using an embedding API and a vector database to retrieve context documents for user queries.

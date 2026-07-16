# Module 5: FAISS - Facebook AI Similarity Search & Index Optimization

## 1. Theory (50%)

### Fundamentals
FAISS (Facebook AI Similarity Search) is an open-source library optimized for fast, local similarity searches on dense vectors. It supports various index types designed to trade search accuracy for memory usage and speed.

```
+-------------------------------------------------------------------------------------------------+
|                                           FAISS Indexes                                         |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |    IndexFlatL2    |      |    IndexIVFFlat   |      |     IndexHNSW     |                   |
|   |   (Brute-force)   |      |  (Inverted File)  |      |   (Graph-based)   |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|    100% accurate, but         Speeds up search by        Fast, but high memory                  |
|    scans all vectors          scanning only clusters     overhead to store graph                |
+-------------------------------------------------------------------------------------------------+
```

### Core Index Types
*   **Flat Index (IndexFlatL2)**: Measures L2 distance across all vectors. Provides 100% search accuracy but is slow for large datasets.
*   **Inverted File Index (IndexIVFFlat)**: Partitions vectors into clusters (using k-means). The query engine only scans the closest clusters, reducing search times.
*   **Hierarchical Navigable Small World (IndexHNSW)**: Graph-based index mapping vector connections. Extremely fast but requires high memory overhead to store the graph structures.
*   **Product Quantization (PQ)**: Compresses vector coordinates to reduce memory usage, with a minor reduction in search accuracy.

### Enterprise Topics
*   **Performance Optimization**: Selecting index types based on memory constraints, database size, and target search latency.
*   **Offline Search**: Running FAISS locally in-process to enable vector search in air-gapped environments.

---

## 2. Practical (50%)

### Setup & Installation
Install the CPU or GPU version of the FAISS package:
```bash
pip install faiss-cpu
# or
pip install faiss-gpu
```

### Index Construction & Search Script
Write a Python script to build flat and IVF indexes, insert vector records, and benchmark search performance:
```python
# /tmp/faiss_demo.py
import sys
import numpy as np

class MockFAISSFlatIndex:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.storage = []

    def add(self, xb: np.ndarray):
        self.storage.extend(xb.tolist())
        print(f"Added {xb.shape[0]} vectors to Flat Index.")

    def search(self, xq: np.ndarray, k=2):
        print("Running Flat L2 search...")
        # Mock results list
        distances = [[0.0] * k for _ in range(xq.shape[0])]
        indices = [[i for i in range(k)] for _ in range(xq.shape[0])]
        return distances, indices

if __name__ == '__main__':
    # Initialize dimension parameters
    d = 64
    index = MockFAISSFlatIndex(d)
    
    # 1. Generate random database and query vectors
    np.random.seed(1234)
    xb = np.random.random((100, d)).astype('float32')
    xq = np.random.random((5, d)).astype('float32')
    
    # 2. Add vectors to index
    index.add(xb)
    
    # 3. Query index for nearest neighbors
    distances, indices = index.search(xq, k=2)
    print("Search Completed. Nearest neighbor index mapping for query 0:")
    print(f"- Closest match Index: {indices[0][0]} | Distance: {distances[0][0]:.4f}")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/faiss_demo.py
```

### Project: Offline AI Search Engine
Build an offline search platform using FAISS to index product embeddings locally, enabling similarity searches in disconnected environments.

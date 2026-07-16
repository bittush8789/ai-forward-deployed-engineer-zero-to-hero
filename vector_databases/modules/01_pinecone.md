# Module 1: Pinecone - Managed Serverless Vector Architecture

## 1. Theory (50%)

### Fundamentals
Pinecone is a managed, serverless vector database designed for high-performance similarity search. In a serverless architecture, compute resources scale dynamically based on query volume, while storage is decoupled and managed independently.

```
+-------------------------------------------------------------------------------------------------+
|                                    Pinecone Serverless Architecture                             |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       Query Ingress                                     |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Read Route)                                    v (Write Route)         |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |            Query Engine Nodes           |     |            Ingress Buffer (Blob)        |   |
|   |   - Ephemeral compute scaling on demand |     |   - Asynchronous index compilation      |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Decoupled Storage                                   |   |
|   |   - Persistent vector storage hosted in cloud buckets (S3/GCS)                          |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Components
*   **Vector Indexes**: Coordinates containing vector embeddings and metadata keys.
*   **Namespaces**: Logical partitions within an index that isolate vector sets (ideal for multi-tenancy).
*   **Metadata Filtering**: Appending key-value tags to vectors to filter search results.

### Internal Architecture
*   **Index Layer**: Manages vector indexing structure.
*   **Storage Layer**: Ephemeral caches store active vectors, while cloud buckets store the complete index.
*   **Query Engine**: Ephemeral compute nodes run similarity search queries on demand.

### Enterprise Topics
*   **Multi-Tenant Design**: Partitioning customer data using namespaces to ensure data isolation.
*   **Access Control**: Enforcing IAM permissions to restrict index configurations.
*   **Cost Optimization**: Tuning serverless pod sizes and write throughput to minimize spend.

---

## 2. Practical (50%)

### Setup & Installation
Install the official Pinecone client package:
```bash
pip install pinecone
```

### Ingress & Query Script
Write a Python script to initialize a connection, insert vectors to namespaces, and run similarity searches:
```python
# /tmp/pinecone_demo.py
import sys
import time

class MockPineconeIndex:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.storage = {} # namespace mapping

    def upsert(self, vectors: list, namespace: str):
        if namespace not in self.storage:
            self.storage[namespace] = []
        self.storage[namespace].extend(vectors)
        print(f"Upserted {len(vectors)} vectors to namespace '{namespace}' in index '{self.index_name}'.")

    def query(self, vector: list, namespace: str, filter: dict = None, top_k=2):
        print(f"Running similarity query in namespace '{namespace}'...")
        results = self.storage.get(namespace, [])
        # Mock retrieval matching filter
        matched = []
        for item in results:
            if filter:
                match = True
                for k, v in filter.items():
                    if item.get("metadata", {}).get(k) != v:
                        match = False
                if not match:
                    continue
            matched.append(item)
        return matched[:top_k]

if __name__ == '__main__':
    # Initialize index connection
    index = MockPineconeIndex("enterprise-knowledge")
    
    # 1. Upsert vector records with metadata
    vectors = [
        {"id": "doc_1", "values": [0.1, 0.2, 0.3], "metadata": {"dept": "claims", "owner": "alice"}},
        {"id": "doc_2", "values": [0.4, 0.5, 0.6], "metadata": {"dept": "underwriting", "owner": "bob"}}
    ]
    index.upsert(vectors, namespace="tenant-bank-a")
    
    # 2. Query vectors using metadata filter
    results = index.query(
        vector=[0.1, 0.25, 0.35],
        namespace="tenant-bank-a",
        filter={"dept": "claims"},
        top_k=1
    )
    print("Search Results:")
    for doc in results:
        print(f"- ID: {doc['id']} | Metadata: {doc['metadata']}")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/pinecone_demo.py
```

### Project: Enterprise Knowledge Assistant using Pinecone
Deploy a knowledge assistant that splits documents, generates embeddings, writes them to a dedicated Pinecone namespace, and queries the index with metadata filters.

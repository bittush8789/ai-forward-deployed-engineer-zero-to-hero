# Module 4: Milvus - Distributed High-Scale Vector Architecture

## 1. Theory (50%)

### Fundamentals
Milvus is a highly scalable, distributed vector database designed to support similarity search on a billion-scale. In a distributed deployment, Milvus decouples compute and storage, partitioning tasks across specialized worker nodes.

```
+-------------------------------------------------------------------------------------------------+
|                                    Milvus Distributed Engine                                    |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Coordinator Layer                                   |   |
|   |   - Manages task allocations and coordinates worker node activities                     |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |               Query Node                |     |               Data Node                 |   |
|   |   - Ephemeral nodes serving queries     |     |   - Ephemeral nodes managing updates    |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Decoupled Storage                                   |   |
|   |   - Persistent vector storage hosted in cloud buckets (MinIO/S3)                        |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Architecture Components
*   **Query Node**: Ephemeral compute nodes that load vectors into memory and serve search queries.
*   **Data Node**: Nodes that manage write updates and write segments to object storage.
*   **Index Node**: Specialized nodes that compile vector indices (such as IVF or HNSW).
*   **Coordinator Layer**: Manages schema definitions, coordinates worker nodes, and tracks cluster metadata.

### Enterprise Topics
*   **High Availability**: Deploying duplicate Query and Data nodes to prevent single-points-of-failure.
*   **Billion-Scale Search**: Sharding large collections horizontally across multiple Query nodes.

---

## 2. Practical (50%)

### Setup & Local Infrastructure
Start Milvus services using Docker Compose:
```bash
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-standalone-docker-compose.yml -O docker-compose.yml
docker compose up -d
```

### Collection & Index Management Script
Write a Python script to define collection schemas, create indices, and run searches:
```python
# /tmp/milvus_demo.py
import sys

class MockMilvusClient:
    def __init__(self):
        self.collections = {}

    def create_collection(self, collection_name: str, dimension: int):
        self.collections[collection_name] = {
            "dimension": dimension,
            "data": [],
            "index_created": False
        }
        print(f"Collection '{collection_name}' (dim={dimension}) created.")

    def create_index(self, collection_name: str, index_type: str):
        if collection_name in self.collections:
            self.collections[collection_name]["index_created"] = True
            print(f"Index type '{index_type}' created for collection '{collection_name}'.")

    def insert(self, collection_name: str, data: list):
        if collection_name in self.collections:
            self.collections[collection_name]["data"].extend(data)
            print(f"Inserted {len(data)} vectors to collection '{collection_name}'.")

    def search(self, collection_name: str, query_vectors: list, limit=2):
        print(f"Searching collection '{collection_name}' for vectors...")
        col = self.collections.get(collection_name, {})
        # Mock retrieval matching
        results = col.get("data", [])
        return results[:limit]

if __name__ == '__main__':
    client = MockMilvusClient()
    
    # 1. Initialize collection schema
    client.create_collection("customer_embeddings", dimension=128)
    
    # 2. Build vector index parameters
    client.create_index("customer_embeddings", index_type="IVF_FLAT")
    
    # 3. Insert vectors
    client.insert("customer_embeddings", [
        {"id": 1, "vector": [0.1] * 128},
        {"id": 2, "vector": [0.2] * 128}
    ])
    
    # 4. Execute search query
    results = client.search("customer_embeddings", [[0.12] * 128], limit=1)
    print("Search Results:")
    for doc in results:
        print(f"- ID: {doc['id']} | Vector values match: {doc['vector'][:3]}...")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/milvus_demo.py
```

### Project: Large Scale AI Search Platform
Design a Milvus cluster deployment topology to partition and search 10 million vector records, integrating data ingestion pipelines.

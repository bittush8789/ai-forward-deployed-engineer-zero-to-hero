# Module 3: Weaviate - Graph Vector Schema & Hybrid Search

## 1. Theory (50%)

### Fundamentals
Weaviate is an open-source, GraphQL-based vector database that maps data objects as classes within a schema, enabling hybrid and semantic searches.

```
+-------------------------------------------------------------------------------------------------+
|                                        Weaviate Schema                                          |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       Classes & Objects                                 |   |
|   |   - Schema definitions (e.g. Document class with text and metadata properties)           |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |              Vector Engine              |     |              Graph Layer                |   |
|   |   - Indexes embeddings (HNSW)           |     |   - Maps relations between objects      |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                        Search Layer                                     |   |
|   |   - Combines vector similarity with BM25 keyword matching (Hybrid)                      |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Architecture Components
*   **Vector Engine**: High-performance engine that indexes vector representations (usually using HNSW).
*   **Graph Layer**: Maps relationships between objects.
*   **Search Layer**: Orchestrates hybrid searches, combining vector similarity and BM25 keyword matching.

### Enterprise Topics
*   **Multi-Tenancy**: Creating dedicated partitions within classes to isolate tenant data.
*   **Data Governance**: Restricting schema mutations and auditing queries for compliance.

---

## 2. Practical (50%)

### Setup & Local Infrastructure
Start a local Weaviate instance in Docker:
```bash
docker run -d -p 8080:8080 semitechnologies/weaviate:latest
```

### Schema & Hybrid Search Script
Write a Python script to define a class schema, insert objects, and run hybrid searches:
```python
# /tmp/weaviate_demo.py
import sys

class MockWeaviateClient:
    def __init__(self):
        self.classes = {}

    def create_schema(self, class_config: dict):
        class_name = class_config.get("class")
        self.classes[class_name] = []
        print(f"Schema class '{class_name}' created successfully.")

    def insert_object(self, class_name: str, properties: dict, vector: list):
        self.classes[class_name].append({
            "properties": properties,
            "vector": vector
        })
        print(f"Inserted object to class '{class_name}'.")

    def hybrid_search(self, class_name: str, query: str, alpha=0.5):
        print(f"Running hybrid search (alpha={alpha}) for: '{query}'...")
        # Mock retrieval matching text properties
        results = self.classes.get(class_name, [])
        return [res["properties"] for res in results[:2]]

if __name__ == '__main__':
    client = MockWeaviateClient()
    
    # 1. Define schema class config
    client.create_schema({
        "class": "DocumentRecord",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "department", "dataType": ["string"]}
        ]
    })
    
    # 2. Insert data objects
    client.insert_object(
        class_name="DocumentRecord",
        properties={"content": "Policy limit is $5000.", "department": "claims"},
        vector=[0.12, 0.22, 0.32]
    )
    
    # 3. Execute hybrid search query
    results = client.hybrid_search("DocumentRecord", "policy limit", alpha=0.5)
    print("Search Results:")
    for doc in results:
        print(f"- Content: {doc['content']} | Dept: {doc['department']}")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/weaviate_demo.py
```

### Project: Enterprise Search Platform
Design a Weaviate schema to represent commercial document logs, import data with multi-tenant isolation, and run hybrid searches via APIs.

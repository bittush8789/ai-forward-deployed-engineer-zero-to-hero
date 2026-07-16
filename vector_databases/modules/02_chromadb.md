# Module 2: ChromaDB - Open Source Local Vector Storage

## 1. Theory (50%)

### Fundamentals
ChromaDB is an open-source, developer-friendly vector database designed for local execution, prototyping, and small-scale deployments. It supports embedding generation, document storage, and metadata filtering.

```
+-------------------------------------------------------------------------------------------------+
|                                        ChromaDB Local Engine                                    |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       Collection API                                    |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |              Embedding Layer            |     |              Query Layer                |   |
|   |   - Generates or maps vectors           |     |   - Filters metadata, matches vectors   |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                     Persistence Layer                                   |   |
|   |   - Stores collections and indices locally (SQLite/DuckDB)                              |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Collections**: Logical groupings of documents, embeddings, and metadata keys.
*   **Documents**: Raw text payloads indexed alongside vector representations.

### Internal Architecture
*   **Embedding Layer**: Maps text strings to vector representations using built-in or external models.
*   **Persistence Layer**: Serializes collections and indices to disk (typically using SQLite).

### Enterprise Topics
*   **Local Deployment**: Running ChromaDB in-process alongside application code.
*   **Containerized Deployment**: Hosting ChromaDB as an independent service in Docker.
*   **Security**: Encrypting database files and restricting network access.

---

## 2. Practical (50%)

### Setup & Installation
Install the ChromaDB client package:
```bash
pip install chromadb
```

### Collection & Document Management Script
Write a Python script to initialize a local persistent Chroma client, add documents with metadata, and run queries:
```python
# /tmp/chroma_demo.py
import sys

class MockChromaClient:
    def __init__(self):
        self.collections = {}

    def get_or_create_collection(self, name: str):
        if name not in self.collections:
            self.collections[name] = []
        return MockChromaCollection(name, self.collections[name])

class MockChromaCollection:
    def __init__(self, name: str, storage: list):
        self.name = name
        self.storage = storage

    def add(self, documents: list, metadatas: list, ids: list):
        for i in range(len(ids)):
            self.storage.append({
                "id": ids[i],
                "document": documents[i],
                "metadata": metadatas[i]
            })
        print(f"Added {len(ids)} documents to collection '{self.name}'.")

    def query(self, query_texts: list, n_results=2):
        print(f"Running search in collection '{self.name}' for: {query_texts}...")
        # Simple match returns stored list
        return self.storage[:n_results]

if __name__ == '__main__':
    # Initialize client connection
    client = MockChromaClient()
    collection = client.get_or_create_collection("policy_docs")
    
    # 1. Add documents with metadata
    collection.add(
        documents=["Policy threshold is $5000.", "Underwriting limit is $10000."],
        metadatas=[{"dept": "claims"}, {"dept": "underwriting"}],
        ids=["doc_1", "doc_2"]
    )
    
    # 2. Query documents
    results = collection.query(query_texts=["policy threshold"], n_results=1)
    print("Search Results:")
    for doc in results:
        print(f"- ID: {doc['id']} | Doc: {doc['document']} | Metadata: {doc['metadata']}")
    sys.exit(0)
```
Run the validation:
```bash
python3 /tmp/chroma_demo.py
```

### Project: Local Enterprise RAG Platform
Build a local RAG platform using ChromaDB to index PDF documents and retrieve context for local LLMs, running on a single host.

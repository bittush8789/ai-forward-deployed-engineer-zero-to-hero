# Practice Tasks: Modules 4-10

## Module 4 - Milvus Cluster Health Check

### Task 1: Run the Milvus Cluster Check Lab
```bash
python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/milvus_cluster_check.py
```
Verify all 4 node types (root_coord, query_node, data_node, index_node) report HEALTHY status.

### Task 2: Interview Questions
1. Name the 4 Milvus node types and their responsibilities.
2. What is the difference between IVF_FLAT and IVF_PQ indexes?
3. How does Milvus achieve high availability?

---

## Module 5 - FAISS Benchmark

### Task 1: Run the FAISS Benchmark Lab
```bash
python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/faiss_offline_search.py
```
Record the latency difference between Flat and IVF_FLAT.

### Task 2: Interview Questions
1. What is the `nprobe` parameter in IVF index and how does it trade speed for accuracy?
2. When would you choose HNSW over IVF_FLAT?
3. What is Product Quantization and when do you use it?

---

## Module 6 - Hybrid Search

### Task 1: Implement RRF from Scratch
Write a Python function that takes two ranked lists and returns an RRF-merged ranked list.
```python
def rrf(list_a: list, list_b: list, k=60) -> list:
    # Your implementation here
    pass
```
Test with: `rrf(["doc1", "doc3", "doc2"], ["doc2", "doc1", "doc4"])`

### Task 2: Interview Questions
1. Why is Hybrid Search superior to pure vector search for enterprise documents?
2. What does BM25 stand for and what does the "25" refer to?
3. What is Cohere Rerank and where does it fit in the pipeline?

---

## Module 7 - Semantic Search

### Task 1: Implement Cosine Similarity
Write a Python function that calculates cosine similarity between two vectors.
Verify with known vectors: `cosine([1,0,0], [1,0,0])` should return `1.0`.

### Task 2: Interview Questions
1. What is the difference between L2 distance and Cosine similarity metrics?
2. When does semantic search fail and how does hybrid search compensate?
3. What is query expansion and how does it improve recall?

---

## Module 8 - Embedding Models

### Task 1: Run the Embedding Benchmark
```bash
python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/pinecone_rag_mock.py
```
Compare simulated latency for `text-embedding-3-small` vs `all-MiniLM-L6-v2`.

### Task 2: Interview Questions
1. What is MTEB and why is it used to evaluate embedding models?
2. How many dimensions does `text-embedding-3-large` produce?
3. When would you self-host an embedding model vs use an API?

---

## Module 9 - Retrieval Architecture

### Task 1: Run the End-to-End Retrieval Pipeline
```bash
python3 /tmp/retrieval_pipeline.py
```
Verify chunking, indexing, retrieval, and reranking all produce output.

### Task 2: Chunking Experiment
Modify `chunk_size` in the pipeline script from 80 to 40 and observe how many more chunks are created. Document the trade-off.

### Task 3: Interview Questions
1. What chunk size would you use for policy documents? Why?
2. What is the difference between a pre-filter and a post-filter in RAG retrieval?
3. How does Ragas measure retrieval quality?

---

## Module 10 - Production Operations

### Task 1: Run the Backup Strategy Validator
```bash
python3 /tmp/backup_strategy_check.py
```

### Task 2: Capacity Planning Exercise
Calculate total storage for: 5 million vectors at 1536 dimensions with 3x replication.
Use the formula from the module:
```
Storage = (1536 * 4 bytes) * 5M vectors * 3 replication
```

### Task 3: Interview Questions
1. What monitoring metric indicates your vector index needs to be re-indexed?
2. What is the Recovery Time Objective (RTO) for a DR drill?
3. How do you implement RBAC in Pinecone at the retrieval layer?

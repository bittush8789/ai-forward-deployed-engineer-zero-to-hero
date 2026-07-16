# Practice Tasks: Module 1 - Pinecone

## Task 1: Create a Pinecone Index and Run a Namespace Query
**Goal**: Validate namespace isolation and metadata filtering logic.

### Step-by-Step
1. Run the Pinecone RAG mock lab:
   ```bash
   python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/pinecone_rag_mock.py
   ```
2. Verify the output shows:
   - Upsert confirmation with namespace label
   - Query results filtered to `dept=claims` only
   - No underwriting documents in results

### Expected Output
```
[Pinecone] Upserted 4 vectors -> namespace='tenant-bank-a'
[Pinecone] Query complete | namespace='tenant-bank-a' | filter={'dept': 'claims'} | results=2
```

---

## Task 2: Extend the Lab to Add a Second Tenant Namespace
**Goal**: Confirm that queries scoped to `tenant-bank-b` return zero results (no data was upserted there).

### Step-by-Step
1. Open [pinecone_rag_mock.py](../labs/pinecone_rag_mock.py) and add after the first upsert:
   ```python
   # Query a namespace with no data
   empty_results = index.query(
       vector=query_vec,
       namespace="tenant-bank-b",  # different tenant
       top_k=2
   )
   print(f"tenant-bank-b results: {len(empty_results)}")  # Should print 0
   ```
2. Re-run the script and confirm the result count is 0.

---

## Task 3: Interview Scenario Practice
Answer the following without looking at your notes:

1. What is the difference between an Index and a Namespace in Pinecone?
2. How does metadata filtering work — is it a pre-filter or post-filter?
3. When would you use Pod-based Pinecone vs Serverless?

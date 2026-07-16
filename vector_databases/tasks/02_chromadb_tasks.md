# Practice Tasks: Module 2 - ChromaDB

## Task 1: Run the ChromaDB Local RAG Lab
**Goal**: Validate collection creation, document ingestion, and metadata-filtered search.

### Step-by-Step
1. Run the ChromaDB RAG mock lab:
   ```bash
   python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/chroma_local_rag.py
   ```
2. Verify the output shows:
   - Collection created and documents added
   - Query results only contain `dept=claims` documents

---

## Task 2: Add a New Collection and Compare Results
**Goal**: Demonstrate multi-collection design by adding a second `regulatory_docs` collection.

### Step-by-Step
1. In the lab script, after the first collection query, add:
   ```python
   reg_collection = client.get_or_create_collection("regulatory_docs")
   reg_collection.add(
       ids=["reg_1"],
       documents=["GDPR Article 5 requires data minimization."],
       metadatas=[{"dept": "legal", "source": "gdpr_2018.pdf"}]
   )
   reg_results = reg_collection.query(
       query_texts=["What does GDPR say about data minimization?"],
       n_results=1
   )
   print(reg_results["documents"])
   ```
2. Confirm results come from the correct collection.

---

## Task 3: Interview Scenario Practice
Answer the following without looking at your notes:

1. How do you enable persistent storage in ChromaDB?
2. What is the difference between a ChromaDB collection and a Pinecone namespace?
3. How does ChromaDB generate embeddings if you don't provide vectors explicitly?

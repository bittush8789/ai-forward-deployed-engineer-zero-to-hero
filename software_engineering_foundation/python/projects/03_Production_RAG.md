# Capstone Project 3: Production RAG Platform

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 20-25 Hours
**Primary Tech Stack:** LlamaIndex, Pinecone, Cohere (Reranking), Celery

---

## 1. Project Overview

You are deployed to a legal firm that has 50,000 PDF case files. They need a system that can accurately search these files and answer complex legal questions. Standard naive RAG (chunk and embed) is failing because the context is too dense. You must build an Advanced RAG pipeline.

## 2. Architecture Requirements

- **Orchestration**: `LlamaIndex`
- **Vector Database**: `Pinecone` Serverless
- **Embeddings**: `text-embedding-3-large`
- **Reranking**: `Cohere` Rerank API
- **Async Workers**: `Celery` (for document ingestion)

## 3. Core Features to Build

1. **Hierarchical Chunking**: Do not just split by 500 characters. Implement LlamaIndex's SentenceWindowNodeParser to store small chunks for embedding (for high accuracy retrieval) but retrieve the surrounding window of text to feed the LLM.
2. **Metadata Extraction**: Before embedding, use an LLM to extract the `Date`, `Case_Type`, and `Lawyer_Name` from the document. Attach this metadata to the vector in Pinecone.
3. **Hybrid Search Pipeline**:
   - Step 1: User asks a question.
   - Step 2: Use LLM to extract metadata filters (e.g., filter by `Case_Type="Criminal"`).
   - Step 3: Perform Vector Similarity Search in Pinecone with the metadata filter.
   - Step 4: Retrieve top 20 results.
   - Step 5: Pass the 20 results through a **Cohere Reranker** to select the definitive top 5 most relevant chunks.
   - Step 6: Pass top 5 chunks to LLM for final generation.
4. **Async Ingestion**: A FastAPI endpoint `/upload` that saves a file and triggers a Celery task to run the parsing/embedding pipeline in the background so the user doesn't wait.

## 4. Submission Checklist
- [ ] Clean OOP implementation defining a `BaseRetriever` and `AdvancedRAGRetriever`.
- [ ] Integration with Pinecone namespaces.
- [ ] Performance profiling script showing the latency difference between Naive RAG and Advanced RAG.

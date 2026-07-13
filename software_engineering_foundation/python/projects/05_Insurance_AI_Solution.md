# Capstone Project 5: Forward Deployed AI Solution for Insurance

**Difficulty:** ⭐⭐⭐⭐⭐
**Estimated Time:** 40+ Hours (Masterpiece)
**Primary Tech Stack:** Full Stack Python (All Modules Combined)

---

## 1. Project Overview

This is the ultimate test. You are deployed to a global Insurance provider. You must build an end-to-end, production-ready AI platform that automates Insurance Claim Assessments. This combines RAG, Multi-Agent workflows, robust APIs, and strict data engineering.

## 2. Architecture Requirements

- **APIs**: FastAPI
- **DBs**: PostgreSQL (Policy Data), Pinecone (Policy PDFs)
- **Queue**: Celery + Redis
- **AI**: LangGraph + LlamaIndex + OpenAI
- **Deploy**: Docker + Makefiles

## 3. Core Features to Build

### Phase 1: Ingestion & RAG
- Ingest massive "Policy Guideline" PDFs into Pinecone using advanced chunking.
- Expose a FastAPI endpoint `/api/policies/search` that securely searches these vectors.

### Phase 2: The Agentic Claim Pipeline
- An endpoint `/api/claims/submit` receives a JSON payload containing user details, accident description, and an estimated cost.
- A **LangGraph** workflow is triggered:
  - **Node 1 (Fraud Detection)**: AI Agent reviews the claim for logical inconsistencies.
  - **Node 2 (Policy Retrieval)**: RAG Agent searches Pinecone to see if the accident type is covered under the user's specific policy type.
  - **Node 3 (Adjustment)**: Math Agent compares the requested cost against typical market rates.
  - **Node 4 (Decision)**: The Supervisor Agent compiles all data and outputs a strict Pydantic JSON: `{"status": "APPROVED|DENIED|MANUAL_REVIEW", "reasoning": "..."}`.

### Phase 3: Observability & Production
- Every step of the graph must log structured JSON using `structlog` containing a unique `trace_id` for the claim.
- All code must be strictly typed, well-commented, and pass a full Pytest suite.
- The entire platform must be configurable via `.env` files (no hardcoded settings).

## 4. Submission Checklist
- [ ] A completely polished, professional GitHub repository.
- [ ] A `README.md` explaining the architecture, how to run it via `docker-compose up`, and API documentation.
- [ ] Demonstration of the Singleton pattern (DB connection), Factory pattern (LLM instantiation), and Strategy pattern (RAG search type).
- [ ] You are now ready to be an AI Forward Deployed Engineer.

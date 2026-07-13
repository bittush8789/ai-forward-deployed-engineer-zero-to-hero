# Final Integrated Project: Enterprise AI Customer Support Platform

**Difficulty:** ⭐⭐⭐⭐⭐
**Estimated Time:** 40-50 Hours (Masterpiece)
**Primary Tech Stack:** FastAPI, PostgreSQL, Redis, Celery, LangGraph, OpenAI, Pinecone, Docker, GitHub Actions, PyTest.

---

## 1. Project Overview

This is the culmination of the entire Software Engineering Foundation curriculum. You are no longer writing isolated scripts; you are architecting a distributed, production-grade enterprise system. 

You are building the **Enterprise AI Customer Support Platform**. 
It receives support tickets, routes them via a Multi-Agent LangGraph workflow, retrieves context from a Pinecone Vector Database, tracks state in Redis, processes heavy tasks in Celery, stores permanent audit logs in PostgreSQL, and is fully CI/CD integrated via GitHub Actions.

## 2. Architecture Specifications

### The Infrastructure Layer (Docker)
- A `docker-compose.yml` file that orchestrates:
  - `web`: The FastAPI server.
  - `worker`: The Celery worker processing AI tasks.
  - `db`: PostgreSQL database.
  - `cache`: Redis (used as Celery Broker and state store).

### The Database Layer (SQL & ORM)
- `users`: Tracks authenticated clients.
- `tickets`: The core resource. Has a `status` (Open, In_Progress, Resolved, Escalated).
- `audit_logs`: A highly normalized table tracking every action an agent takes on a ticket.

### The API Layer (FastAPI)
- `POST /token`: JWT Authentication.
- `POST /tickets`: Accepts a new support request. Returns `202 Accepted` and a `ticket_id` instantly, offloading the work to Celery.
- `GET /tickets/{id}`: Polls PostgreSQL for the current status and AI response.

### The AI Layer (Data Structures & LangGraph)
- A LangGraph State Machine (DAG) triggered by the Celery worker.
- **Triage Node**: Determines if the ticket is Billing or Technical.
- **RAG Node**: If Technical, searches Pinecone for documentation.
- **Resolution Node**: Generates the final response.
- **QA Node**: Uses a Judge LLM to verify the response. If it fails, routes back to Resolution (Cycle!).

### The DevOps Layer (Git & Testing)
- A `.github/workflows/deploy.yml` pipeline.
- It runs `pytest` and `flake8`.
- If tests pass, it builds the Docker image.

## 3. Step-by-Step Implementation Guide

### Phase 1: Foundation (Git & DB)
1. Initialize the Git repository.
2. Design the PostgreSQL schema using SQLAlchemy models.
3. Generate the initial Alembic migration.

### Phase 2: The API (FastAPI)
1. Build the JWT authentication dependencies.
2. Build the CRUD routes for Tickets.
3. Write PyTest Integration tests using `TestClient` and `pytest-mock` to verify the routes are secured.

### Phase 3: The Asynchronous Engine (Celery)
1. Configure Celery to use Redis.
2. Modify `POST /tickets` to call `process_ticket.delay(ticket_id)`.
3. Verify the background worker successfully picks up the job.

### Phase 4: The Brain (LangGraph)
1. Build the LangGraph workflow using pure Python Data Structures (Graphs/Nodes).
2. Integrate Pinecone vector search into the Technical Node.
3. Connect the Celery task to the entry point of the LangGraph workflow.
4. Ensure the graph writes the final output back to PostgreSQL.

### Phase 5: Production Readiness
1. Write Dockerfiles for the API and Worker.
2. Write the `docker-compose.yml`.
3. Push to GitHub and ensure GitHub Actions successfully runs your test suite.

## 4. Submission & Evaluation

To pass this final capstone and prove you are a capable AI Forward Deployed Engineer, you must demonstrate:
- [ ] **Data Integrity**: The database schema is in 3NF and handles concurrent updates safely.
- [ ] **Performance**: The API never blocks on LLM network I/O. Time-to-First-Byte for the `POST /tickets` endpoint must be < 100ms.
- [ ] **Security**: No hardcoded API keys. All endpoints require valid JWTs.
- [ ] **Reliability**: PyTest coverage > 85%. Infinite agent loops are mathematically prevented.
- [ ] **Deployability**: A senior engineer should be able to run `docker-compose up` and have the entire distributed system working flawlessly on their local machine within 3 minutes.

***Good luck.***

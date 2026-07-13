# FastAPI Capstone Project: Enterprise AI Gateway

**Difficulty:** ⭐⭐⭐⭐⭐
**Estimated Time:** 12-15 Hours
**Primary Tech Stack:** FastAPI, SQLAlchemy, PostgreSQL, PyJWT, Uvicorn

---

## 1. Project Overview

You are deployed to a major corporation that has 50 internal applications wanting to use OpenAI. Instead of giving 50 teams the raw OpenAI API Key, you have been tasked with building an **AI Gateway**. 

This FastAPI service will sit between the internal apps and OpenAI. It will authenticate users, rate-limit them, log all prompts to a PostgreSQL database for auditing, and proxy the request to OpenAI (streaming the response back).

## 2. Architecture Requirements

- **Auth**: JWT-based Authentication via Dependency Injection.
- **Database**: PostgreSQL (via SQLAlchemy ORM & Alembic).
- **Core Route**: `/v1/chat/completions` (Designed to perfectly match the OpenAI spec so clients can use the standard OpenAI Python SDK, just pointing the `base_url` to your FastAPI server).
- **Middleware**: A custom middleware that calculates the time taken for the LLM to respond and adds it to the HTTP headers.

## 3. Core Features to Build

1. **Authentication Endpoints**:
   - `POST /register`: Creates a user and API Key in the database.
   - `POST /token`: Returns a JWT token.
2. **The Proxy Endpoint** (`POST /v1/chat/completions`):
   - Secure it with JWT.
   - Read the incoming JSON (messages, model).
   - Use the `AsyncOpenAI` client to forward the request to the real OpenAI API.
   - Wait for the response.
   - Save the `user_id`, `prompt`, `response`, and `tokens_used` to a PostgreSQL table `audit_logs` using a BackgroundTask (so it doesn't slow down the response).
   - Return the response to the user.
3. **Analytics Endpoint**:
   - `GET /admin/usage`: Requires a JWT token with `role='admin'`.
   - Returns a grouped sum of tokens used by each user (requires SQLAlchemy `func.sum`).

## 4. Tasks to Complete

1. **Setup**: Initialize a Poetry project, set up FastAPI, and configure SQLAlchemy connecting to a local Postgres or SQLite instance.
2. **Schemas & Models**: Define the Pydantic schemas (Incoming/Outgoing data) and SQLAlchemy models (DB Tables).
3. **Dependencies**: Write `get_db()`, `get_current_user()`, and `require_admin()`.
4. **Implementation**: Write the routing logic.
5. **Testing**: Write a quick script that uses the `openai` python package, but sets `client = OpenAI(base_url="http://localhost:8000/v1", api_key="your_jwt")` to test your gateway.

## 5. Submission Checklist
- [ ] Code is separated into logical files (`main.py`, `models.py`, `schemas.py`, `database.py`, `routers/`).
- [ ] Alembic is initialized and a migration exists to create the tables.
- [ ] The proxy endpoint successfully passes data to OpenAI and logs the result to the DB asynchronously.
- [ ] Admin endpoint strictly blocks non-admin users with a 403 status code.

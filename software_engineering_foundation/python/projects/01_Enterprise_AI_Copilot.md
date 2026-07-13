# Capstone Project 1: Enterprise AI Copilot Platform

**Difficulty:** ⭐⭐⭐
**Estimated Time:** 15-20 Hours
**Primary Tech Stack:** FastAPI, LangChain, PostgreSQL, Redis, React (Mock UI)

---

## 1. Project Overview

You have been deployed to "Acme Corp," a Fortune 500 manufacturing company. They want a centralized "AI Copilot" that all employees can use securely. The copilot must act as an assistant, remembering user contexts, querying internal databases for employee information, and ensuring that no sensitive PII leaks into the OpenAI logs.

## 2. Architecture Requirements

- **Backend Framework**: `FastAPI`
- **Database**: `PostgreSQL` (via `SQLAlchemy` ORM) to store Users, Sessions, and Chat History.
- **Cache**: `Redis` for caching user context and API rate limiting.
- **AI Orchestration**: `LangChain` to build the conversational retrieval chain.
- **Security**: Implement a custom PII scrubbing middleware using functional programming before sending prompts to the LLM.

## 3. Core Features to Build

1. **Authentication Layer**: A JWT-based login system where users are assigned roles (`employee`, `manager`, `admin`).
2. **Session Management**: Each chat window has a unique `session_id`. The backend must fetch the last 10 messages from Postgres to inject into the LLM context window.
3. **Tool Integration**: 
   - A tool that queries a mock SQL database to retrieve employee PTO balances.
   - A tool that fetches the live company stock price.
4. **Streaming Responses**: Use FastAPI's `StreamingResponse` and Async generators to stream tokens to the frontend just like ChatGPT.
5. **Telemetry**: Use `structlog` to output JSON logs containing `user_id`, `tokens_used`, and `latency` for every LLM interaction.

## 4. Submission Checklist
- [ ] Dockerfile that containerizes the FastAPI app.
- [ ] `docker-compose.yml` that spins up FastAPI, PostgreSQL, and Redis simultaneously.
- [ ] Pytest suite covering at least 80% of the API endpoints, with mocked LLM calls.
- [ ] A clean `pyproject.toml` managed by Poetry.

# Capstone Project 4: AI Workflow Automation Platform

**Difficulty:** ⭐⭐⭐⭐⭐
**Estimated Time:** 30-40 Hours
**Primary Tech Stack:** FastAPI, Kafka/RabbitMQ, PostgreSQL, Asyncio

---

## 1. Project Overview

You are deployed to a logistics company. They receive 10,000 emails a day with shipping manifests, complaints, and invoices attached as images or PDFs. They need an asynchronous automation platform (like a custom Zapier) that listens for incoming emails, uses AI to extract structured data, updates their SQL database, and sends confirmation Slack messages.

## 2. Architecture Requirements

- **Framework**: `FastAPI` (Fully `async def`)
- **Message Broker**: `RabbitMQ` or `Kafka`
- **Database**: `PostgreSQL` (using `asyncpg` and SQLAlchemy 2.0 Async)
- **AI Models**: OpenAI GPT-4o (for vision/parsing)

## 3. Core Features to Build

1. **Event-Driven Architecture**: The system must not use direct synchronous API calls between services. When an email is received, emit an `EmailReceivedEvent` to the Kafka/RabbitMQ topic.
2. **The Worker Service**: A separate Python process listening to the queue. When it gets a message, it:
   - Downloads the attachment.
   - Sends it to GPT-4o for OCR and structured JSON extraction.
3. **Strict Validation**: The output from the LLM MUST be strictly validated using `Pydantic`. If it fails validation, emit an `ExtractionFailedEvent`.
4. **Database Operations**: Insert the valid JSON payload into a highly normalized PostgreSQL database using Async SQLAlchemy.
5. **Resilience**: Implement the `Circuit Breaker` and `Retry` patterns. If OpenAI API goes down, the worker should automatically pause processing and requeue the messages without losing data.

## 4. Submission Checklist
- [ ] A Docker Compose file orchestrating 4 containers: FastAPI, RabbitMQ, Worker Node, Postgres.
- [ ] Implementation of `Dependency Injection` for the message broker client.
- [ ] Strict type hinting (`mypy --strict`) passing perfectly across the entire codebase.

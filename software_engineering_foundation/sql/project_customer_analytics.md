# SQL Capstone Project: AI Copilot Analytics Platform

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 8-10 Hours
**Primary Tech Stack:** PostgreSQL, SQL, Python (Mock Data Generation)

---

## 1. Project Overview

You are deployed to a major e-commerce company that recently launched an AI Customer Support Copilot. The executive team wants to know if the AI is actually saving money. You must design the entire relational database schema from scratch, generate mock data, and write complex analytical queries to extract ROI metrics.

## 2. Requirements

1. **Schema Design**: Design a normalized database schema in PostgreSQL.
2. **Mock Data Generation**: Write a Python script using the `Faker` library and `psycopg2` (or SQLAlchemy) to generate 10,000 realistic records.
3. **Analytics Queries**: Write 5 complex SQL queries solving specific business questions.

## 3. Database Schema Specifications

Design tables for the following entities (you determine the exact columns and data types):
- `users`: Customers of the e-commerce platform.
- `agents`: The different AI models or agent personas (e.g., Triage, Returns, Technical).
- `chat_sessions`: A single conversation instance.
- `messages`: Individual messages within a session (Role: User/Assistant).
- `token_logs`: Tracking exactly how many prompt/completion tokens were used per message and the cost.
- `human_handoffs`: Records of when an AI failed and routed the chat to a human agent.

## 4. Analytical Queries to Write

Provide the raw SQL for the following reports:

1. **The Cost Report**: Total AI API cost aggregated by `agent` persona for the current month.
2. **The Handoff Rate**: What percentage of `chat_sessions` required a human handoff, grouped by the `agent` persona? (Requires `LEFT JOIN` and conditional aggregation).
3. **The Token Hog**: Identify the top 5 `users` who have consumed the most tokens across all their sessions.
4. **The Longest Conversations**: Use a Window Function or Aggregation to find the average number of `messages` per `chat_session`.
5. **The AI Success Metric**: (Advanced) Find the sessions that ended without a human handoff AND where the final message was from the AI (indicating resolution).

## 5. Submission Checklist
- [ ] An Entity-Relationship (ER) diagram image or mermaid markdown of your schema.
- [ ] A `schema.sql` file containing all `CREATE TABLE` statements with proper Primary and Foreign keys.
- [ ] A `generate_data.py` script that cleanly populates the database.
- [ ] An `analytics.sql` file containing the 5 required queries, heavily commented explaining the logic.

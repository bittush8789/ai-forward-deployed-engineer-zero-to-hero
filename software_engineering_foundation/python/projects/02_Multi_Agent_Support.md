# Capstone Project 2: Multi-Agent Customer Support System

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 25-30 Hours
**Primary Tech Stack:** LangGraph, FastAPI, OpenAI API, SQLite

---

## 1. Project Overview

You are deployed to a rapidly growing SaaS company whose support team is overwhelmed. You need to build a fully autonomous Multi-Agent system that can read incoming support tickets, route them to specialized AI agents, attempt to resolve them, and only escalate to humans when absolutely necessary.

## 2. Architecture Requirements

- **Framework**: `LangGraph` (for stateful multi-agent workflows)
- **Backend**: `FastAPI` (to receive webhook payloads representing tickets)
- **Database**: `SQLite` (to track ticket status and agent actions)
- **LLM**: `OpenAI gpt-4-turbo` for complex reasoning.

## 3. Core Features to Build

1. **The State Object**: Define a TypedDict holding `ticket_id`, `user_query`, `current_agent`, `resolution_steps`, and `status`.
2. **The Triage Agent (Router)**: Reads the ticket and decides if it goes to:
   - `Billing Agent`
   - `Technical Support Agent`
   - `Account Management Agent`
3. **Specialized Agents**:
   - **Billing**: Has access to a tool (mock API) to issue refunds or check invoice status.
   - **Technical**: Has access to a tool to search a mock documentation Vector Store.
4. **The QA Agent (The Supervisor)**: After a specialized agent drafts a response, it goes to the QA Agent. If the response is poor, it is routed *back* to the specialized agent for a rewrite. If good, it is finalized.
5. **Human Escalation Edge**: If any agent fails 3 times, or explicitly detects high frustration, route the state to the `Escalation Node` which alerts a human and stops the AI loop.

## 4. Submission Checklist
- [ ] A visual representation (mermaid chart) of your LangGraph workflow.
- [ ] Functional python script utilizing `StateGraph`.
- [ ] Implement the `Design Pattern: Factory` to instantiate the correct AI tools based on the active agent.
- [ ] E2E tests simulating 5 different types of tickets ensuring they hit the correct final states.

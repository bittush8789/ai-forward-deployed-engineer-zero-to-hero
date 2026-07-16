# Module 12: LLMOps Interview Preparation & Platform Questions

This module compiles deep technical interview questions and model answers across LLMOps subsystems.

---

## 1. Prompt Management & Versioning

### Q1: Why is it bad practice to store prompt templates directly in application code?
*   **Answer**: Storing templates in code requires a full deployment cycle (building, testing, and releasing code) to modify prompt wording. Decoupling prompts using a Prompt Registry allows prompt engineers to update and deploy prompt modifications dynamically without affecting code.

### Q2: Explain a rollback strategy for prompt templates.
*   **Answer**: Assign environment tags (like `production` or `staging`) to prompt versions in the registry. If a new version fails, update the tag to point to the previous stable version, reverting the change in sub-seconds without redeploying code.

---

## 2. LLM & RAG Evaluation

### Q1: What is the RAG Triad, and why is it critical for RAG evaluation?
*   **Answer**: The RAG Triad consists of three metrics: context relevance, faithfulness, and answer relevance. It is critical because it isolates pipeline bottlenecks, identifying whether poor responses are caused by poor retrieval (context relevance) or poor generation (faithfulness/answer relevance).

### Q2: Explain the "LLM-as-a-judge" evaluation pattern.
*   **Answer**: The "LLM-as-a-judge" pattern uses a larger, high-performance model (such as GPT-4) to evaluate the outputs of other models. The judge compares the output to the ground truth and context based on specific guidelines (like toxicity or faithfulness), returning a numerical score.

---

## 3. Safety Guardrails & Policy Enforcement

### Q1: What is a guardrail, and why is it critical in production LLM platforms?
*   **Answer**: A guardrail is a middleware security layer that validates user inputs and model outputs against safety policies (such as toxicity, PII, or prompt injection), preventing harmful content or jailbreak attacks from reaching the model or user.

### Q2: How do you validate structured JSON outputs from LLMs?
*   **Answer**: Use schema validation libraries (like Pydantic or Instructor) to parse and validate outputs against a predefined schema, running validation checks and executing retries if the schema is violated.

---

## 4. Hallucination Detection

### Q1: What is a hallucination, and how do you detect it?
*   **Answer**: A hallucination is when a model generates factually incorrect or ungrounded outputs. It is detected by extracting claims from the output and cross-referencing them against the retrieved context or a verified database.

---

## 5. Observability & Tracing

### Q1: Explain the difference between a Trace and a Span.
*   **Answer**:
    *   **Trace**: The entire execution path of a single request (e.g., user search transaction).
    *   **Span**: A single step within the trace (e.g., database query or model call).

---

## 6. Cost Optimization & Semantic Caching

### Q1: What is semantic caching, and how does it save costs?
*   **Answer**: Semantic caching stores past queries and responses in a vector database. When a new query is received, the cache compares it to stored queries using similarity metrics. If a match is found, it returns the cached response, saving token costs and reducing response latency.

### Q2: How does model routing optimize costs?
*   **Answer**: Model routing directs queries to the most cost-effective model that can answer them (e.g., routing simple classification queries to smaller models and reserving larger models for complex reasoning tasks).

---

## 7. Enterprise LLMOps Architecture & Governance

### Q1: Explain the unified LLMOps platform architecture blueprint.
*   **Answer**: Prompts are managed in a registry, user queries route through a model gateway, pass through input guardrails to block injections, call the model, pass through output guardrails to scrub PII, and telemetry data is logged to an observability service.

### Q2: Explain the "Right to Explanation" under GDPR.
*   **Answer**: The GDPR "Right to Explanation" grants users the right to receive an explanation for decisions made by automated systems (such as models), requiring models to be explainable.

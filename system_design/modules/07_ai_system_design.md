# Module 7: AI System Design, RAG Topologies & Multi-Agent Orchestrations

## 1. Theory (60%)

### AI Platform Components
An enterprise AI platform integrates specialized layers to manage model lifecycles and serve predictions:
*   **Data Layer**: Data lakes and feature stores (like Feast) that manage raw and preprocessed features.
*   **Training Layer**: Orchestrators (like Kubeflow) and metadata stores (like MLflow) that run and track training jobs.
*   **Serving Layer**: Model gateways and engines (like vLLM, Triton, or KServe) that serve predictions with low latency.
*   **Monitoring Layer**: Prometheus and Grafana dashboards that track model performance and data drift.
*   **Governance Layer**: Model registries and evaluation pipelines that manage versions and run compliance audits.

```
+-------------------------------------------------------------------------------------------------+
|                                     Enterprise AI Platform                                      |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Serving Layer                                       |   |
|   |   - Model gateways and engines (vLLM/Triton) serving predictions                        |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Telemetry Data)                                v (Telemetry Data)      |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |               Monitoring Layer          |     |               Governance Layer          |     |
|   |   - Tracks data drift (Prometheus)      |     |   - Audits model versions (MLflow)      |     |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### AI Patterns

#### Retrieval-Augmented Generation (RAG)
RAG systems retrieve relevant context from vector stores to ground model responses, reducing hallucinations:
1.  **Ingestion**: Documents are split into chunks, processed by embedding models, and stored in vector databases (e.g., Pinecone, Qdrant).
2.  **Retrieval**: User queries are vectorized to search for semantically similar context in the vector database.
3.  **Generation**: The context is merged with the user prompt, guiding the model to generate accurate responses.

#### AI Agents
Agents are autonomous entities that use models to plan and execute tasks using tools:
*   **Planner**: Instructs the model to break tasks into steps.
*   **Memory**: Maintains context across interactions.
*   **Tools**: Integrates external APIs (e.g., database queries or search) to retrieve information or execute actions.

---

## 2. Practical (40%)

### Design System 1: Enterprise RAG Platform Design
We will design a RAG system to support **1 Million Documents** and **1,000 Users** with RBAC and audit logging:

```
+-------------------------------------------------------------------------------------------------+
|                                      RAG Platform Topology                                      |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                   API Gateway & RBAC                                    |   |
|   |   - Enforces role-based access policies before routing queries                          |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Route Query)                                       |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  RAG Microservice                                       |   |
|   |   +---------------------------------------------------------------------------------+   |   |
|   |   | 1. Query Embeddings ---> 2. Vector DB (Search) ---> 3. Context Integration      |   |   |
|   |   +---------------------------------------------------------------------------------+   |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Log Transaction)                                   |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                              Audit Logs (PostgreSQL)                                    |   |
|   |   - Logs query, retrieved documents, and user roles to maintain audit compliance        |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

#### Core Components
*   **API Gateway**: Enforces role-based access controls (RBAC) to ensure users only access authorized documents.
*   **Vector Database (Qdrant)**: Stores and searches document embeddings.
*   **Audit Logger**: Logs user queries, retrieved document IDs, and access roles to maintain compliance.

### Design System 2: Multi-Agent Platform Design
We will design a multi-agent system managing task routing and execution:
*   **Agent Router**: Evaluates user queries and routes them to specialized agents (e.g., Sales or TechSupport).
*   **Agent Instances**: Stateful workers that execute tasks using tools (e.g., database search or email API).
*   **Shared Memory (Redis)**: Stores conversation state and task history across agents.

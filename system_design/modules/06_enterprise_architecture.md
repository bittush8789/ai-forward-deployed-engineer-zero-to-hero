# Module 6: Enterprise Architecture, Domain-Driven Design & Compliance

## 1. Theory (60%)

### Enterprise Architecture Layers
Large enterprise systems partition applications, data, and business processes into distinct architecture layers:
*   **Business Layer**: Maps business processes, user roles, and compliance workflows.
*   **Application Layer**: Contains microservices, API routers, and business logic runtimes.
*   **Data Layer**: Manages databases, vector stores, data lakes, and transactional storage.
*   **Infrastructure Layer**: Physical or cloud infrastructure (VMs, Kubernetes clusters, networking VPCs).

```
+-------------------------------------------------------------------------------------------------+
|                                 Enterprise Architecture Layers                                  |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Business Layer                                      |   |
|   |   - Enforces business processes, user roles, and compliance workflows                   |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                    Application Layer                                    |   |
|   |   - Microservices, API gateways, and core business logic runtimes                       |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       Data Layer                                        |   |
|   |   - Databases, data lakes, caches, and transactional storage layers                     |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                    Infrastructure Layer                                 |   |
|   |   - Cloud hosting services (VPCs, container node pools, load balancers)                 |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Design Patterns
*   **Layered Architecture**: Partitioning code into presentation, business, and data access layers.
*   **Microservices**: Decoupling the application into small, independent services mapped to business domains.
*   **Domain-Driven Design (DDD)**: Modeling software based on the business domain using concepts like bounded contexts and aggregate roots.
*   **Hexagonal Architecture (Ports & Adapters)**: Decoupling core business logic from external frameworks, databases, and APIs using interfaces.

### Governance & Compliance
*   Enforce security policies, audit logging, and data privacy rules (like GDPR or HIPAA) to protect sensitive data.

---

## 2. Practical (40%)

### Design Exercise: Insurance AI Platform Design
We will design a multi-module AI system to automate insurance operations:
1.  **Claims Module**: Automates claim document parsing.
2.  **Underwriting Module**: Evaluates applicant risk profiles.
3.  **Customer Service Module**: Serves chat assistants.
4.  **AI Copilot**: Orchestrates agent tasks.

```
+-------------------------------------------------------------------------------------------------+
|                                 Insurance AI Platform Topology                                  |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Istio Ingress Gateway                                  |   |
|   |   - Routes client requests and validates Keycloak JWT tokens                            |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                      +--------------------+--------------------+                                |
|                      |                                         |                                |
|                      v (Route)                                 v (Route)                        |
|   +------------------+------------------+   +------------------+------------------+             |
|   |           Claims Namespace          |   |        Underwriting Namespace       |             |
|   |   - Claims API (FastAPI)            |   |   - Underwriting API (FastAPI)      |             |
|   |   - Model worker (Triton)           |   |   - Policy database (PostgreSQL)    |             |
|   +------------------+------------------+   +------------------+------------------+             |
|                      |                                         |                                |
|                      +--------------------+--------------------+                                |
|                                           |                                                     |
|                                           v (Log Events)                                        |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  Message Broker (Kafka)                                 |   |
|   |   - Logs claims and policy events for audit and compliance checks                       |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

#### Core Components
*   **Ingress Gateway**: Enforces TLS and validates Keycloak JWT tokens.
*   **Claims Namespace**: Decoupled environment running the Claims API and Triton model workers.
*   **Underwriting Namespace**: Runs the Underwriting API and PostgreSQL database.
*   **Audit Broker (Kafka)**: Logs claim and policy events to maintain an audit trail for compliance.

### Case Study: Hexagonal Architecture at Uber
Uber refactored their payment processing engines using Hexagonal Architecture. By separating core transaction logic from database drivers and external API integrations using ports and adapters, they simplified testing and allowed database updates without affecting business logic.

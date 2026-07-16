# Phase 8: Backend Engineering Academy

Welcome to the **Backend Engineering Academy**. This phase of the AI Forward Deployed Engineer (FDE) curriculum covers high-performance API design (FastAPI, Flask, gRPC), secure identity management (Authentication, Authorization), edge routing gateways, microservice architectures, event-driven streaming (Kafka), observability, and AI backend platforms.

---

## 🗺️ Course Syllabus

The academy consists of **12 theoretical modules (90%)** and **5 practical projects (10%)**, alongside an interactive dashboard for hands-on planning and calculations.

### 📚 Theory Modules
1. **[Module 1: FastAPI](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/01_fastapi.md)**: REST API design, dependency injection, async loops, Pydantic, and background tasks.
2. **[Module 2: Flask](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/02_flask.md)**: Flask routing, blueprints, WSGI middlewares, and serving legacy models.
3. **[Module 3: gRPC](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/03_grpc.md)**: Protocol Buffers schema, unary vs. streaming RPC channels, and inter-service connections.
4. **[Module 4: Authentication](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/04_authentication.md)**: JWT verification, OAuth2 flows, OIDC registries, API keys, and SSO.
5. **[Module 5: Authorization](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/05_authorization.md)**: RBAC schemas, ABAC rules, multi-tenant separation, and policy engine audits.
6. **[Module 6: API Gateway](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/06_api_gateway.md)**: Request routing pools, reverse proxy configurations, and rate-limiting.
7. **[Module 7: Microservices](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/07_microservices.md)**: Service discovery, REST/gRPC contracts, database isolation, and circuit breakers.
8. **[Module 8: Event-Driven Architecture](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/08_event_driven.md)**: Event stream queues, Kafka publishers & subscribers, event sourcing, and CQRS.
9. **[Module 9: Backend Architecture Patterns](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/09_architecture_patterns.md)**: Monolith vs. microservices, clean and hexagonal architecture configurations, and Domain-Driven Design (DDD).
10. **[Module 10: Backend Observability](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/10_observability.md)**: Distributed tracing (OpenTelemetry), structured logging, and system health metrics.
11. **[Module 11: Backend Security](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/11_security.md)**: OWASP API top 10, secrets vaults management, TLS encryption, and zero trust models.
12. **[Module 12: Backend Engineering for AI Platforms](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/modules/12_ai_backend.md)**: Inference serving gateways, multi-tenant billing logs, and distributed TPU/GPU clusters.

---

## 🛠️ Practical Projects (10%)

Each project folder includes a complete mockable implementation showing real APIs, dynamic routing logic, and data validation:

1. **[Project 1: Enterprise AI API Platform](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/projects/project1_api_platform/run_project.py)**
   * **Skills**: FastAPI routes, Pydantic parameter schemas, JWT validation, and RBAC token audits.
2. **[Project 2: AI Model Serving Platform](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/projects/project2_model_serving/run_project.py)**
   * **Skills**: Flask serving web interfaces, API gateway redirection, and load balancing proxies.
3. **[Project 3: Distributed AI Platform](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/projects/project3_distributed_platform/run_project.py)**
   * **Skills**: gRPC-style Proto schema compilation and client-server unary/streaming calls.
4. **[Project 4: Enterprise AI Copilot Backend](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/projects/project4_copilot_backend/run_project.py)**
   * **Skills**: API Gateway rate limiter validation, JWT tokens, and RBAC permissions.
5. **[Project 5: Event-Driven AI Workflow Platform](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/projects/project5_event_driven/run_project.py)**
   * **Skills**: Event streaming brokers (Kafka style), Producer-Consumer message loops, and async worker tasks.

---

## 🎓 Interview Preparation
- **[Interview Preparation Guide](file:///d:/ai-forward-deployed-engineer-zero-to-hero/backend_engineering/interview_prep.md)**: Technical questions, microservices, gRPC, JWT tokens, event sourcing, system designs, and FDE discovery protocols.

---

## 🌐 Interactive Web Hub (Course Dashboard)

To explore interactive dashboards, index estimators, quiz modules, and playgrounds:
1. Locate the directory `backend_engineering/course_hub/`.
2. Launch a local web server:
   ```bash
   python -m http.server 8000 --directory backend_engineering/course_hub
   ```
3. Open your browser and navigate to `http://localhost:8000/`.

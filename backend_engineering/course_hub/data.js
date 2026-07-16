// Unified Database - Backend Engineering Academy Dashboard
const COURSE_DATA = {
  modules: [
    {
      id: "m1",
      title: "Module 1: FastAPI Applications",
      summary: "Understand async loops, Pydantic data schemas, dependency injection, and background tasks.",
      details: `
<h3>Key Concepts</h3>
<p>FastAPI runs on an asynchronous event loop (using ASGI servers like Uvicorn) to handle concurrent connections efficiently, using Pydantic for data validation.</p>
<h4>1. Dependency Injection</h4>
<p>Decoupling database connections, security checks, and service configurations from routing logic makes code modular and easy to test.</p>
      `,
      fileLink: "../modules/01_fastapi.md"
    },
    {
      id: "m2",
      title: "Module 2: Flask Services",
      summary: "Explore Flask routing blueprints, WSGI middlewares, application factories, and legacy model serving.",
      details: `
<h3>Key Concepts</h3>
<p>Flask is a lightweight WSGI framework commonly used in legacy codebases and traditional machine learning pipelines.</p>
<h4>1. Application Factory Pattern</h4>
<p>Initializing database drivers and extensions dynamically prevents global state issues and supports modular testing.</p>
      `,
      fileLink: "../modules/02_flask.md"
    },
    {
      id: "m3",
      title: "Module 3: gRPC Communications",
      summary: "Configure Protocol Buffers, RPC unary and streaming calls, and microservice connections.",
      details: `
<h3>Key Concepts</h3>
<p>gRPC uses Protocol Buffers to compile service contracts into binary payloads, significantly reducing network overhead and latency compared to REST.</p>
<h4>1. HTTP/2 Transport</h4>
<p>Multiplexing requests over a single TCP connection minimizes handshake overhead and keeps latency low.</p>
      `,
      fileLink: "../modules/03_grpc.md"
    },
    {
      id: "m4",
      title: "Module 4: Authentication Security",
      summary: "Master JWT validation, OAuth2 credential flows, OIDC, and SSO integrations.",
      details: `
<h3>Key Concepts</h3>
<p>Enterprise authentication uses token-based validation to verify identities securely across services.</p>
<h4>1. Asymmetric Token Verification (RS256)</h4>
<p>Signing tokens with private keys and verifying signatures locally using public keys allows services to validate identities without storing secrets.</p>
      `,
      fileLink: "../modules/04_authentication.md"
    },
    {
      id: "m5",
      title: "Module 5: Authorization Governance",
      summary: "Tune RBAC role groups, ABAC policies, tenant boundaries, and audit logging.",
      details: `
<h3>Key Concepts</h3>
<p>Authorization controls access to resources based on roles (RBAC) and attributes (ABAC).</p>
<h4>1. Object-Level Access (BOLA)</h4>
<p>Always verify resource ownership and check tenant boundaries at the microservice layer to prevent unauthorized data access.</p>
      `,
      fileLink: "../modules/05_authorization.md"
    },
    {
      id: "m6",
      title: "Module 6: API Gateway Routing",
      summary: "Deploy edge reverse proxy controllers, NGINX/Kong gateway rates, and load balancing.",
      details: `
<h3>Key Concepts</h3>
<p>API Gateways manage entry points, route traffic, handle SSL termination, and enforce rate limits at the edge of the network.</p>
<h4>1. Token Bucket Rate Limiting</h4>
<p>Tracking request counts in fast Redis caches to limit access rates and protect internal services from overload.</p>
      `,
      fileLink: "../modules/06_api_gateway.md"
    },
    {
      id: "m7",
      title: "Module 7: Microservices Integration",
      summary: "Master service discovery, REST/gRPC service contracts, and circuit breakers.",
      details: `
<h3>Key Concepts</h3>
<p>Microservice architectures partition business logic into loosely coupled services, scaling resources independently.</p>
<h4>1. Circuit Breaker Pattern</h4>
<p>Wrapping network calls in circuit breakers to handle downstream timeouts and prevent cascading failures.</p>
      `,
      fileLink: "../modules/07_microservices.md"
    },
    {
      id: "m8",
      title: "Module 8: Event-Driven Architecture",
      summary: "Design Kafka message streams, event publishers, consumer groups, and event sourcing.",
      details: `
<h3>Key Concepts</h3>
<p>Event-Driven Architecture coordinates services asynchronously by publishing and consuming events, reducing coupling.</p>
<h4>1. Dead Letter Queues (DLQ)</h4>
<p>Routing failing events to a separate DLQ to isolate errors and prevent corrupt messages from blocking processing pipelines.</p>
      `,
      fileLink: "../modules/08_event_driven.md"
    },
    {
      id: "m9",
      title: "Module 9: Backend Design Patterns",
      summary: "Learn Clean and Hexagonal architecture, domain boundaries, and DDD.",
      details: `
<h3>Key Concepts</h3>
<p>Hexagonal Architecture isolates business rules from external technologies using abstract interface adapters (Ports & Adapters).</p>
      `,
      fileLink: "../modules/09_architecture_patterns.md"
    },
    {
      id: "m10",
      title: "Module 10: Platform Observability",
      summary: "Implement OpenTelemetry distributed tracing, structured JSON logging, and prometheus metrics.",
      details: `
<h3>Key Concepts</h3>
<p>Observability monitors platform health using logs, metrics, and distributed tracing across microservices.</p>
<h4>1. Distributed Tracing</h4>
<p>Propagating unique trace IDs through request headers to track workflows across services.</p>
      `,
      fileLink: "../modules/10_observability.md"
    },
    {
      id: "m11",
      title: "Module 11: Production Security Protocols",
      summary: "Scan OWASP API top 10 vulnerabilities, Vault keys, and mTLS networks.",
      details: `
<h3>Key Concepts</h3>
<p>Production security requires encrypting data at rest and in transit, securing credentials, and protecting APIs from vulnerabilities.</p>
<h4>1. Mutual TLS (mTLS)</h4>
<p>Encrypting all network connections between microservices and requiring authorization checks for every call.</p>
      `,
      fileLink: "../modules/11_security.md"
    },
    {
      id: "m12",
      title: "Module 12: Backend for AI Platforms",
      summary: "Design inference server queues, semantic caches, usage counters, and GPU scaling.",
      details: `
<h3>Key Concepts</h3>
<p>AI backends manage compute-heavy GPU workloads, optimize context windows, and track API costs.</p>
<h4>1. Semantic Caching</h4>
<p>Caching model prompts and responses in Redis to reduce token costs on repetitive queries.</p>
      `,
      fileLink: "../modules/12_ai_backend.md"
    }
  ],
  projects: [
    {
      id: "p1",
      title: "Project 1: Enterprise AI API Platform",
      description: "FastAPI request schemas and JWT RBAC validations.",
      systemPrompt: "FastAPI Endpoint: /api/v1/inference. Validate JWT headers. Required role: 'Admin'.",
      inputs: [
        { name: "token", label: "Authorization Token Header", type: "text", default: "valid_admin_token" },
        { name: "prompt", label: "Pydantic Prompt Text", type: "text", default: "Audit contract clauses for liability limits." }
      ],
      mockResponses: [
        { match: "admin", text: "[FASTAPI MIDDLEWARE] Token validated. User: user_402 (Role: Admin)\n[PYDANTIC] Request payload validated successfully: {'prompt': 'Audit contract clauses.', 'max_tokens': 64}\n[AUTHORIZATION GATE] RBAC Audited. Access granted.\n\nFinal Response:\n{\n  \"status_code\": 200,\n  \"data\": { \"model\": \"Llama-3-8B\", \"choices\": [{\"text\": \"Simulated prediction text.\"}] }\n}" },
        { match: "*", text: "[FASTAPI MIDDLEWARE] Token validated. User: user_109 (Role: Reader)\n[AUTHORIZATION GATE] {\"status_code\": 403, \"detail\": \"RBAC Denied. Required role: Admin. User role: Reader\"}" }
      ]
    },
    {
      id: "p2",
      title: "Project 2: AI Model Serving Platform",
      description: "API Gateway routing between legacy Flask classifiers and modern FastAPI endpoints.",
      systemPrompt: "Gateway routes /api/v1/legacy to Flask and /api/v1/inference to FastAPI.",
      inputs: [
        { name: "path", label: "API Gateway Request Path", type: "text", default: "/api/v1/legacy/classify" }
      ],
      mockResponses: [
        { match: "legacy", text: "[GATEWAY] Incoming Request Path: '/api/v1/legacy/classify'\n -> Gateway Routing Decision: Forward to Legacy Flask Service.\n\n[FLASK SERVER] Received request on blueprint: '/blueprints/classify'\n[FLASK SERVER] Running Scikit-Learn classifier...\n\nFlask Response:\n{ \"model_type\": \"Scikit-Learn Random Forest\", \"prediction\": \"LOW_RISK\" }" },
        { match: "*", text: "[GATEWAY] Incoming Request Path: '/api/v1/inference/chat'\n -> Gateway Routing Decision: Forward to FastAPI Serving Service.\n\n[FASTAPI SERVER] Received request on async route: '/v1/chat'\n[FASTAPI SERVER] Processing LLM prompt...\n\nFastAPI Response:\n{ \"model_type\": \"Llama-3-8B\", \"choices\": [{\"text\": \"Completed predictions.\"}] }" }
      ]
    },
    {
      id: "p3",
      title: "Project 3: Distributed AI Platform",
      description: "gRPC Protobuf serialization comparison and streaming requests.",
      systemPrompt: "Protobuf binary formatting and TCP HTTP/2 stream chunk simulator.",
      inputs: [
        { name: "prompt", label: "Protobuf Request Prompt", type: "text", default: "Analyze server logs and report errors." }
      ],
      mockResponses: [
        { match: "*", text: "[PERFORMANCE TEST] Comparing JSON vs Protobuf...\n - JSON Payload Size: 62 bytes | Serialization Time: 0.12ms\n - Proto Payload Size: 45 bytes | Serialization Time: 0.03ms\n -> Size Reduction: 27.4% smaller\n\n[gRPC CLIENT] Executing Unary Call...\n[gRPC SERVER] Deserialized Unary Request. Prompt: 'Analyze server logs'\n[gRPC CLIENT] Received Unary Response: 'Completed inference'\n\n[gRPC CLIENT] Executing Server Streaming Call...\n[gRPC SERVER] Starting token stream...\n -> Chunk: 'Executive '\n -> Chunk: 'brief: '\n -> Chunk: 'Llama-3 '" }
      ]
    },
    {
      id: "p4",
      title: "Project 4: Enterprise AI Copilot Backend",
      description: "Secure gateway token bucket rate limiting and tenant checks.",
      systemPrompt: "Redis-style Token Bucket capacity = 3. Gateway verifies key authentication.",
      inputs: [
        { name: "key", label: "API Client Key", type: "text", default: "key_user_01" },
        { name: "tenant", label: "Target Tenant ID", type: "text", default: "tenant_a" }
      ],
      mockResponses: [
        { match: "user_02", text: "[GATEWAY] Processing request for API Key: 'key_user_02'\n[AUDIT LOG] {'user_id': 'user_beta', 'action': 'API_ACCESS', 'status': 'RATE_LIMITED'}\n\nGateway Response:\n{ \"status_code\": 429, \"error\": \"Too Many Requests. Rate limit exceeded.\" }" },
        { match: "tenant_b", text: "[GATEWAY] Processing request for API Key: 'key_user_01'\n[AUDIT LOG] {'user_id': 'user_alpha', 'action': 'RESOURCE_ACCESS', 'status': 'DENIED', 'detail': 'Tenant mismatch'}\n\nGateway Response:\n{ \"status_code\": 403, \"error\": \"Forbidden. Tenant access mismatch.\" }" },
        { match: "*", text: "[GATEWAY] Processing request for API Key: 'key_user_01'\n[AUDIT LOG] {'user_id': 'user_alpha', 'action': 'RESOURCE_ACCESS', 'status': 'APPROVED'}\n\nGateway Response:\n{ \"status_code\": 200, \"data\": \"Access approved.\" }" }
      ]
    },
    {
      id: "p5",
      title: "Project 5: Event-Driven AI Workflow Platform",
      description: "Asynchronous document ingestion consumer processing.",
      systemPrompt: "Kafka topics: document_uploaded -> text_extracted -> embeddings_generated.",
      inputs: [
        { name: "file", label: "Upload Document File Name", type: "text", default: "policy_guideline.pdf" }
      ],
      mockResponses: [
        { match: "*", text: "[PRODUCER] Uploading file: 'policy_guideline.pdf'...\n[KAFKA BROKER] Produced event to Topic 'document_uploaded' | Offset: 0\n\n[KAFKA BROKER] Consumer 'text_extractor_group' read from Topic 'document_uploaded' | Offset: 0\n[CONSUMER: TextExtractor] Processing document: 'policy_guideline.pdf'\n[KAFKA BROKER] Produced event to Topic 'text_extracted' | Offset: 0\n\n[KAFKA BROKER] Consumer 'vector_indexer_group' read from Topic 'text_extracted' | Offset: 0\n[CONSUMER: VectorIndexer] Ingesting and indexing text: 'ALL STAFF CAN WORK REMOTELY...'\n[CONSUMER: VectorIndexer] Successfully indexed 'policy_guideline.pdf' in ChromaDB." }
      ]
    }
  ],
  quiz: [
    {
      question: "What is the primary risk of using synchronous functions (like standard time.sleep() or legacy database drivers) inside a FastAPI 'async def' path handler?",
      options: [
        "It invalidates Pydantic response models",
        "It blocks the single-threaded async event loop, slowing down all concurrent requests",
        "It triggers token bucket rate limiters",
        "It corrupts local SQLite database files"
      ],
      answer: 1,
      explanation: "Slow synchronous operations run inside 'async def' block the event loop, preventing FastAPI from processing other concurrent requests until the blocking operation completes."
    },
    {
      question: "In microservice architectures, why is RS256 token signing preferred over HS256?",
      options: [
        "RS256 uses binary Protocol Buffers which are faster to serialize",
        "RS256 uses asymmetric key pairs, allowing microservices to verify tokens using only a public key without storing secret keys",
        "RS256 is compatible with legacy Flask blueprints",
        "RS256 handles rate limiting token buckets automatically"
      ],
      answer: 1,
      explanation: "RS256 uses asymmetric key pairs. Microservices only store the public key to verify signatures, keeping the signing private key secure."
    },
    {
      question: "Which pattern isolates microservice databases to prevent schema coupling?",
      options: [
        "Circuit Breaker Pattern",
        "Database-per-Service Pattern",
        "Hexagonal Port Pattern",
        "Dead Letter Queue Pattern"
      ],
      answer: 1,
      explanation: "The Database-per-Service pattern ensures each microservice accesses and manages its own database, preventing service coupling."
    },
    {
      question: "What is the role of a Dead Letter Queue (DLQ) in event-driven systems?",
      options: [
        "To route search queries to active replica nodes",
        "To isolate and store failing event messages for audit, preventing corrupt messages from blocking processing pipelines",
        "To compress binary gRPC payloads",
        "To execute code scripts in sandboxed environments"
      ],
      answer: 1,
      explanation: "A DLQ isolates and stores corrupt or failing events, allowing developers to audit errors without blocking processing queues."
    },
    {
      question: "In Hexagonal Architecture, what is the role of 'Ports'?",
      options: [
        "To configure network load balancers",
        "To define abstract interfaces that decouple core business logic from external databases and third-party APIs",
        "To route client requests inside API Gateways",
        "To store conversation histories in Redis"
      ],
      answer: 1,
      explanation: "Ports define abstract interfaces (contracts) for input/output actions, keeping core business logic isolated from external packages and frameworks."
    }
  ]
};
const SERVER_TIERS = {
  "small": { cores: 2, ram: 4, costPerMonth: 20 },
  "medium": { cores: 4, ram: 8, costPerMonth: 40 },
  "large": { cores: 8, ram: 16, costPerMonth: 80 }
};

# Module 10: System Design Interview Preparation & Platform Questions

This module compiles deep technical interview questions and model answers across System Design topics.

---

## 1. Distributed Systems

### Q1: Explain the CAP Theorem and its trade-offs.
*   **Answer**: The CAP Theorem states that a distributed system can guarantee at most two of three properties simultaneously: Consistency, Availability, and Partition Tolerance. In practice, systems must support Partition Tolerance due to network realities, forcing a choice between Consistency (CP systems, returning errors if nodes cannot sync) and Availability (AP systems, returning stale data).

### Q2: Explain the Saga Pattern for distributed transactions.
*   **Answer**: The Saga Pattern manages distributed transactions by breaking them into a sequence of local transactions across microservices. Each service executes a local transaction and publishes an event. If a step fails, the coordinator triggers compensating transactions in reverse order to revert changes.

---

## 2. Scalability & High Availability

### Q1: How do you design a system to support 50,000 requests per second?
*   **Answer**: Deploy API gateways to manage routing and rate limiting, distribute load using Layer-7 load balancers, scale application instances horizontally on Kubernetes, implement distributed caching (like Redis) to bypass database calls, and use message queues (like Kafka) to process requests asynchronously.

### Q2: What is a Single Point of Failure (SPOF), and how do you eliminate it?
*   **Answer**: A SPOF is any component whose failure crashes the entire system. Eliminate it by adding redundancy: deploying multiple service instances across availability zones, configuring active-passive load balancers, and running primary-secondary database replication with automated failover.

---

## 3. Disaster Recovery

### Q1: Explain the difference between RTO and RPO.
*   **Answer**:
    *   **RTO (Recovery Time Objective)**: The target duration to restore system operations after an outage.
    *   **RPO (Recovery Point Objective)**: The maximum allowable data loss window, measured in time.

---

## 4. Event-Driven Systems

### Q1: Why is Kafka preferred over standard queues for event streaming?
*   **Answer**: Kafka is designed as a distributed commit log, storing events sequentially on disk. This allows multiple consumer groups to read messages independently at their own pace, and supports message replay, which is critical for system auditing and recovery.

---

## 5. AI System Design

### Q1: How do you design a vector ingestion pipeline for a RAG system?
*   **Answer**: User uploads trigger document upload events. Worker nodes consume events, partition text into chunks, generate embeddings using model APIs, write vectors to a vector database, and log transaction metadata to PostgreSQL.

---

## 6. Multi-Tenant Architecture

### Q1: Explain the trade-offs between Shared Database and Separate Database models.
*   **Answer**:
    *   **Shared Database**: High resource efficiency and simple maintenance, but carries a risk of accidental data exposure and resource contention ("noisy neighbors").
    *   **Separate Database**: Strongest isolation and security, but at higher hosting and operational costs.

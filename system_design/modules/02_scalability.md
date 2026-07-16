# Module 2: System Scalability, Caching & Load Balancing Patterns

## 1. Theory (60%)

### What is Scalability?
Scalability is the ability of a system to handle increasing workloads (such as higher query volume or larger datasets) by adding resources without degrading performance.

```
+-------------------------------------------------------------------------------------------------+
|                                        Scalability Patterns                                     |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |  Vertical Scaling |      | Horizontal Scaling|      | Database Sharding |                   |
|   |   (Scale Up CPU)  |      |  (Scale Out Pods) |      | (Split by Tenant) |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|       4 CPU -> 16 CPU            1 Pod -> 100 Pods          Node A (1-50) | Node B (51-100)     |
+-------------------------------------------------------------------------------------------------+
```

### Scaling Paradigms
*   **Vertical Scaling (Scale Up)**: Adding compute resources (CPUs, VRAM, RAM) to a single machine. Limited by hardware bounds and introduces a single point of failure (SPOF).
*   **Horizontal Scaling (Scale Out)**: Adding more independent node instances to the cluster. This is the preferred approach for cloud-native architectures due to elasticity.

### Scalability Patterns

#### Load Balancing
Routing incoming client requests across available worker nodes:
*   **NGINX**: High-performance HTTP server and reverse proxy.
*   **Application Load Balancers (ALB)**: Layer-7 routing proxies that inspect HTTP headers to route requests.
*   **HAProxy**: High-performance TCP/HTTP load balancer.

#### Distributed Caching
Storing frequently accessed data in low-latency memory caches:
*   **Redis / Memcached**: In-memory databases that serve read queries in sub-milliseconds, bypassing database calls.

#### Database Scaling
*   **Read Replicas**: Directing write transactions to a primary database node while routing read queries to secondary replica nodes.
*   **Sharding / Partitioning**: Splitting database tables horizontally to distribute storage and I/O load across multiple servers.

#### Queue-Based Scaling (Asynchronous Processing)
*   Using message brokers (like Kafka or RabbitMQ) to store requests. Worker processes consume messages from the queue at their own pace, preventing database overload during traffic spikes.

---

## 2. Practical (40%)

### Design Exercise: Enterprise ChatGPT Platform Design
We will design a globally scalable system layout to support **10 Million Users** and **50,000 Requests Per Second (RPS)**.

```
+-------------------------------------------------------------------------------------------------+
|                                        ChatGPT Platform                                         |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Anycast DNS & CDN                                      |   |
|   |   - Routes user queries to the closest regional edge location                           |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Local Region Ingress)                          v (Local Region Ingress)|
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |               API Gateway               |     |               API Gateway               |   |
|   |   - Enforces auth and rate limits       |     |   - Enforces auth and rate limits       |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Read Cache)                                    v (Read Cache)          |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |              Redis Cache                |     |              Redis Cache                |   |
|   |   - Serves active sessions in sub-ms    |     |   - Serves active sessions in sub-ms    |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Compute Cluster)                               v (Compute Cluster)     |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |          Kubernetes Nodes (vLLM)        |     |          Kubernetes Nodes (vLLM)        |   |
|   |   - Dynamic auto-scaling of serving pods|     |   - Dynamic auto-scaling of serving pods|   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Global Write Store)                           |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                              Global Sharded Database                                    |   |
|   |   - Shards data across regions to ensure low-latency writes                             |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

#### Core Components
1.  **Global Edge (CDN)**: Caches static content close to users to reduce latency.
2.  **API Gateway**: Manages rate limiting, routing, and user authentication.
3.  **Redis Cache Layer**: Stores session data and active chat history, reducing database load.
4.  **Kubernetes Scaling Nodes (vLLM)**: Auto-scales predictor pods based on concurrent request counts.
5.  **Global Sharded Database**: Shards user data across regional database servers to ensure low-latency write operations.

### Case Study: Scaling Twitter's Timeline
Twitter migrated from a pull-based timeline generation model to a push-based model. When a user posts a tweet, the system writes it directly to the Redis caches of the user's followers. This optimization shifted CPU-heavy query logic to fast memory lookups, allowing the platform to scale under heavy traffic.

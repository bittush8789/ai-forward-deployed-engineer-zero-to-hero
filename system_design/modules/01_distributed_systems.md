# Module 1: Distributed Systems Design & Microservice Communication

## 1. Theory (60%)

### What is a Distributed System?
A distributed system is a collection of independent services running across multiple machines that coordinate execution via networks to function as a single system. Enterprise platforms (like Google Search, Netflix, Uber, or ChatGPT) rely on distributed systems to scale compute capacities.

```
+-------------------------------------------------------------------------------------------------+
|                                        Distributed Topology                                     |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                       API Gateway                                       |   |
|   |   - Authenticates requests and routes traffic to backend microservices                  |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (gRPC / HTTP Call)                              v (gRPC / HTTP Call)    |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |               User Service              |     |               Agent Service             |   |
|   |   - Manages accounts (PostgreSQL)       |     |   - Manages tool executions (Redis) |   |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|                       |                                                 |                       |
|                       +------------------------+------------------------+                       |
|                                                |                                                |
|                                                v (Event Broker)                                 |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                                    Message Broker (Kafka)                               |   |
|   |   - Asynchronous event bus enabling decoupled communication across downstream layers      |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts

#### Service Communication Protocols
*   **REST (HTTP/JSON)**: Simple, stateless protocol. High bandwidth overhead due to verbose JSON parsing.
*   **gRPC (HTTP/2 / Protobuf)**: Low-latency, binary serialization format. Supports streaming, ideal for internal microservice communication.
*   **Message Queues / Event Streams (Kafka, RabbitMQ)**: Asynchronous event brokers that decouple producer services from consumers, improving reliability.

#### Distributed Data Patterns
*   **Replication**: Duplicating data across multiple database nodes to improve read performance and ensure tolerance to single-node failures.
*   **Partitioning/Sharding**: Splitting large databases horizontally based on a key (e.g., tenant ID) to distribute storage across nodes.

#### Distributed Consistency (CAP Theorem)
A distributed system can guarantee at most two of the following properties simultaneously:
*   **Consistency (C)**: Every read returns the most recent write.
*   **Availability (A)**: Every request receives a non-error response.
*   **Partition Tolerance (P)**: The system continues to operate despite network connection drops between nodes.

#### Distributed Coordination
*   **Consensus**: Algorithms (like Raft or Paxos) that ensure distributed nodes agree on a single data value or system state.
*   **Distributed Locks**: Mechanisms (using Redis Redlock or ZooKeeper) that prevent concurrent access to shared resources across instances.

### Design Patterns
*   **API Gateway**: A single entry point that manages routing, rate limiting, and authentication.
*   **Service Mesh**: A infrastructure layer (like Istio) that manages service-to-service communication, retries, and circuit breakers.
*   **Saga Pattern**: Managing distributed transactions across microservices by executing local transactions and triggering compensation transactions if a step fails.
*   **CQRS (Command Query Responsibility Segregation)**: Segregating read and write operations into separate database models.

---

## 2. Practical (40%)

### Build: Enterprise AI Platform Microservices
We will design a modular AI platform consisting of six microservices:
1.  **User Service**: Manages accounts and access controls.
2.  **Agent Service**: Orchestrates prompt compilation and tool calls.
3.  **RAG Service**: Manages vector index retrievals.
4.  **Embedding Service**: Generates vector representations.
5.  **Model Serving Service**: Hosts inference containers (vLLM/Triton).
6.  **Billing Service**: Meters token consumption.

#### Tech Stack
*   **Framework**: FastAPI (Python)
*   **Metadata DB**: PostgreSQL
*   **Cache & Locks**: Redis
*   **Event Broker**: Apache Kafka
*   **Orchestration**: Kubernetes

### Design Exercise: Implementing Resilient Communications
Write a Python script using FastAPI and the `tenacity` library to configure retry logic and circuit breakers for inter-service communication:
```python
# /tmp/resilient_client.py
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.failure_count = 0
        self.circuit_open = False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def fetch_data(self):
        # Implement a simple local circuit breaker check
        if self.circuit_open:
            print("Circuit is OPEN. Aborting network call.")
            raise Exception("CircuitOpenException")
            
        print(f"Attempting connection to service: {self.target_url}")
        try:
            # Simulate a request
            response = requests.get(self.target_url, timeout=2)
            self.failure_count = 0 # reset on success
            return response.json()
        except requests.exceptions.RequestException as e:
            self.failure_count += 1
            if self.failure_count >= 3:
                self.circuit_open = True
                print("Failures exceeded limit. Tripping circuit to OPEN.")
            raise e

if __name__ == '__main__':
    # Initialize client (points to dummy port for connection failure testing)
    client = ServiceClient("http://localhost:5999/api/v1/data")
    try:
        client.fetch_data()
    except Exception as err:
        print(f"Request execution failed: {err}")
```
Run the client validation:
```bash
pip install requests tenacity
python3 /tmp/resilient_client.py
```

### Case Study: Netflix gRPC Migration
Netflix migrated internal microservice communication from REST/JSON to gRPC. By using HTTP/2 multiplexing and binary Protocol Buffers, they reduced network bandwidth requirements by 40% and improved response latency, improving API reliability.

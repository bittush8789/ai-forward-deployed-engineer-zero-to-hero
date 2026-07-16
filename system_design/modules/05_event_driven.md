# Module 5: Event-Driven Architectures & Real-Time Kafka Pipelines

## 1. Theory (60%)

### What is Event-Driven Architecture?
Event-Driven Architecture (EDA) is a design pattern where decoupled services communicate by generating, caching, and consuming events. An event represents a state change or action that occurred in the system.

```
+-------------------------------------------------------------------------------------------------+
|                                    Event-Driven Architecture                                    |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |   Producer (API)  | ---> |   Event Broker    | ---> |    Consumer (ML)  |                   |
|   |  (Generate event) |      | (Kafka/RabbitMQ)  |      |  (Process event)  |                   |
|   +-------------------+      +---------+---------+      +-------------------+                   |
|                                        |                                                        |
|                                        v (Decoupling)                                           |
|                              Multiple downstream systems can                                    |
|                              subscribe to the same topic                                        |
+-------------------------------------------------------------------------------------------------+
```

### Core Components
*   **Producers**: Services that capture occurrences and publish them as event messages to the broker.
*   **Brokers**: Intermediate message distribution systems (such as Apache Kafka or RabbitMQ) that store, organize, and route events.
*   **Consumers**: Services that subscribe to topics and process event payloads asynchronously.

### Design Benefits
*   **Decoupling**: Producers have no dependencies on consumer implementations or statuses.
*   **Scalability**: Consumers can be scaled independently to process messages from specific partitions.
*   **Reliability**: If a consumer service crashes, events remain in the broker queue, allowing the consumer to resume processing once restarted without data loss.

### Communication Patterns
*   **Publish/Subscribe (Pub/Sub)**: Events are published to a topic and broadcast to all subscribed consumer groups.
*   **Event Streaming**: Storing sequence-ordered events in a log, allowing consumers to replay history.
*   **Event Sourcing**: Storing mutations as a sequence of events rather than updating database tables directly.

---

## 2. Practical (40%)

### Design Exercise: AI Ingestion Workflow Platform
We will design an asynchronous AI processing pipeline:
1.  **File Upload**: User uploads a document, triggering a `FileUploadedEvent`.
2.  **Embedding Generation**: The embedding service consumes the event, generates vector matrices, and publishes an `EmbeddingGeneratedEvent`.
3.  **Index Update**: The RAG service consumes the event, writes vectors to the database, and publishes an `IndexUpdatedEvent`.

```
+-------------------------------------------------------------------------------------------------+
|                                      AI Ingestion Pipeline                                      |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                    FastAPI Service                                      |   |
|   |   - Accepts raw document uploads and publishes FileUploadedEvent to Kafka               |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Publish FileUploadedEvent)                         |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  Message Broker (Kafka)                                 |   |
|   |   +---------------------------------------------------------------------------------+   |   |
|   |   | Topic: file-uploads  ---> Topic: embeddings-generated ---> Topic: index-updated |   |   |
|   |   +---------------------------------------------------------------------------------+   |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Consume / Process Events)                          |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                  Compute Services                                       |   |
|   |   - Embedding Service: Generates vector representations                                 |   |
|   |   - RAG Service: Writes vector embeddings to Database                                   |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Hands-On Task: Event Stream Processing Script
Write a Python script simulating an asynchronous event processing pipeline:
```python
# /tmp/event_pipeline.py
import json
import time

def simulate_event_pipeline():
    print("=== Starting Asynchronous AI Ingestion Pipeline ===")
    
    # 1. Simulate File Upload Event
    upload_event = {
        "event_id": "evt_1001",
        "type": "FileUploadedEvent",
        "file_name": "annual_report.pdf",
        "timestamp": time.time()
    }
    print(f"Producer published: {upload_event['type']} for {upload_event['file_name']}")
    
    # 2. Simulate Embedding Service Consumer
    time.sleep(0.5)
    print(f"Consumer (Embedding Service) received {upload_event['type']}.")
    print("Generating vector representation mappings...")
    
    embed_event = {
        "event_id": "evt_1002",
        "type": "EmbeddingGeneratedEvent",
        "dimensions": 1536,
        "source_event": upload_event["event_id"]
    }
    print(f"Producer published: {embed_event['type']}")
    
    # 3. Simulate Database Writer Consumer
    time.sleep(0.5)
    print(f"Consumer (RAG Service) received {embed_event['type']}.")
    print("Writing vector indexes to Database. Ingestion complete.")
    print("===================================================\n")

if __name__ == '__main__':
    simulate_event_pipeline()
```
Run the validation:
```bash
python3 /tmp/event_pipeline.py
```

### Case Study: LinkedIn's Kafka Deployment
LinkedIn developed and deployed Apache Kafka to manage activity stream tracking. By standardizing internal communications on high-throughput event logs, they decoupled downstream databases from write loads, preventing database bottlenecks.

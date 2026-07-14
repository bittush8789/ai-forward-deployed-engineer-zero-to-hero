# Module 5.6: Kafka Streams

Welcome to **Kafka Streams**. While Kafka Connect moves data *into* and *out of* Kafka, Kafka Streams processes data *inside* Kafka. It is a client library for building applications and microservices where the input and output data are stored in Kafka topics.

---

## 1. Detailed Theory

### What is Kafka Streams?
Unlike Spark Streaming (which requires a dedicated cluster and executor JVMs), Kafka Streams is a lightweight Java client library. You write your processing logic in Java/Kotlin, package it as a standard JAR, and run it inside your standard application containers (e.g., Spring Boot on Kubernetes). It uses the local disk (`RocksDB`) to maintain state.

### Core Concepts
- **KStream**: A representation of an unstructured event stream. Every message is an append to the log (e.g., `user clicked A`, `user clicked B`).
- **KTable**: A representation of a changelog stream. Every message represents an update to a state (e.g., `user_1 location is now Paris`, `user_1 location is now London`). Analogous to a database table.
- **Duality of Streams and Tables**: A stream can be aggregated into a table, and a table's state updates can be streamed as a changelog.

### Windowing & Stateful Joins
- **Stateless Processing**: Transformations that don't require historical memory (e.g., `map`, `filter`, `selectKey`).
- **Stateful Processing**: Transformations that require memory (e.g., `count`, `aggregate`, `join`). 
- **Windowing**: Aggregating events in time blocks:
  - **Tumbling Window**: Fixed-size, non-overlapping time blocks (e.g., 00:00 - 05:00, 05:00 - 10:00).
  - **Sliding Window**: Moving time windows based on event timestamps.

---

## 2. Architecture Diagram: Stream-Table Duality

```mermaid
flowchart TD
    subgraph "KStream: Raw Event Stream (Append-Only)"
        S1[Key: A | Value: 10] --> S2[Key: B | Value: 20]
        S2 --> S3[Key: A | Value: 15]
    end
    
    subgraph "KTable: Aggregated State (Latest Values)"
        T1[Key: A | Value: 15]
        T2[Key: B | Value: 20]
    end
    
    S1 -.->|Aggregated into| T1
    S2 -.->|Aggregated into| T2
    S3 -.->|Updates| T1
```

---

## 3. Production Use Cases

1. **Real-Time Fraud Detection**: A KStream of transactions is joined with a KTable of customer profile metrics (updated in real-time). If a transaction's amount exceeds the customer's average 30-day spend by 500%, the application immediately publishes an alert event to a `high-risk-transactions` topic.
2. **Live Analytics Dashboard**: Aggregating incoming website clicks in 5-minute sliding windows to count active sessions, streaming the results to a dashboard topic.

---

## 4. Real Company Examples

- **LinkedIn**: Extensively uses Kafka Streams to aggregate metrics, track user activity, and compute connection recommendation values.
- **Netflix**: Integrates Kafka Streams to parse real-time logs and monitor service performance metrics across their microservice mesh.

---

## 5. Coding Examples

### Defining a Streaming Pipeline (Java/Spring Boot Concept)

Though written in Java, the topology design follows functional patterns:

```java
// Java KStreams Topology definition
StreamsBuilder builder = new StreamsBuilder();

// 1. Ingest event stream from Topic (KStream)
KStream<String, String> clickStream = builder.stream("user-clicks");

// 2. Stateless Transformation: Filter and Map
KStream<String, String> checkoutClicks = clickStream
    .filter((key, value) -> value.contains("click_checkout"))
    .mapValues(value -> value.toLowerCase());

// 3. Stateful Aggregation (Aggregating into a KTable)
KTable<String, Long> userCheckoutCounts = checkoutClicks
    .groupByKey()
    .count(Materialized.as("checkout-counts-store")); // Local RocksDB store

// 4. Stream the updates back to another Kafka Topic
userCheckoutCounts.toStream().to("user-checkout-aggregates", Produced.with(Serdes.String(), Serdes.Long()));
```

---

## 6. Hands-on Labs

**Lab: Stream vs. Table**
**Objective**: Differentiate KStream and KTable updates.
**Instructions**:
Write out the visual state changes for:
1. A KStream.
2. A KTable.
When the following messages are received:
- `(Key: "A", Value: "1")`
- `(Key: "B", Value: "2")`
- `(Key: "A", Value: "3")`

---

## 7. Assignments

**Assignment: RocksDB Recovery**
Kafka Streams uses a local embedded key-value store called **RocksDB** on the host instance's disk to perform stateful operations (like counting or joins) fast.
Explain what happens if the Docker container running a Kafka Streams application crashes. How does Kafka Streams recover the local RocksDB state on a newly provisioned container? (Hint: Look up "Changelog Topics").

---

## 8. Interview Questions

1. **What is the difference between a KStream and a KTable?**
   *Answer Hint: A KStream is an append-only stream of independent events (insert-only). A KTable is a changelog stream representing the latest state for each key (upsert-only).*
2. **Why is Kafka Streams considered lightweight compared to Spark Streaming?**
   *Answer Hint: Kafka Streams is a standard library. It does not require a dedicated processing cluster (like Spark master/workers). You compile it into your standard application JAR and deploy it to Kubernetes or VM instances just like a regular web service.*

---

## 9. Best Practices (FDE Standards)

- **Always configure Changelogs**: Ensure stateful stores are backed by a Kafka changelog topic. This allows state to be restored on other nodes during node restarts.
- **Tune RocksDB Memory**: In production containers, RocksDB consumes off-heap memory. Explicitly limit RocksDB memory allocations to prevent the OS/Kubernetes from killing the container.

---

## 10. Common Mistakes

- **Monolithic State Stores**: Performing complex 10-table joins in a single topology, resulting in massive RocksDB directories that take hours to sync on restarts.
- **Using String Serdes for JSON**: Attempting to process complex object payloads using simple String serializers/deserializers, resulting in unparseable message exceptions.

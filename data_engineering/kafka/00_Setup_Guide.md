# Apache Kafka Setup Guide

This guide provides step-by-step instructions to configure and run Apache Kafka both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

The simplest way to run Apache Kafka locally is using **Docker Compose** with KRaft (Kafka Raft metadata mode), which eliminates the need to run Zookeeper separately.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Step-by-Step Installation (KRaft Mode)

1. **Create a Directory**:
   ```bash
   mkdir kafka-local
   cd kafka-local
   ```

2. **Create a `docker-compose.yaml` file**:
   ```yaml
   version: '3'
   services:
     kafka:
       image: confluentinc/cp-kafka:7.4.0
       container_name: kafka-kraft
       ports:
         - "9092:9092"
       environment:
         # Define broker configuration
         KAFKA_NODE_ID: 1
         KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'
         KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092'
         KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
         KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
         KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
         KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
         KAFKA_PROCESS_ROLES: 'broker,controller'
         KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:29093'
         KAFKA_LISTENERS: 'PLAINTEXT://0.0.0.0:29092,CONTROLLER://0.0.0.0:29093,PLAINTEXT_HOST://0.0.0.0:9092'
         KAFKA_INTER_BROKER_LISTENER_NAME: 'PLAINTEXT'
         KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
         KAFKA_LOG_DIRS: '/tmp/kraft-combined-logs'
         # Generate a random cluster ID for KRaft initialization
         CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
   ```

3. **Start the Broker**:
   ```bash
   docker compose up -d
   ```

4. **Verify the Installation**:
   Verify you can create a test topic using the built-in CLI binaries inside the container:
   ```bash
   # Create a topic named test-topic
   docker exec -it kafka-kraft kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

   # List topics
   docker exec -it kafka-kraft kafka-topics --list --bootstrap-server localhost:9092
   ```

---

## 2. Production Setup

Production Kafka demands absolute data availability and fault-tolerant partitions. You must set a replication factor of at least 3, use multi-availability zone node deployments, and secure access channels.

### Option A: Managed Cloud Kafka (Recommended)
Cloud providers host resilient Kafka architectures:
- **AWS MSK (Managed Streaming for Apache Kafka)**: Handles broker provisioning, Zookeeper clusters, replication configurations, and integrates with AWS IAM.
- **Confluent Cloud**: Fully serverless, managed Kafka, featuring built-in connectors, Schema Registry, and stream processing tools.

**AWS MSK Deployment Steps**:
1. Open the Amazon MSK console and create a new cluster.
2. Choose **Custom Creation**, select the Kafka version, and define the cluster type (Provisioned or Serverless).
3. Configure the VPC network, selecting at least **3 subnets** across separate Availability Zones (AZs) to match the replication factor.
4. Enable **IAM Client Authentication** or TLS mutual authentication to secure client requests.
5. In client code, configure your Python Kafka client to authenticate using AWS IAM credentials.

### Option B: Cloud-Native Kubernetes Deployment (Strimzi Operator)
To deploy and scale Kafka inside a Kubernetes cluster, utilize the **Strimzi Operator**. It simplifies creating clusters, topics, and users via custom Kubernetes resources (CRDs).

1. **Install the Strimzi Operator**:
   ```bash
   helm repo add strimzi https://strimzi.io/charts/
   helm install my-strimzi-release strimzi/strimzi-kafka-operator --namespace kafka --create-namespace
   ```

2. **Define a Kafka Cluster Resource (`kafka-cluster.yaml`)**:
   ```yaml
   apiVersion: kafka.strimzi.io/v1beta2
   kind: Kafka
   metadata:
     name: my-production-cluster
     namespace: kafka
   spec:
     kafka:
       version: 3.4.0
       replicas: 3 # High-Availability Replication
       listeners:
         - name: plain
           port: 9092
           type: internal
           tls: false
         - name: tls
           port: 9093
           type: internal
           tls: true
       config:
         offsets.topic.replication.factor: 3
         transaction.state.log.replication.factor: 3
         transaction.state.log.min.isr: 2
         default.replication.factor: 3
         min.insync.replicas: 2
       storage:
         type: persistent-claim # Mounts AWS EBS or persistent volumes dynamically
         size: 100Gi
         class: gp2
     zookeeper:
       replicas: 3
       storage:
         type: persistent-claim
         size: 10Gi
         class: gp2
   ```

3. **Deploy the Cluster**:
   ```bash
   kubectl apply -f kafka-cluster.yaml
   ```
   The Strimzi operator intercepts the manifest and provisions the StatefulSets, PersistentVolumeClaims, and headless services required to run a production-grade 3-broker cluster.

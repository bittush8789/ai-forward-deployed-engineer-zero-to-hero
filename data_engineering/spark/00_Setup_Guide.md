# Apache Spark Setup Guide

This guide provides step-by-step instructions to configure and run Apache Spark both locally (for development) and in production environments.

---

## 1. Local Setup (Development)

For PySpark development, you can run Spark in standalone mode directly on your local system or containerize it via Docker.

### Prerequisites
- Install **Java Development Kit (JDK) 8 or 11** (OpenJDK is recommended). Spark is built on Scala and requires Java runtime.
- Install **Python 3.8+**.

### PySpark Setup via pip (Simplest Local Flow)
If you only need to run PySpark scripts locally (which automatically initializes a local Spark context inside your JVM):

1. **Install PySpark**:
   ```bash
   pip install pyspark findspark
   ```

2. **Verify in Python**:
   ```python
   import findspark
   findspark.init()

   from pyspark.sql import SparkSession
   spark = SparkSession.builder.master("local[*]").appName("TestLocal").getOrCreate()
   print("Spark Version:", spark.version)
   ```

### Full Standalone Binary Setup (to run `spark-submit`)
1. **Download Spark**:
   Go to the [Apache Spark Downloads Page](https://spark.apache.org/downloads.html). Select a Spark release and package type (e.g., "Pre-built for Apache Hadoop").
2. **Extract and Set Paths**:
   Extract the `.tgz` package and move it to your system paths (e.g., `/usr/local/spark` or `C:\spark`).
3. **Configure Environment Variables**:
   Add the following variables to your shell profile (`.bashrc`, `.zshrc`, or Windows Environment variables):
   ```bash
   export SPARK_HOME=/usr/local/spark
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
   export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
   ```
4. **Start Standalone Master & Worker**:
   ```bash
   # Start the Master Node
   start-master.sh
   # Start the Worker Node (point to the Master URL shown in the logs)
   start-worker.sh spark://localhost:7077
   ```
   Access the local Spark dashboard at `http://localhost:8080`.

---

## 2. Production Setup

In production, running a standalone Spark cluster requires heavy infrastructure administration. Choose either a **Managed Cloud Cluster** or run on **Kubernetes**.

### Option A: Managed Cloud Compute (Recommended)
Managed services scale clusters dynamically based on CPU/Memory load:
- **AWS EMR (Elastic MapReduce)**: Spins up clusters of EC2 instances with Spark pre-installed.
- **Databricks**: A managed Lakehouse platform that coordinates Spark scaling and optimization (Tungsten/Catalyst) automatically.

**AWS EMR Serverless (Modern Serverless Spark)**:
1. Open the EMR Console and select **EMR Serverless**.
2. Create a new Spark application, choosing version types and CPU allocations.
3. Package your python files and dependent libraries into a zip or wheel package.
4. Upload files to S3, submit the job to EMR Serverless pointing to the entrypoint python file, and EMR scales up workers to run the job and shuts them down when done.

### Option B: Cloud-Native Kubernetes Deployment (Spark Operator)
To run Spark containerized on EKS/GKE without paying EMR administration fees, utilize the **Kubernetes Spark Operator**.

1. **Install the Spark Operator using Helm**:
   ```bash
   helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
   helm install my-release spark-operator/spark-operator --namespace spark-operator --create-namespace
   ```

2. **Define a SparkApplication resource (`spark-job.yaml`)**:
   ```yaml
   apiVersion: "sparkoperator.k8s.io/v1beta2"
   kind: SparkApplication
   metadata:
     name: pyspark-sales-aggregation
     namespace: default
   spec:
     type: Python
     pythonVersion: "3"
     mode: cluster
     image: "gcr.io/spark-operator/spark-py:v3.1.1" # Container image with Spark and Python
     mainApplicationFile: "local:///opt/spark/work-dir/app.py" # Code location inside container
     sparkVersion: "3.1.1"
     driver:
       cores: 1
       coreLimit: "1200m"
       memory: "512m"
       labels:
         version: 3.1.1
       serviceAccount: spark
     executor:
       cores: 1
       instances: 2
       memory: "512m"
       labels:
         version: 3.1.1
   ```

3. **Submit the Job**:
   ```bash
   kubectl apply -f spark-job.yaml
   ```
   The Operator intercepts this YAML file, provisions a Driver Pod, which then requests Executor Pods from the Kubernetes Scheduler to execute the distributed processing.

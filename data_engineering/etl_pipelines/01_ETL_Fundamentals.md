# Module 2.1: ETL Fundamentals

Welcome to **ETL Fundamentals**. Extract, Transform, Load (ETL) is the beating heart of Data Engineering. Before you can build an AI Agent to answer questions, you must reliably extract the raw data, transform it into a usable format, and load it into a system the AI can read.

---

## 1. Detailed Theory

### What is ETL?
ETL stands for **Extract, Transform, Load**. It is the traditional process of moving data from source systems (like transactional databases or APIs) into a Data Warehouse.
- **Extract**: Pulling data from the source.
- **Transform**: Cleaning, joining, validating, and formatting the data on a dedicated processing server.
- **Load**: Writing the transformed data into the destination Data Warehouse.

### ETL vs. ELT
With the rise of massively parallel cloud Data Warehouses (like Snowflake and BigQuery), the paradigm shifted to **ELT (Extract, Load, Transform)**.
- **Extract & Load**: Data is extracted and immediately loaded into the Data Warehouse in its raw format (often the Bronze layer).
- **Transform**: The transformation happens *inside* the Data Warehouse using SQL, leveraging the warehouse's massive compute power.

### Batch Processing vs. Stream Processing
- **Batch Processing**: Data is processed in large chunks at scheduled intervals (e.g., every night at 2 AM). Great for historical reporting. High latency.
- **Stream Processing**: Data is processed continuously as it arrives (e.g., Kafka). Required for real-time AI inference, like fraud detection. Low latency, higher complexity.

---

## 2. Architecture Diagram: ETL vs ELT

```mermaid
flowchart TD
    subgraph "Traditional ETL"
        E1[Extract from DB] --> T1[Transform Server\n(e.g., Informatica/Spark)]
        T1 --> L1[Load to Warehouse]
    end
    
    subgraph "Modern ELT"
        E2[Extract from DB] --> L2[Load to Warehouse\n(Raw/Bronze)]
        L2 --> T2[Transform INSIDE Warehouse\n(e.g., dbt / SQL)]
    end
```

---

## 3. Production Use Cases

1. **Nightly AI Retraining**: A batch ETL pipeline runs every midnight to extract the day's customer support tickets, transforms the text (removes HTML tags), and loads it into an S3 bucket to fine-tune an LLM overnight.
2. **Real-time Feature Generation**: An ELT pipeline loads raw clickstream data into Snowflake, where a dbt (Data Build Tool) job immediately transforms it to update a user's `recent_interest_category` for an AI recommendation engine.

---

## 4. Real Company Examples

- **Fivetran / Airbyte**: These companies built billion-dollar businesses simply by perfecting the "Extract and Load" (EL) part of ELT. They offer plug-and-play connectors to pull data from Salesforce and drop it into BigQuery.
- **dbt Labs**: Popularized the "T" in ELT. They provide a framework to write data transformations using pure SQL inside the Data Warehouse.

---

## 5. Coding Examples

### Conceptual Python ETL Script

```python
import pandas as pd
import sqlite3

def run_etl():
    # 1. EXTRACT: Read from a CSV (Source)
    raw_data = pd.read_csv('raw_users.csv')
    
    # 2. TRANSFORM: Clean data
    # Drop rows missing an email
    clean_data = raw_data.dropna(subset=['email'])
    # Standardize names to uppercase
    clean_data['name'] = clean_data['name'].str.upper()
    
    # 3. LOAD: Write to a SQLite DB (Destination)
    conn = sqlite3.connect('enterprise_warehouse.db')
    clean_data.to_sql('dim_users', conn, if_exists='append', index=False)
    
if __name__ == "__main__":
    run_etl()
```

---

## 6. Hands-on Labs

**Lab: Manual ETL**
**Objective**: Understand the pain of manual data transformation.
**Instructions**:
1. Create a `raw.csv` with columns `id`, `name`, `price`, `tax`. Add 3 rows, with one row missing a `tax` value, and one row having a negative `price`.
2. Write a Python script to extract this data, transform it (fill missing tax with 0.0, drop negative prices), and print the resulting JSON.

---

## 7. Assignments

**Assignment: ELT Trade-offs**
Write a short paragraph explaining why a company might choose ELT over ETL. What specific technological advancement in the last 10 years made ELT the industry standard for analytical workloads?

---

## 8. Interview Questions

1. **What is the primary difference between ETL and ELT?**
   *Answer Hint: In ETL, transformation happens on a separate compute engine before the data hits the warehouse. In ELT, raw data is loaded first, and the warehouse's own compute engine handles the transformation using SQL.*
2. **When would you use Batch processing over Stream processing?**
   *Answer Hint: Use batch when real-time latency is not required (e.g., monthly billing reports, nightly model retraining), as it is cheaper and less complex to maintain. Use streaming only when immediate action is required (e.g., fraud detection).*

---

## 9. Best Practices (FDE Standards)

- **Idempotency**: An ETL pipeline must be idempotent. If you run the pipeline for yesterday's data three times, the final result in the database should be exactly the same as if you ran it once. Do not blindly append data; use `UPSERT` or `MERGE`.
- **Fail Fast and Alert**: If the extraction phase fails (e.g., the source API is down), the pipeline should crash immediately and send a Slack alert, rather than loading partial/empty data into the warehouse.

---

## 10. Common Mistakes

- **Silent Failures**: The pipeline runs successfully, but the source data was empty, so you just loaded an empty table into production. Always implement row-count validation checks.
- **Hardcoding Credentials**: Writing database passwords directly in the ETL Python script instead of using a Secrets Manager or Environment Variables.

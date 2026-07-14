# Module 2.2: Data Extraction

Welcome to **Data Extraction**. The first step of any pipeline is getting the data out of the source system. As an AI FDE, you will extract data from ancient mainframes, modern SaaS APIs, and messy file systems. Doing this reliably without bringing down the source system is an art.

---

## 1. Detailed Theory

### Source Types
1. **Databases (Relational/NoSQL)**: Extracting directly from the client's production DB (Postgres, MongoDB, Oracle).
2. **APIs (REST/GraphQL)**: Pulling data from SaaS applications (Salesforce, Zendesk, Jira).
3. **Files**: Parsing CSV, JSON, XML, or Parquet files dropped in an FTP server or S3 bucket.
4. **Event Streams**: Consuming messages from Kafka or RabbitMQ.

### Extraction Strategies
- **Full Extract**: Pulling the entire dataset every time. Simple, but slow and resource-intensive. Only feasible for small tables (e.g., a `Country_Codes` table).
- **Incremental Extract**: Only pulling data that has changed since the last extraction. Requires a "High Water Mark" (e.g., `updated_at > last_run_time`).
- **Change Data Capture (CDC)**: The most advanced method. Instead of querying the database, CDC tools read the database's internal transaction logs (e.g., Postgres WAL) to stream every `INSERT`, `UPDATE`, and `DELETE` in real-time without adding load to the database.

### API Handling
When extracting from APIs, you must handle:
- **Pagination**: Looping through pages of results (Cursor-based or Offset-based).
- **Rate Limiting**: Implementing exponential backoff when the API responds with a `429 Too Many Requests`.
- **Authentication**: Managing OAuth tokens or API keys securely.

---

## 2. Architecture Diagram: Change Data Capture (CDC)

```mermaid
flowchart LR
    subgraph "Production Environment"
        App[Web Application] -->|Writes| DB[(PostgreSQL)]
        DB -.->|Transaction Logs (WAL)| Log[Write-Ahead Log]
    end
    
    subgraph "CDC Pipeline (e.g., Debezium)"
        Log -->|Reads Log| CDC[Debezium Connector]
        CDC -->|Streams Changes| Kafka[Kafka Topic]
    end
    
    Kafka -->|Consumes| Lakehouse[(Data Lakehouse)]
```

---

## 3. Production Use Cases

1. **LLM Knowledge Base Syncing**: A company uses Confluence for documentation. You write an extraction pipeline that hits the Confluence API every hour, pulls newly modified pages (Incremental Extract), and sends them to a RAG ingestion pipeline.
2. **Real-Time Fraud Detection**: You use Debezium (CDC) to read the transaction logs of the main payment database so your AI model can evaluate a transaction milliseconds after it occurs, without slowing down the payment database.

---

## 4. Real Company Examples

- **Airbyte / Fivetran**: These platforms provide pre-built extraction connectors. Instead of writing custom Python code to handle Salesforce API pagination and rate limits, you just configure Fivetran to extract it for you.
- **Stripe**: Provides robust webhook event streams, allowing data engineers to push data out in real-time rather than constantly polling the API for new payments.

---

## 5. Coding Examples

### Incremental API Extraction (Python)

```python
import requests
import time

def extract_tickets_incrementally(last_sync_timestamp):
    url = "https://api.zendesk.com/api/v2/tickets.json"
    params = {"start_time": last_sync_timestamp} # High Water Mark
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    all_tickets = []
    
    while url:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 429:
            print("Rate limited! Sleeping...")
            time.sleep(int(response.headers.get("Retry-After", 60)))
            continue
            
        data = response.json()
        all_tickets.extend(data["tickets"])
        
        # Handle Pagination
        url = data.get("next_page", None)
        params = None # URL already contains params on next_page
        
    return all_tickets
```

---

## 6. Hands-on Labs

**Lab: Handling Pagination**
**Objective**: Write a script to handle API pagination.
**Instructions**:
Use the public Pokemon API (`https://pokeapi.co/api/v2/pokemon?limit=100`). Write a Python script that loops through the `next` URL in the response payload until you have extracted the names of exactly 300 Pokémon.

---

## 7. Assignments

**Assignment: CDC vs. Polling**
You are deployed to a bank. They need their `Transactions` table synced to a Data Warehouse.
Write a brief technical proposal arguing why you should use Change Data Capture (reading the DB logs) instead of a python script that runs `SELECT * FROM transactions WHERE created_at > NOW() - 5 minutes` every 5 minutes.

---

## 8. Interview Questions

1. **What is a "High Water Mark" in incremental extraction?**
   *Answer Hint: A tracking mechanism (usually a timestamp or ID) that records the last successfully extracted record. The next pipeline run uses this mark to only pull data created/updated after that point.*
2. **What is Change Data Capture (CDC)?**
   *Answer Hint: CDC is a pattern that identifies and tracks changes (inserts, updates, deletes) in a database, typically by reading the internal transaction logs (like binlog or WAL), rather than executing SQL queries against the tables.*

---

## 9. Best Practices (FDE Standards)

- **Never `SELECT *` without limits on Production**: If you run a Full Extract query on a 500GB production table in the middle of the day, you will crash the client's application.
- **Respect Rate Limits**: Always implement exponential backoff and retry logic when extracting from third-party APIs to avoid being permanently banned/blocked.

---

## 10. Common Mistakes

- **Ignoring Deletes in Incremental Extracts**: If your high-water mark query is `SELECT * WHERE updated_at > X`, you will catch inserts and updates. But if a record is hard-deleted from the source, it won't have an `updated_at` timestamp. It simply vanishes. You will never extract that deletion, and your Data Warehouse will be out of sync. (CDC solves this).

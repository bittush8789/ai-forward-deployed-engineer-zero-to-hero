# Module 2.4: Data Loading

Welcome to **Data Loading**. The final step of the pipeline is writing the extracted and/or transformed data into the destination system (Data Warehouse, Data Lake, or Vector DB). How you load the data determines whether your pipeline is idempotent, reliable, and performant.

---

## 1. Detailed Theory

### Loading Strategies
- **Full Load (Truncate and Load)**: The destination table is completely emptied (truncated) and the new data is loaded from scratch. Simplest method, but slow and terrible for historical tracking.
- **Incremental Load (Append)**: Only new records are added to the table. Fast, but risks data duplication if the pipeline runs twice (not idempotent).
- **Upsert (Merge)**: "Update or Insert". If the record already exists (based on a primary key), update it. If it doesn't exist, insert it. This is the gold standard for idempotency.

### Slowly Changing Dimensions (SCD) Loading
As covered in Data Modeling, loading data into an SCD Type 2 table requires complex logic:
1. Identify if a record exists.
2. If it exists and data changed, update the old record to set `is_active = FALSE`.
3. Insert the new record with `is_active = TRUE`.

### Loading to Vector Databases
Loading for AI systems has specific challenges. When loading data into Pinecone or Milvus:
- You must batch your vector inserts (e.g., 100 vectors at a time) rather than inserting one by one to avoid rate limits and network latency.
- You must handle updates carefully. If a source document changes, you must delete its old vectors and insert the new ones, ensuring the metadata stays perfectly synced.

---

## 2. Architecture Diagram: The Upsert (Merge) Pattern

```mermaid
flowchart TD
    Source[New Incoming Data\n(Staging Table)] --> MergeLogic{Primary Key Exists\n in Target?}
    Target[(Target Table)]
    
    MergeLogic -- YES --> Update[UPDATE existing row\nwith new values]
    MergeLogic -- NO --> Insert[INSERT new row]
    
    Update --> Target
    Insert --> Target
```

---

## 3. Production Use Cases

1. **RAG Vector Syncing**: A nightly pipeline loads updated Confluence pages into a Vector DB. It uses an Upsert pattern: if the `chunk_id` exists in the Vector DB, update the embedding and text. If it doesn't, insert it.
2. **Sales Dashboard**: Loading daily transactional data into Snowflake using a `MERGE` statement to ensure that if a transaction's status changed from "Pending" to "Completed", the existing row is updated rather than duplicated.

---

## 4. Real Company Examples

- **Snowflake**: Provides highly optimized `COPY INTO` and `MERGE` commands designed to load terabytes of data from S3 buckets into their warehouse in seconds.
- **Pinecone / Weaviate**: Optimized vector databases that provide specialized bulk-load endpoints for inserting thousands of high-dimensional embeddings efficiently.

---

## 5. Coding Examples

### The SQL MERGE Statement (Upsert)

```sql
-- Merging new data from a staging table into the production table
MERGE INTO target_users AS t
USING staging_users AS s
ON t.user_id = s.user_id

-- If the user exists, update their email
WHEN MATCHED THEN
    UPDATE SET t.email = s.email, t.updated_at = CURRENT_TIMESTAMP

-- If the user does not exist, insert them
WHEN NOT MATCHED THEN
    INSERT (user_id, email, updated_at)
    VALUES (s.user_id, s.email, CURRENT_TIMESTAMP);
```

---

## 6. Hands-on Labs

**Lab: Idempotent Loading in Python**
**Objective**: Write an idempotent load function.
**Instructions**:
Given a Pandas DataFrame and a SQLAlchemy connection to a Postgres database, write a function that uses a primary key (`id`) to update existing rows and insert new ones (you can use Pandas `to_sql` combined with a temporary table and a SQL `ON CONFLICT` query).

---

## 7. Assignments

**Assignment: Full Load vs Incremental**
A client has a `Country_Codes` table (195 rows) that changes maybe once a decade. They also have a `Web_Clicks` table (10 million rows per day). Which loading strategy (Full Load vs Incremental/Upsert) would you use for each, and why?

---

## 8. Interview Questions

1. **What does it mean for an ETL pipeline to be "Idempotent"?**
   *Answer Hint: Running the pipeline multiple times with the same input yields the exact same final state in the database, without causing duplicate data or errors.*
2. **Explain how an UPSERT (or MERGE) works.**
   *Answer Hint: It uses a unique identifier (Primary Key) to check the target table. If a match is found, it updates the existing record. If no match is found, it inserts a new record. This ensures idempotency.*

---

## 9. Best Practices (FDE Standards)

- **Always Aim for Idempotency**: Never use a blind "Append" (`INSERT INTO`) without guaranteeing the source data is perfectly clean and the pipeline will never re-run. Default to `MERGE`/Upsert.
- **Batching**: When loading APIs or Vector DBs, batch your payloads. Sending 1,000 HTTP requests to load 1,000 rows will throttle your system. Sending 1 request with a payload of 1,000 rows is vastly more efficient.

---

## 10. Common Mistakes

- **Silent Duplication**: Running an "Append" pipeline that fails halfway through. The developer restarts the pipeline, and the first half of the data is loaded twice, doubling the client's revenue metrics on their dashboard.
- **Forgetting to Delete**: When syncing source data to a Vector DB, a document is deleted in the source. If the load pipeline only does Upserts, the vector is never deleted, leading to AI hallucinations based on deleted data. (You must implement a hard-delete sync mechanism).

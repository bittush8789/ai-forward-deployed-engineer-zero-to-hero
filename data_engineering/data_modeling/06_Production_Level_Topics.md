# Module 1.6: Production-Level Topics

Welcome to **Production-Level Topics in Data Modeling**. Moving from a Jupyter Notebook to an enterprise environment introduces strict requirements for security, scale, and compliance. As an AI FDE, your models must support multi-tenancy, survive massive traffic spikes, and comply with data privacy laws.

---

## 1. Detailed Theory

### Multi-Tenant Data Models
When building SaaS applications or B2B AI platforms, you must store data for multiple clients (tenants) in a single system without them seeing each other's data.
- **Siloed (Database per Tenant)**: Highest isolation. Every client gets their own database. Hard to scale and manage.
- **Pool (Row-Level Security)**: Lowest cost. All clients share the same tables. Every row requires a `tenant_id` column.

### Data Security & Privacy
- **Row-Level Security (RLS)**: A database feature that automatically filters query results based on the user executing the query (e.g., User A can only `SELECT` rows where `tenant_id = A`).
- **Data Masking**: Dynamically hiding sensitive information (like replacing a credit card with `XXXX-XXXX-XXXX-1234`) when queried by unauthorized roles.

### Scalability Strategies
- **Sharding (Horizontal Partitioning)**: Splitting a massive table across multiple physical database servers. (e.g., Users A-M on Server 1, Users N-Z on Server 2).
- **Partitioning Strategies**: Splitting data logically within the same server (e.g., by Date or by Region) to speed up queries.
- **High Availability (HA)**: Designing models with Primary-Replica architectures. Writes go to the Primary, reads go to Replicas (Read Replicas) to handle massive AI inference traffic.

### Data Governance
- **Data Catalogs**: Tools (like Alation or Amundsen) that serve as a search engine for your company's data. If you want to find the `churn_rate` feature, the catalog tells you exactly which table holds it and who owns it.
- **Data Quality Frameworks**: Automated tests that run against your data (e.g., checking if `age < 0` or if `email` is null).

---

## 2. Architecture Diagram: Multi-Tenant Pooling with RLS

```mermaid
flowchart TD
    App[AI SaaS Application] --> |Query: SELECT * FROM documents| Proxy[Connection Proxy\nInjects tenant_id=42]
    Proxy --> DB[(Enterprise Database)]
    
    subgraph "Database Table: Documents (Pooled)"
    Row1[Row 1 | tenant_id: 12 | Doc: 'Secret A']
    Row2[Row 2 | tenant_id: 42 | Doc: 'Public B']
    Row3[Row 3 | tenant_id: 42 | Doc: 'Private C']
    end
    
    DB --> |RLS enforces filter| Result[Result: Rows 2 & 3]
    Result --> App
```

---

## 3. Production Use Cases

1. **Healthcare AI Agent**: You are building an agent that summarizes patient records. Due to HIPAA, you must implement Data Masking on the database level so the agent never actually sees the patient's Social Security Number in the raw text.
2. **Global E-Commerce Scale**: Your recommendation engine reads from a database that gets 50,000 requests per second. You implement Sharding based on `continent_id` to distribute the load across 5 different database clusters.

---

## 4. Real Company Examples

- **Salesforce**: The ultimate master of the Multi-Tenant Pooled model. Millions of organizations share the same underlying massive Oracle/PostgreSQL databases, securely separated by strict `org_id` enforcement.
- **Instagram / Meta**: Extensive use of Sharding. User data is sharded across thousands of databases to handle global, billion-user scale.

---

## 5. Coding Examples

### Implementing Row-Level Security (PostgreSQL)

```sql
-- 1. Create a table with a tenant_id
CREATE TABLE chat_histories (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    chat_log TEXT
);

-- 2. Enable RLS on the table
ALTER TABLE chat_histories ENABLE ROW LEVEL SECURITY;

-- 3. Create a policy: Users can only select rows where tenant_id matches their session variable
CREATE POLICY tenant_isolation_policy ON chat_histories
    FOR SELECT
    USING (tenant_id = current_setting('app.current_tenant')::UUID);
```

---

## 6. Hands-on Labs

**Lab: Data Masking Strategy**
**Objective**: Identify PII (Personally Identifiable Information) that needs masking.
**Instructions**:
You have a table: `users(id, first_name, last_name, email, phone, medical_condition, signup_date)`. 
Identify which columns require strict Data Masking before this data is passed to a generic LLM for summary analysis, and write the pseudocode for how you would mask them.

---

## 7. Assignments

**Assignment: Sharding Architecture**
You are designing a database for a global IoT platform where millions of cars stream telemetry data. A single database is failing. Propose a Sharding Key (e.g., `car_id`, `region`, `timestamp`) and explain the pros and cons of your chosen key.

---

## 8. Interview Questions

1. **What is the difference between Sharding and Partitioning?**
   *Answer Hint: Partitioning splits data logically within the SAME database/server to improve query performance. Sharding splits data physically across MULTIPLE servers to distribute compute/storage load.*
2. **Explain the trade-offs between a Siloed vs. Pooled multi-tenant database design.**
   *Answer Hint: Siloed offers perfect security isolation but is expensive and hard to update (you have to update 1,000 databases for 1,000 clients). Pooled is cheap and easy to manage (one schema update), but requires rigorous software engineering (RLS) to prevent catastrophic data leaks.*

---

## 9. Best Practices (FDE Standards)

- **Default to Pooled Multi-Tenancy**: Unless a client strictly demands a dedicated database for compliance reasons (e.g., defense contractors), always build pooled models using `tenant_id` for easier scaling.
- **Always use RLS**: Do not rely solely on the application code (`WHERE tenant_id = x`) to filter data. A single bug in the Python code will leak data. Enforce it at the database level with RLS.

---

## 10. Common Mistakes

- **Choosing a Bad Sharding Key**: Sharding by `date`. If you shard by date, all today's traffic hits Server 1 (hotspot), while the other servers sit idle holding historical data.
- **Ignoring Data Governance**: Allowing data scientists to copy the production database to an unprotected S3 bucket to train a model, thereby bypassing all Data Masking and RLS policies.

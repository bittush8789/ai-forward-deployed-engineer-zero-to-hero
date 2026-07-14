# Module 2.3: Data Transformation

Welcome to **Data Transformation**. This is where the heavy lifting happens. Raw data is rarely usable for BI or AI. It must be cleaned, standardized, joined, and enriched. In the ELT paradigm, this happens inside the Data Warehouse using SQL (via tools like dbt). In traditional ETL or Big Data, it happens using distributed compute engines like Apache Spark.

---

## 1. Detailed Theory

### Core Transformation Types
- **Data Cleaning**: Handling NULL values, removing duplicates (Deduplication), and filtering out bad data (e.g., removing test accounts).
- **Data Standardization**: Enforcing consistent formats. (e.g., converting all text to lowercase, formatting dates to `YYYY-MM-DD`, standardizing currency to USD).
- **Data Enrichment**: Joining the primary dataset with external data to add context (e.g., joining an IP address to a Geo-IP database to add `Country` and `City` columns).
- **Business Rules Processing**: Applying complex logic (e.g., "If a user has logged in 5 times and spent $100, classify them as a 'Power User'").

### The Role of dbt (Data Build Tool)
dbt has revolutionized data transformation. It allows data analysts/engineers to write transformations as simple `SELECT` statements using SQL. 
- dbt handles the boilerplate (creating tables/views, managing dependencies).
- It introduces software engineering best practices (version control, automated testing, CI/CD) to SQL data pipelines.

---

## 2. Architecture Diagram: dbt Transformation Flow

```mermaid
flowchart LR
    subgraph "Data Warehouse (e.g., Snowflake)"
        Raw[(Bronze/Raw\nData)] -->|dbt run| Stg[Staging Views\n(Cleaned)]
        Stg -->|dbt run| Int[Intermediate Tables\n(Joined)]
        Int -->|dbt run| Mart[(Data Marts\nGold Layer)]
    end
    
    Git[GitHub Repos] -.->|CI/CD Deploys SQL| DW
```

---

## 3. Production Use Cases

1. **LLM Instruction Tuning Prep**: Transforming raw chat logs into a highly standardized JSONL format. You must filter out conversations that are too short, standardize the system prompt text, and ensure the `role` is strictly mapped to `user` or `assistant`.
2. **Customer 360 View**: An enterprise has a customer's billing data in Stripe and support data in Zendesk. A transformation pipeline joins these datasets on `email_address` to create a unified `dim_customer` table.

---

## 4. Real Company Examples

- **Spotify**: Performs massive daily transformations on listening data. Raw streams are enriched with song metadata, standardized into timezones, and aggregated into "Daily Top 50" charts.
- **dbt Labs**: As mentioned, they created the industry standard tool for SQL-based transformations, used by almost every modern data-driven company.

---

## 5. Coding Examples

### dbt Model (SQL + Jinja)

```sql
-- models/staging/stg_users.sql
-- This is a dbt model. It uses Jinja templating to reference other tables.

WITH raw_users AS (
    SELECT * FROM {{ source('raw_stripe', 'users') }}
)

SELECT 
    id AS user_id,
    LOWER(email) AS email_address,
    COALESCE(status, 'inactive') AS account_status, -- Handling NULLs
    CAST(created_at AS DATE) AS signup_date
FROM raw_users
WHERE is_deleted = FALSE -- Filtering
```

---

## 6. Hands-on Labs

**Lab: Data Cleaning with Pandas**
**Objective**: Clean a messy dataset.
**Instructions**:
Write a short Python Pandas script that takes a DataFrame with columns `['Name', 'Age', 'Email']`.
1. Fill any `NaN` ages with the median age.
2. Strip whitespace and lowercase all emails.
3. Drop rows where `Email` does not contain an `@` symbol.

---

## 7. Assignments

**Assignment: Business Logic Transformation**
You have an `Orders` table (`order_id`, `amount`, `status`). 
Write a SQL `CASE` statement that creates a new column called `order_category`:
- If amount > 1000 and status = 'completed', category is 'High Value'.
- If amount < 1000 and status = 'completed', category is 'Standard'.
- If status is 'failed', category is 'Failed'.

---

## 8. Interview Questions

1. **What is the difference between Data Cleaning and Data Enrichment?**
   *Answer Hint: Cleaning is fixing the existing data (removing nulls, standardizing formats). Enrichment is adding NEW data by joining the dataset with external sources (e.g., adding demographic data based on a zip code).*
2. **Why has dbt become so popular for data transformations?**
   *Answer Hint: It allows transformations to be written in plain SQL (accessible to analysts), while bringing software engineering best practices (version control, testing, modularity, DAG dependencies) to the warehouse.*

---

## 9. Best Practices (FDE Standards)

- **Modularity (DRY - Don't Repeat Yourself)**: Instead of writing a massive 500-line SQL query, break it into smaller, modular steps (Staging -> Intermediate -> Final).
- **Never Transform in the Extraction Script**: Do not perform complex joins or business logic in the Python script pulling from the API. Extract it raw, load it, and THEN transform it in the warehouse (ELT).

---

## 10. Common Mistakes

- **Assuming Data is Clean**: Assuming an `email` column from a source system won't have nulls or malformed strings. Always explicitly handle edge cases using `COALESCE` or strict filtering.
- **Hardcoding Transformation Logic**: Hardcoding an exchange rate (`amount * 1.15`) instead of joining to an `exchange_rates` dimension table that tracks historical rates.

# Module 1.3: Advanced SQL

Welcome to **Module 1.3**. Relational databases are powerful because data is spread across multiple tables to avoid redundancy. Advanced SQL is about putting that data back together efficiently, performing mathematical aggregations, and executing complex, multi-step queries seamlessly.

---

## 1. Detailed Theory

### Joins
Combine rows from two or more tables based on a related column.
- **INNER JOIN**: Returns records that have matching values in BOTH tables.
- **LEFT (OUTER) JOIN**: Returns ALL records from the left table, and matched records from the right table. If no match, NULLs are returned for right table columns.
- **RIGHT JOIN / FULL OUTER JOIN**: Less common, but returns all from right, or all from both.

### Aggregations and `GROUP BY`
Used for data analysis. Functions include `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()`. When you aggregate, you usually use `GROUP BY` to group the rows that have the same values in specified columns into summary rows.
- **`HAVING`**: The equivalent of `WHERE`, but used specifically *after* an aggregation.

### Subqueries and CTEs
- **Subquery**: A query nested inside another query (e.g., in a WHERE clause).
- **CTE (Common Table Expression)**: Defined using the `WITH` keyword. It acts as a temporary, readable virtual table that exists only for the duration of the query. Great for breaking complex logic into readable steps.

### Window Functions
Perform calculations across a set of table rows that are somehow related to the current row, but *unlike aggregations, they do not collapse the rows into a single output*. (e.g., `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at)`).

---

## 2. Architecture Diagram: The JOIN Concept

```mermaid
venn
    title SQL Joins
    "Table A (Users)" : [1, 2, 3, 4]
    "Table B (Orders)" : [3, 4, 5, 6]
    "INNER JOIN" : [3, 4]
    "LEFT JOIN" : [1, 2, 3, 4]
```

---

## 3. Production Use Cases

1. **Context Assembly (JOINs)**: Before passing data to an LLM, fetching a User's profile, their company details, and their active subscription status by joining the `users`, `companies`, and `subscriptions` tables in a single lightning-fast query.
2. **AI Cost Analysis (Aggregations)**: Using `GROUP BY user_id` and `SUM(tokens_used)` to build a dashboard showing which enterprise users are burning the most AI credits.
3. **Session Rebuilding (Window Functions)**: Numbering the messages within an agent chat session sequentially (1, 2, 3...) based on their timestamp, so the UI can render them in exact order.

---

## 4. Real Company Examples

- **Snowflake / BigQuery Workloads**: Data Scientists and Analytics Engineers write 500-line SQL queries using dozens of CTEs to aggregate trillions of rows of product telemetry data into clean "Features" to train Machine Learning models.
- **Uber**: Uses complex geospatial Window functions to calculate the moving average speed of drivers in specific grid sectors in real-time.

---

## 5. Coding Examples

### INNER JOIN
```sql
-- Fetch the prompt text AND the email of the user who sent it
SELECT 
    users.email, 
    agent_prompts.prompt_text 
FROM agent_prompts
INNER JOIN users 
    ON agent_prompts.user_id = users.id;
```

### Aggregation and GROUP BY
```sql
-- Find how many tokens each user has consumed in total, 
-- but ONLY show users who have used more than 50,000 tokens.
SELECT 
    user_id, 
    SUM(tokens_used) as total_tokens,
    COUNT(prompt_id) as prompt_count
FROM agent_prompts
GROUP BY user_id
HAVING SUM(tokens_used) > 50000 
ORDER BY total_tokens DESC;
```

### Common Table Expressions (CTEs)
```sql
-- 1. Create a temporary result set of "Power Users"
WITH PowerUsers AS (
    SELECT id, email 
    FROM users 
    WHERE plan_type = 'Enterprise'
)
-- 2. Join the temporary table with prompts
SELECT 
    p.email, 
    COUNT(a.prompt_id) as query_count
FROM PowerUsers p
LEFT JOIN agent_prompts a ON p.id = a.user_id
GROUP BY p.email;
```

---

## 6. Hands-on Labs

**Lab: The Orphan Finder**
**Objective**: Use a LEFT JOIN to find data anomalies.
**Instructions**:
You have `users` and `subscriptions`. Write a query using `LEFT JOIN` to find all users who DO NOT have an active subscription record.
*Hint: Select all from `users`, LEFT JOIN `subscriptions`, and filter `WHERE subscriptions.id IS NULL`.*

---

## 7. Assignments

**Assignment: AI Agent Leaderboard**
1. Assume `agents` (id, name) and `agent_executions` (id, agent_id, success_boolean).
2. Write a query that groups by `agent_id`.
3. Calculate the total executions (`COUNT`).
4. (Advanced): Calculate the success rate using conditional aggregation (e.g., `SUM(CASE WHEN success_boolean THEN 1 ELSE 0 END) / COUNT(*)`).

---

## 8. Interview Questions

1. **What is the difference between `WHERE` and `HAVING`?**
   *Answer Hint: `WHERE` filters rows BEFORE aggregation occurs. `HAVING` filters the results AFTER the `GROUP BY` aggregation has occurred.*
2. **When would you use a `LEFT JOIN` instead of an `INNER JOIN`?**
   *Answer Hint: Use `LEFT JOIN` when you want all records from the primary table, even if there is no matching relational data. (e.g., Get a list of ALL users and their latest AI prompt, returning NULL for the prompt column if they've never used the AI).*
3. **Why are CTEs (`WITH` clauses) preferred over nested Subqueries?**
   *Answer Hint: Readability. A nested subquery must be read from the inside out. A query with 3 CTEs can be read top-to-bottom sequentially, making it vastly easier to debug.*

---

## 9. Best Practices (FDE Standards)

- **Use Table Aliases**: When joining tables, always use aliases (`FROM users u INNER JOIN prompts p`) and explicitly prefix your selected columns (`u.email, p.text`). This prevents "Ambiguous Column Name" errors if both tables have an `id` or `created_at` column.
- **Avoid Joining on Non-Indexed Columns**: Joining two tables on a `VARCHAR` column (like an email string) is terribly slow. Always join on integer Primary/Foreign keys which are indexed by the database.

---

## 10. Common Mistakes

- **Cartesian Explosion**: Forgetting the `ON` clause in a Join (or writing it incorrectly). If you join a 100-row table with a 100-row table without an `ON` clause, you create a 10,000-row result set, instantly freezing your application.

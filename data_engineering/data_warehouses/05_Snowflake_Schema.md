# Module 7.5: Snowflake Schema

Welcome to the **Snowflake Schema**. The Snowflake Schema is a variation of the Star Schema where dimension tables are normalized, breaking down low-cardinality attributes into separate related tables. While it reduces data redundancy and saves storage space, it increases query complexity by requiring more JOIN operations.

---

## 1. Detailed Theory

### What is a Snowflake Schema?
A Snowflake Schema is a multi-dimensional database design where the central fact table is connected to normalized dimension tables. For example, instead of storing `City`, `State`, and `Country` directly in a single `dim_store` table, the store table points to a `dim_city` table, which points to a `dim_state` table, resembling the shape of a snowflake.

### Star vs. Snowflake Trade-offs
- **Storage Efficiency**: Snowflake is normalized (3NF-like for dimensions), eliminating redundant text storage. Star is denormalized, containing redundant text values. Historically, when storage was expensive, Snowflake was popular; today, with cheap cloud storage, Star is generally preferred.
- **Query Complexity & Speed**: Star schemas require simple, fast single-level joins. Snowflake schemas require nested, multi-level joins, increasing query execution time on large datasets.
- **Maintenance**: Snowflake schemas reduce the risk of update anomalies because text fields are updated in single lookup tables.

---

## 2. Architecture Diagram: Snowflake Schema Layout

```mermaid
flowchart TD
    subgraph "Snowflake Schema"
        Fact[FACT_SALES\n- date_key (FK)\n- product_key (FK)\n- store_key (FK)\n- revenue]
        
        DimProduct[DIM_PRODUCT\n- product_key (PK)\n- name\n- category_key (FK)]
        DimCategory[DIM_CATEGORY\n- category_key (PK)\n- category_name]
        
        DimStore[DIM_STORE\n- store_key (PK)\n- name\n- city_key (FK)]
        DimCity[DIM_CITY\n- city_key (PK)\n- city_name\n- state_key (FK)]
        DimState[DIM_STATE\n- state_key (PK)\n- state_name\n- country]
    end
    
    DimProduct <--> Fact
    DimStore <--> Fact
    DimCategory <--> DimProduct
    DimCity <--> DimStore
    DimState <--> DimCity
```

---

## 3. Production Use Cases

1. **Enterprise Data Warehouse**: A company with highly complex hierarchical dimensions (e.g., a corporate organizational structure with departments, sub-departments, units, and teams) uses a Snowflake schema to represent this deep relationship without duplicating department details across millions of rows.

---

## 4. Real Company Examples

- **SAP / Oracle Enterprise Systems**: Commonly output their transactional reports in Snowflake configurations due to the normalized nature of their core ERP software.

---

## 5. Coding Examples

### Querying a Snowflake Schema (Requires Nested Joins)

```sql
SELECT 
    p.name AS product_name,
    c.category_name,
    city.city_name,
    state.state_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_category c ON p.category_key = c.category_key -- Second level join
JOIN dim_store s ON f.store_key = s.store_key
JOIN dim_city city ON s.city_key = city.city_key       -- Second level join
JOIN dim_state state ON city.state_key = state.state_key -- Third level join
GROUP BY 1, 2, 3, 4
ORDER BY total_revenue DESC;
```

---

## 6. Hands-on Labs

**Lab: Converting Star to Snowflake**
**Objective**: Normalize a dimension table.
**Instructions**:
Given a flat dimension table `dim_product(product_key, product_name, category_name, department_name)`, write the SQL DDL statements to normalize this table into three separate Snowflake tables: `dim_product`, `dim_category`, and `dim_department`.

---

## 7. Assignments

**Assignment: Snowflake Join Analysis**
Review the SQL query in Section 5. Write a short explanation of how the five-way join path affects the execution plan of a database query engine compared to a simple three-way join in a Star Schema. How does column-oriented storage handle these nested joins?

---

## 8. Interview Questions

1. **What is the difference between a Star Schema and a Snowflake Schema?**
   *Answer Hint: In a Star Schema, dimension tables are denormalized (flat). In a Snowflake Schema, dimension tables are normalized into multiple related lookup tables to reduce redundancy, requiring more joins to query.*
2. **Under what scenario would you choose a Snowflake Schema?**
   *Answer Hint: When the dimension tables contain massive hierarchies (e.g., geographical zones or corporate structures) where storage efficiency is important, or when the source data naturally evolves in normalized formats.*

---

## 9. Best Practices (FDE Standards)

- **Avoid Over-Snowflaking**: Do not normalize dimensions unless the hierarchy is extremely deep or storage size is a critical constraint. Flat tables are always faster to read.
- **Document the Join Paths**: If a Snowflake schema is required, clearly document the join paths (foreign key mappings) in the schema metadata catalog to assist analytics users.

---

## 10. Common Mistakes

- **Assuming Snowflake is always faster**: Choosing Snowflake assuming it will run faster because tables are smaller. In modern column-oriented databases, the join overhead of Snowflake usually makes it slower than Star.
- **Broken Referential Integrity**: Failing to enforce foreign key constraints between the normalized dimension tables, leading to orphaned categories or cities.

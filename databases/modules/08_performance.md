# 08 Performance Engineering

## Theory & Architecture (Ubuntu Setup)
- **Installation**: No extra services required; install profiling tools.
  ```bash
  sudo apt-get update && sudo apt-get install -y python3-pip postgresql-client mysql-client mongodb-org-tools redis-tools
  pip3 install psycopg2-binary mysql-connector-python pymongo redis
  ```
- **Key Concepts**: 
  - **EXPLAIN / EXPLAIN ANALYZE** for query plans.
  - **Query optimization**: index selection, join re‑ordering, materialized views.
  - **Caching** layers (Redis, application‑level caches).
  - **Connection pooling** impact on latency.
  - **Benchmarking** with `pgbench`, `sysbench`, `redis-benchmark`.

## Production Internals
- **PostgreSQL**: `pg_stat_statements` extension for per‑query stats.
- **MySQL**: `performance_schema` for low‑overhead instrumentation.
- **MongoDB**: `mongotop` and `mongostat` for I/O.
- **Redis**: `INFO` command; latency monitor.

## Business Use Cases
- Detect slow queries in an AI inference logging DB.
- Optimize read‑heavy LLM metadata look‑ups.
- Reduce latency for real‑time recommendation engines.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import subprocess, json, time

# Helper to run a shell command and capture output
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Example: PostgreSQL EXPLAIN ANALYZE
print('--- PostgreSQL EXPLAIN ANALYZE ---')
explain_pg = run_cmd("psql -d postgres -c \"EXPLAIN ANALYZE SELECT COUNT(*) FROM pg_class;\"")
print(explain_pg)

# Example: MySQL performance_schema query
print('\n--- MySQL Statement Digest ---')
explain_mysql = run_cmd("mysql -e \"SELECT digest_text, sum_timer_wait/1000000000 as seconds FROM performance_schema.events_statements_summary_by_digest ORDER BY sum_timer_wait DESC LIMIT 5;\"")
print(explain_mysql)

# Example: Redis latency monitor (short run)
print('\n--- Redis Latency ---')
latency = run_cmd('redis-cli --latency-history 5')
print(latency)

# Example: MongoDB aggregation explain
print('\n--- MongoDB Explain ---')
explain_mongo = run_cmd("mongo --quiet --eval 'db.test.explain().aggregate([{$match:{}}])'")
print(explain_mongo)
```
Save as `performance_demo.py` in `databases/projects/` and run `python3 performance_demo.py`.

## Interview Questions
- How do you identify and address a query that triggers a sequential scan?
- What is the impact of **implicit type casting** on index usage?
- Explain the difference between **cold cache** and **warm cache** performance.

## AI FDE Perspective
Performance metrics feed back into the UI via a dashboard, allowing front‑end engineers to spot latency spikes and adjust caching strategies.

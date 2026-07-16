# 01 PostgreSQL

## Theory & Architecture (Ubuntu Setup)
- **Installation**: `sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib`
- **Service Management**: `sudo systemctl enable postgresql && sudo systemctl start postgresql`
- **Architecture**: PostgreSQL follows a **process‑per‑connection** model with a **shared‑buffer cache**, **WAL** for durability, and **MVCC** for ACID compliance.
- **Key Components**: `postmaster`, `bgwriter`, `walwriter`, `autovacuum`.

## Production Internals
- **Connection Pooling** with **PgBouncer**: `sudo apt-get install -y pgbouncer`; configure `/etc/pgbouncer/pgbouncer.ini` and enable the service.
- **Read Replicas** via **Streaming Replication** – primary writes WAL, replicas replay.
- **Backup & Recovery**: `pg_basebackup -D /var/lib/postgresql/12/main -Fp -Xs -P -R -h <primary-host>`.

## Business Use Cases
- Metadata store for LLMs (model versions, experiment logs).
- Transactional user data for SaaS platforms.
- Audit logs with immutable append‑only tables.

## Schema Design Example
```sql
CREATE TABLE ai_models (
    model_id   UUID PRIMARY KEY,
    name       TEXT NOT NULL,
    version    TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE model_metrics (
    metric_id  UUID PRIMARY KEY,
    model_id   UUID REFERENCES ai_models(model_id),
    metric_key TEXT NOT NULL,
    value      NUMERIC,
    ts         TIMESTAMPTZ DEFAULT now()
);
```

## Query Design & Optimization
- Use **GIN indexes** for JSONB columns, **BRIN** for time‑series.
```sql
CREATE INDEX idx_metrics_ts ON model_metrics USING BRIN (ts);
CREATE INDEX idx_metrics_json ON model_metrics USING GIN (to_jsonb(metric_key));
```
- **EXPLAIN ANALYZE** to inspect query plans.

## Performance Tuning (Ubuntu)
```bash
# Increase shared_buffers (25% of RAM)
sudo -u postgres psql -c "ALTER SYSTEM SET shared_buffers = '4GB';"
# Enable effective_cache_size
sudo -u postgres psql -c "ALTER SYSTEM SET effective_cache_size = '12GB';"
# Restart PostgreSQL
sudo systemctl restart postgresql
```

## Scalability Patterns
- **Partitioning** (range on `ts`):
```sql
CREATE TABLE model_metrics_2023 PARTITION OF model_metrics FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
```
- **Logical Replication** for selective table sync.

## Security Considerations
- Enable **SSL** in `postgresql.conf` (`ssl = on`).
- Use **scram‑sha‑256** authentication (`password_encryption = scram-sha-256`).
- **Row‑level security** (RLS) for tenant isolation.

## Monitoring Strategy
- **pg_stat_statements** extension for query stats.
- **Prometheus exporter**: `postgres_exporter` Docker container.
- Set up alerts for replication lag, connection count.

## Hands‑On Lab (Ubuntu)
1. Install PostgreSQL and PgBouncer.
2. Create the `ai_models` and `model_metrics` tables.
3. Insert 1 M synthetic rows using Python script (see below).
4. Run `EXPLAIN ANALYZE` on a sample aggregation query.
5. Set up a streaming replica on a second VM.

## Real Production Incident
*Incident*: Replica lag exceeded 30 seconds after a heavy bulk load. *Resolution*: Throttled `COPY` rate, increased `wal_sender_timeout`, and tuned `max_wal_size`.

## Interview Questions
- How does MVCC work in PostgreSQL?
- Explain the difference between physical and logical replication.
- What is a GIN index and when would you use it?

## Enterprise Case Study
**Company X** used PostgreSQL to store LLM experiment metadata, achieving sub‑millisecond query latency by partitioning on `created_at` and using columnar storage via **cstore_fdw**.

## AI FDE Perspective
Front‑end services consume model metadata via a **typed REST API** backed by PostgreSQL. Engineers must ensure low‑latency reads (use read‑replicas) and safe updates (optimistic concurrency with `xmin`).

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import os
import psycopg2
import uuid
from datetime import datetime, timezone

# Connection via Unix socket
conn = psycopg2.connect(dbname="postgres", user=os.getenv("USER"))
cur = conn.cursor()

# Insert synthetic model and metrics
model_id = uuid.uuid4()
cur.execute(
    "INSERT INTO ai_models (model_id, name, version) VALUES (%s, %s, %s)",
    (model_id, "gpt‑x", "v1.2"),
)

metrics = [(uuid.uuid4(), model_id, f"metric_{i}", i * 0.1, datetime.now(timezone.utc)) for i in range(1000)]
args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s)", row) for row in metrics)
cur.execute(b"INSERT INTO model_metrics (metric_id, model_id, metric_key, value, ts) VALUES " + args_str)
conn.commit()
print("Inserted sample data.")
cur.close()
conn.close()
```
Save as `insert_demo.py` and run `python3 insert_demo.py`.

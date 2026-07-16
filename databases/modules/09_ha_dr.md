# 09 HA & DR

## Theory & Architecture (Ubuntu Setup)
- **Installation**: Install the required services for HA setups.
  ```bash
  sudo apt-get update && sudo apt-get install -y postgresql mysql-server mongodb-org redis-server
  # For Docker-based setups (Elasticsearch, Neo4j)
  sudo apt-get install -y docker.io
  ```
- **Key Concepts**:
  - **Streaming Replication** for PostgreSQL.
  - **Asynchronous/Semi‑synchronous Replication** for MySQL.
  - **Replica Sets** for MongoDB.
  - **Redis Sentinel** for automatic failover.
  - **Elasticsearch Cluster** health and shard allocation.
  - **Neo4j Causal Clustering** (core members, read replicas).

## Production Internals
- **PostgreSQL**: `pg_basebackup` for base backups, `pg_receivewal` for continuous archiving.
- **MySQL**: `mysqldump` for logical backups, `xtrabackup` for hot physical backups.
- **MongoDB**: `mongodump`/`mongorestore` and `oplog` tailing.
- **Redis**: RDB snapshots (`SAVE`) and AOF (`appendonly yes`). Sentinel configuration for failover.
- **Elasticsearch**: Snapshot/restore APIs to S3 or filesystem.
- **Neo4j**: `neo4j-admin backup` for online backups.

## Business Use Cases
- Disaster‑recovery for AI experiment metadata.
- High‑availability services for LLM serving platforms.
- Multi‑region replication for global AI SaaS.

## Hands‑On Lab (Ubuntu)
1. Set up a **PostgreSQL streaming replica** on a second VM.
2. Configure a **MySQL asynchronous replica**.
3. Deploy a **MongoDB replica set** with three nodes.
4. Enable **Redis Sentinel** with a master and two replicas.
5. Take a **snapshot of an Elasticsearch index** and restore it.
6. Run the Python script `ha_dr_demo.py` to verify connectivity and failover.

## Real Production Incident
*Incident*: PostgreSQL replica fell behind after a network glitch, causing replication lag > 60 s.
*Resolution*: Adjusted `wal_sender_timeout`, increased `max_wal_size`, and enabled `hot_standby_feedback` on the replica.

## Interview Questions
- How does **WAL archiving** enable point‑in‑time recovery?
- What are the differences between **synchronous** and **asynchronous** replication in MySQL?
- Explain **Redis Sentinel**'s leader election process.
- How does **Elasticsearch snapshot lifecycle** work?

## AI FDE Perspective
Front‑end services rely on a **read‑through cache** that automatically switches to replica endpoints after failover, ensuring uninterrupted UI experiences.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import subprocess, time, os

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

# Check PostgreSQL replica status
print('--- PostgreSQL Replica Status ---')
pg_status = run_cmd("psql -d postgres -c \"SELECT client_addr, state, sync_state FROM pg_stat_replication;\"")
print(pg_status)

# Check MySQL replica status
print('\n--- MySQL Replica Status ---')
mysql_status = run_cmd("mysql -e 'SHOW SLAVE STATUS\G'")
print(mysql_status)

# Check MongoDB replica set status
print('\n--- MongoDB Replica Set Status ---')
mongo_status = run_cmd("mongo --quiet --eval 'rs.status()'")
print(mongo_status)

# Check Redis Sentinel status
print('\n--- Redis Sentinel Info ---')
redis_info = run_cmd("redis-cli -p 26379 sentinel masters")
print(redis_info)

# Elasticsearch snapshot test (requires ES container running)
print('\n--- Elasticsearch Snapshot ---')
# Create a repository (local filesystem) and snapshot
run_cmd("curl -XPUT 'http://localhost:9200/_snapshot/local?verify=true' -H 'Content-Type: application/json' -d '{\"type\": \"fs\", \"settings\": {\"location\": \"/tmp/es_snapshots\"}}'")
run_cmd("curl -XPUT 'http://localhost:9200/_snapshot/local/snap_1?wait_for_completion=true' -H 'Content-Type: application/json' -d '{}' ")
print('Snapshot created.')
```
Save as `ha_dr_demo.py` in `databases/projects/` and run `python3 ha_dr_demo.py`.

# 04 Redis

## Theory & Architecture (Ubuntu Setup)
- **Installation**: `sudo apt-get update && sudo apt-get install -y redis-server`.
- **Service Management**: `sudo systemctl enable redis-server && sudo systemctl start redis-server`.
- **Architecture**: Redis is an **in‑memory key‑value store** using a **single‑threaded event loop**. It supports various data structures (strings, hashes, lists, sets, sorted sets, streams) and persistence via RDB snapshots and AOF logs.
- **Key Components**: `redis-server`, `redis-cli`, persistence modules (RDB, AOF), replication masters/slaves.

## Production Internals
- **Connection Pooling** handled by client libraries; Python example uses `redis.ConnectionPool`.
- **Replication**: Master‑slave asynchronous replication; enable in `redis.conf` with `replicaof <master-ip> <port>`.
- **Persistence**: Configure `save` intervals for RDB snapshots and `appendonly yes` for AOF.
- **Backup & Recovery**: Copy RDB/AOF files; use `redis-cli --rdb` for export.

## Business Use Cases
- Session store for web applications.
- Caching layer for AI inference results.
- Rate‑limiting and distributed locks for microservices.

## Schema Design Example
```redis
# Store model metadata as a hash
HMSET model:1 name "gpt‑x" version "v1.0" created_at 1660000000

# Store recent scores in a sorted set (timestamp → score)
ZADD model_scores:1 1660000100 0.95
ZADD model_scores:1 1660000200 0.96
```

## Query Design & Optimization
- Use **TTL** (`EXPIRE`) to auto‑expire cache entries.
- Leverage **Lua scripts** for atomic operations.
```lua
-- Lua script for atomic increment-if-exists
local val = redis.call('GET', KEYS[1])
if val then
  return redis.call('INCRBY', KEYS[1], ARGV[1])
end
return nil
```

## Performance Tuning (Ubuntu)
```bash
# Increase maxmemory (e.g., 4GB) in /etc/redis/redis.conf
sudo sed -i "s/^# maxmemory <bytes>/maxmemory 4gb/" /etc/redis/redis.conf
# Enable lazy freeing
sudo sed -i "s/^# lazyfree-lazy-eviction no/lazyfree-lazy-eviction yes/" /etc/redis/redis.conf
sudo systemctl restart redis-server
```

## Scalability Patterns
- **Redis Cluster** for horizontal sharding across multiple nodes.
- **Read Replicas** for scaling reads.
- **Sentinel** for automatic failover.

## Security Considerations
- Bind to localhost or use firewall rules (`bind 127.0.0.1`).
- Enable **TLS** (`tls-port 6379`, `tls-cert-file`, `tls-key-file`).
- Use **ACLs** to restrict commands per user.

## Monitoring Strategy
- **INFO** command for metrics.
- **Redis Exporter** for Prometheus.
- Alerts for memory usage and eviction rates.

## Hands‑On Lab (Ubuntu)
1. Install Redis and configure persistence (`appendonly yes`).
2. Run the `redis_demo.py` script to store and retrieve model metadata and scores.
3. Set a TTL on a cache key and observe expiration.
4. Enable a replica on a second VM and verify data sync.

## Real Production Incident
*Incident*: Cache stampede caused massive DB load after a cache miss. *Resolution*: Implemented a Lua‑based lock with `SETNX` and exponential backoff.

## Interview Questions
- How does Redis achieve high performance with a single‑threaded model?
- Explain the difference between **RDB** and **AOF** persistence.
- What is Redis Sentinel and when would you use it?

## Enterprise Case Study
**MediaCo** uses Redis Cluster to cache AI‑generated video thumbnails, achieving 99.9 % cache hit rate and reducing backend load by 70 %.

## AI FDE Perspective
Front‑end components fetch cached inference results via a lightweight HTTP endpoint backed by Redis. Engineers must ensure cache invalidation on model updates.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import redis
import os
from uuid import uuid4
from time import sleep

# Connect to local Redis instance
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
client = redis.Redis(connection_pool=pool)

# Store model metadata as a hash
model_id = str(uuid4())
client.hset(f"model:{model_id}", mapping={
    "name": "gpt-x",
    "version": "v1.0",
    "created_at": "1660000000"
})
print(f"Stored model metadata for {model_id}")

# Store a score in a sorted set
client.zadd(f"model_scores:{model_id}", {"0.95": 1660000100})
print("Added initial score.")

# Demonstrate TTL
client.setex("temp_key", 10, "temporary value")
print("Set temp_key with 10‑second TTL.")
print("Current TTL:", client.ttl("temp_key"))

# Lua script for atomic increment
lua_script = """
local val = redis.call('GET', KEYS[1])
if val then
  return redis.call('INCRBY', KEYS[1], ARGV[1])
end
return nil
"""
increment = client.register_script(lua_script)
client.set("counter", 0)
new_val = increment(keys=["counter"], args=[5])
print("Counter after atomic increment:", new_val)
```
Save as `redis_demo.py` in `databases/projects/` and run `python3 redis_demo.py`.

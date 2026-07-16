# Redis Practice Tasks

## Step‑by‑Step Lab

1. **Install Redis**
   ```bash
   sudo apt-get update && sudo apt-get install -y redis-server
   sudo systemctl enable redis-server && sudo systemctl start redis-server
   ```
2. **Verify the service**
   ```bash
   redis-cli ping
   # Expected output: PONG
   ```
3. **Create a simple key‑value store**
   ```bash
   redis-cli SET model:1 "gpt‑x"
   redis-cli GET model:1
   ```
4. **Use a hash to store model metadata**
   ```bash
   redis-cli HSET model:1 name "gpt‑x" version "v1.0" created_at 1660000000
   redis-cli HGETALL model:1
   ```
5. **Create a sorted set for scoring**
   ```bash
   redis-cli ZADD model_scores:1 1660000100 0.95
   redis-cli ZADD model_scores:1 1660000200 0.96
   redis-cli ZRANGE model_scores:1 0 -1 WITHSCORES
   ```
6. **Set a TTL on a cache key**
   ```bash
   redis-cli SETEX temporary_key 10 "temp_value"
   redis-cli TTL temporary_key
   ```
7. **Run the Python lab script**
   ```bash
   python3 ../projects/redis_demo.py
   ```
8. **Enable persistence** – edit `/etc/redis/redis.conf`:
   ```
   save 900 1   # snapshot every 15 minutes if at least 1 key changed
   appendonly yes
   ```
   Restart the service and verify persistence by checking the RDB file.
9. **Configure a replica (optional)** – follow module 09 HA & DR for Sentinel.
10. **Cleanup** – delete test keys with `redis-cli DEL model:1 model_scores:1 temporary_key`.

---

[Run the full lab script](../projects/redis_demo.py) for quick verification.

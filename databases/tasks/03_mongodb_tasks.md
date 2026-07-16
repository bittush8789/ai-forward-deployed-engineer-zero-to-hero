# MongoDB Practice Tasks

## Step‑by‑Step Lab

1. **Install MongoDB**
   ```bash
   sudo apt-get update && sudo apt-get install -y mongodb-org
   sudo systemctl enable mongod && sudo systemctl start mongod
   ```
2. **Create a database and collection**
   ```bash
   mongo --quiet <<'EOF'
   use ai_platform;
   db.createCollection('model_metrics');
   EOF
   ```
3. **Insert a sample document manually**
   ```bash
   mongo ai_platform --eval "db.model_metrics.insertOne({\
       metric_id: UUID(),\
       model_id: UUID(),\
       metric_key: 'accuracy',\
       value: 0.94,\
       ts: new Date()\
   })"
   ```
4. **Bulk insert synthetic data with Python**
   ```bash
   python3 ../projects/mongodb_demo.py
   ```
5. **Create an index for fast look‑ups**
   ```bash
   mongo ai_platform --eval "db.model_metrics.createIndex({model_id:1, metric_key:1})"
   ```
6. **Run an aggregation query**
   ```bash
   mongo ai_platform --eval "printjson(db.model_metrics.aggregate([{$match:{metric_key:'accuracy'}},{$group:{_id:'$model_id', avgVal:{$avg:'$value'}}}]).toArray())"
   ```
7. **Set up a replica set (optional)** – follow module 09 HA & DR.
8. **Backup the database**
   ```bash
   mongodump --db ai_platform --out /tmp/mongo_backup
   ```
9. **Enable TLS** – edit `/etc/mongod.conf` (`net.tls.mode: requireTLS`) and restart.
10. **Cleanup** – drop collection or database if desired.

---

[Run the full lab script](../projects/mongodb_demo.py) for quick verification.

# PostgreSQL Practice Tasks

## Step‑by‑Step Lab

1. **Install PostgreSQL**
   ```bash
   sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib
   sudo systemctl enable postgresql && sudo systemctl start postgresql
   ```
2. **Create a new role and database**
   ```bash
   sudo -u postgres createuser myuser --createdb
   sudo -u postgres createdb mydb -O myuser
   ```
3. **Connect and create tables**
   ```bash
   psql -U myuser -d mydb -c "\
   CREATE TABLE ai_models (\n       model_id UUID PRIMARY KEY,\n       name TEXT NOT NULL,\n       version TEXT NOT NULL,\n       created_at TIMESTAMPTZ DEFAULT now()\n   );\
   CREATE TABLE model_metrics (\n       metric_id UUID PRIMARY KEY,\n       model_id UUID REFERENCES ai_models(model_id),\n       metric_key TEXT NOT NULL,\n       value NUMERIC,\n       ts TIMESTAMPTZ DEFAULT now()\n   );"
   ```
4. **Insert synthetic data using the provided Python script**
   ```bash
   python3 ../projects/insert_demo.py
   ```
5. **Run an aggregation query and examine the plan**
   ```sql
   EXPLAIN ANALYZE SELECT model_id, AVG(value) FROM model_metrics GROUP BY model_id;
   ```
6. **Create indexes for performance**
   ```sql
   CREATE INDEX idx_metrics_ts ON model_metrics USING BRIN (ts);
   CREATE INDEX idx_metrics_json ON model_metrics USING GIN (to_jsonb(metric_key));
   ```
7. **Set up streaming replication (optional)** – follow the steps in module 09 HA & DR.
8. **Backup the database**
   ```bash
   pg_basebackup -D /tmp/pg_backup -Fp -Xs -P -R -h localhost
   ```
9. **Verify security settings** – enable SSL in `postgresql.conf` and test connection with `psql "sslmode=require"`.
10. **Cleanup** – drop the test database and role.

---

[Run the full lab script](../projects/insert_demo.py) for quick verification.

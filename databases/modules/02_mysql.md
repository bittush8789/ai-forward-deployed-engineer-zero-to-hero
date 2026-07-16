# 02 MySQL

## Theory & Architecture (Ubuntu Setup)
- **Installation**: `sudo apt-get update && sudo apt-get install -y mysql-server`.
- **Service Management**: `sudo systemctl enable mysql && sudo systemctl start mysql`.
- **Architecture**: MySQL uses a **single‑process + thread pool** model. The InnoDB storage engine provides **ACID** compliance, MVCC, and crash‑recovery via redo logs.
- **Key Components**: `mysqld`, `mysqlrouter`, `InnoDB` buffer pool, `binary log`.

## Production Internals
- **Connection Pooling** via **ProxySQL** or **MySQL Router**. Example install: `sudo apt-get install -y proxysql`.
- **Read Replicas** – set up asynchronous replication (`CHANGE MASTER TO`, `START SLAVE`).
- **Backup & Recovery** – `mysqldump` for logical backups, `xtrabackup` for hot physical backups.

## Business Use Cases
- Transactional order data for e‑commerce.
- User profile storage for SaaS platforms.
- Session store for web applications.

## Schema Design Example
```sql
CREATE TABLE customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE orders (
    order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT,
    amount DECIMAL(10,2),
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;
```

## Query Design & Optimization
- Use **composite indexes** for frequent filters:
```sql
CREATE INDEX idx_orders_customer_date ON orders (customer_id, ordered_at);
```
- **EXPLAIN** to analyze query plans.

## Performance Tuning (Ubuntu)
```bash
# Increase innodb_buffer_pool_size (e.g., 2G)
sudo sed -i "s/^#innodb_buffer_pool_size.*/innodb_buffer_pool_size=2G/" /etc/mysql/mysql.conf.d/mysqld.cnf
# Enable the query cache (if using MySQL 5.7)
sudo sed -i "s/^#query_cache_type.*/query_cache_type=ON/" /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
```

## Scalability Patterns
- **Sharding** using **MySQL Fabric** or **Vitess** for horizontal scaling.
- **Logical Replication** for selective table sync.

## Security Considerations
- Enforce **SSL/TLS** (`require_secure_transport=ON`).
- Use **caching_sha2_password** authentication.
- Apply **Row‑Level Security** via views or application logic.

## Monitoring Strategy
- **Performance Schema** for detailed metrics.
- **Prometheus MySQL exporter** (`mysqld_exporter`).
- Alerts for slow queries and replication lag.

## Hands‑On Lab (Ubuntu)
1. Install MySQL and ProxySQL.
2. Create `customers` and `orders` tables.
3. Insert 500k synthetic rows using the Python script `mysql_demo.py` (see project folder).
4. Run `EXPLAIN` on a join query.
5. Set up a replica on a second VM and verify replication.

## Real Production Incident
*Incident*: Replication stopped after a large `LOAD DATA` operation. *Resolution*: Increased `max_allowed_packet`, applied `GTID` mode, and restarted the replica.

## Interview Questions
- Explain the difference between **InnoDB** and **MyISAM**.
- How does MySQL’s binary log support point‑in‑time recovery?
- What is a **deadlock** and how can it be mitigated?

## Enterprise Case Study
**FinTech Co.** migrated to MySQL 8.0, using ProxySQL for connection pooling and Percona XtraBackup for zero‑downtime backups, achieving 99.99 % uptime.

## AI FDE Perspective
Front‑end services query MySQL via a **REST API** that caches frequent reads in Redis. Ensure low latency by routing reads to replicas and using optimistic locking for updates.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import os
import mysql.connector
from uuid import uuid4

# Connect using Unix socket (default on Ubuntu)
conn = mysql.connector.connect(user='root', unix_socket='/var/run/mysqld/mysqld.sock')
cur = conn.cursor()

# Create synthetic data
cur.execute("INSERT INTO customers (name, email) VALUES ('Alice', 'alice@example.com')")
customer_id = cur.lastrowid

# Bulk insert orders
orders = [(customer_id, i * 10.5) for i in range(1000)]
cur.executemany("INSERT INTO orders (customer_id, amount) VALUES (%s, %s)", orders)
conn.commit()
print('Inserted sample data into MySQL.')
cur.close()
conn.close()
```
Save as `mysql_demo.py` in `databases/projects/` and run `python3 mysql_demo.py`.

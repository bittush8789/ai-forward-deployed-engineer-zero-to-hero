# MySQL Practice Tasks

## Step‑by‑Step Lab

1. **Install MySQL**
   ```bash
   sudo apt-get update && sudo apt-get install -y mysql-server
   sudo systemctl enable mysql && sudo systemctl start mysql
   ```
2. **Secure the installation** (set root password, remove test DB, etc.)
   ```bash
   sudo mysql_secure_installation
   ```
3. **Create a new user and database**
   ```sql
   CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'StrongPass!123';
   CREATE DATABASE mydb;
   GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';
   FLUSH PRIVILEGES;
   ```
4. **Create tables**
   ```sql
   USE mydb;
   CREATE TABLE customers (
       customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   CREATE TABLE orders (
       order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
       customer_id BIGINT,
       amount DECIMAL(10,2),
       ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
   );
   ```
5. **Insert synthetic data with Python**
   ```bash
   python3 ../projects/mysql_demo.py
   ```
6. **Run an EXPLAIN on a join query**
   ```sql
   EXPLAIN ANALYZE SELECT c.name, SUM(o.amount) FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name;
   ```
7. **Create an index for query performance**
   ```sql
   CREATE INDEX idx_orders_customer_date ON orders (customer_id, ordered_at);
   ```
8. **Set up a replica (optional)** – follow the steps in module 09 HA & DR.
9. **Backup using mysqldump**
   ```bash
   mysqldump -u myuser -p mydb > /tmp/mydb_backup.sql
   ```
10. **Enable TLS** – edit `/etc/mysql/mysql.conf.d/mysqld.cnf` (`require_secure_transport=ON`) and restart.

---

[Run the full lab script](../projects/mysql_demo.py) for quick verification.

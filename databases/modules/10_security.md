# 10 Security

## Theory & Architecture (Ubuntu Setup)
- **Installation**: Install each DB with packages that support TLS/SSL.
  ```bash
  sudo apt-get update && sudo apt-get install -y \
    postgresql postgresql-contrib \
    mysql-server \
    mongodb-org \
    redis-server \
    docker.io   # for Elasticsearch & Neo4j
  ```
- **TLS/SSL Enablement**:
  - **PostgreSQL** – edit `/etc/postgresql/*/main/postgresql.conf`:
    ```
    ssl = on
    ssl_cert_file = '/etc/ssl/certs/pg_cert.pem'
    ssl_key_file = '/etc/ssl/private/pg_key.pem'
    ```
    Generate self‑signed certs (`openssl req -newkey rsa:4096 -nodes -keyout pg_key.pem -x509 -days 365 -out pg_cert.pem`).
  - **MySQL** – set `require_secure_transport = ON` in `mysqld.cnf` and point to cert/key.
  - **MongoDB** – enable TLS in `/etc/mongod.conf` (`net.tls.mode: requireTLS`).
  - **Redis** – configure `tls-port 6379`, `tls-cert-file`, `tls-key-file` in `redis.conf`.
  - **Elasticsearch** – set `xpack.security.enabled: true` and configure `http.ssl.enabled: true` with keystore.
  - **Neo4j** – `dbms.connector.bolt.tls_level=REQUIRED` and provide certificates.

## Production Internals
- **Authentication Methods**:
  - PostgreSQL – `scram-sha-256` passwords, `peer` auth for local users.
  - MySQL – `caching_sha2_password` (default), IAM authentication (optional).
  - MongoDB – `SCRAM-SHA-256` and X.509 client certificates.
  - Redis – ACLs (user/command restrictions) plus TLS.
- **Authorization** – Role‑Based Access Control (RBAC) in MySQL, PostgreSQL `pg_roles`, MongoDB `roles`, Elasticsearch RBAC via built‑in roles, Neo4j `dbms.security.auth_enabled`.
- **Audit Logging** – enable `log_line_prefix` in PostgreSQL, `audit_log` plugin for MySQL, MongoDB auditLog, Redis `logfile`, Elasticsearch audit logs.

## Business Use Cases
- Protecting proprietary LLM model metadata.
- Compliance (PCI‑DSS, GDPR) for customer data.
- Secure multi‑tenant SaaS platforms.

## Hands‑On Lab (Ubuntu)
1. Generate a self‑signed CA and server certificates.
2. Enable TLS for PostgreSQL and verify connection with `psql "sslmode=require"`.
3. Enable TLS for MySQL and connect via `mysql --ssl-mode=REQUIRED`.
4. Enable TLS for Redis and connect with `redis-cli --tls`.
5. Run the Python script `ssl_connection_demo.py` to programmatically test secure connections to PostgreSQL and Redis.

## Real Production Incident
*Incident*: Misconfigured TLS cert chain caused client connection failures after a certificate rotation. *Resolution*: Implemented automated cert renewal with `certbot` and added health‑check scripts to validate TLS handshakes.

## Interview Questions
- How does **TLS termination** differ between a reverse proxy and the database server itself?
- What is **client certificate authentication** and when would you use it?
- Explain **row‑level security (RLS)** in PostgreSQL and its benefits.
- How would you audit privileged SQL statements in MySQL?

## AI FDE Perspective
Front‑end services connect through a gateway that enforces TLS and validates JWT tokens. Secure connections ensure that AI model predictions and user data are protected end‑to‑end.

## Practical Code (Python on Ubuntu)
```python
#!/usr/bin/env python3
import psycopg2
import redis
import os

# PostgreSQL SSL connection
pg_conn = psycopg2.connect(
    dbname='postgres',
    user=os.getenv('USER'),
    host='localhost',
    port=5432,
    sslmode='require',
    sslrootcert='/etc/ssl/certs/ca.pem',
    sslcert='/etc/ssl/certs/pg_cert.pem',
    sslkey='/etc/ssl/private/pg_key.pem'
)
pg_cur = pg_conn.cursor()
pg_cur.execute('SELECT version();')
print('PostgreSQL version (SSL):', pg_cur.fetchone())
pg_cur.close()
pg_conn.close()

# Redis TLS connection
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    ssl=True,
    ssl_certfile='/etc/ssl/certs/redis_cert.pem',
    ssl_keyfile='/etc/ssl/private/redis_key.pem',
    ssl_ca_certs='/etc/ssl/certs/ca.pem'
)
redis_client.set('secure_key', 'secure_value')
print('Redis TLS GET:', redis_client.get('secure_key'))
```
Save as `ssl_connection_demo.py` in `databases/projects/` and run `python3 ssl_connection_demo.py`.

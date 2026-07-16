# MySQL 연습 과제 (Korean)

## 단계별 실습

1. **MySQL 설치**
   ```bash
   sudo apt-get update && sudo apt-get install -y mysql-server
   sudo systemctl enable mysql && sudo systemctl start mysql
   ```
2. **보안 설정** (`mysql_secure_installation` 실행) - 루트 비밀번호 설정, 테스트 DB 삭제 등.
3. **새 사용자와 데이터베이스 생성**
   ```sql
   CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'StrongPass!123';
   CREATE DATABASE mydb;
   GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';
   FLUSH PRIVILEGES;
   ```
4. **테이블 생성**
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
5. **Python 스크립트로 샘플 데이터 삽입**
   ```bash
   python3 ../projects/mysql_demo.py
   ```
6. **조인 쿼리 실행 및 실행 계획 확인**
   ```sql
   EXPLAIN ANALYZE SELECT c.name, SUM(o.amount) FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name;
   ```
7. **인덱스 생성**
   ```sql
   CREATE INDEX idx_orders_customer_date ON orders (customer_id, ordered_at);
   ```
8. **레플리카 설정 (선택)** – 09 HA & DR 모듈 참고.
9. **mysqldump 로 백업**
   ```bash
   mysqldump -u myuser -p mydb > /tmp/mydb_backup.sql
   ```
10. **TLS 활성화** – `/etc/mysql/mysql.conf.d/mysqld.cnf`에 `require_secure_transport=ON` 추가 후 재시작.
11. **정리** – 테스트 DB와 사용자 삭제.

---

[전체 실습 스크립트 실행](../projects/mysql_demo.py)으로 빠르게 검증 가능합니다.

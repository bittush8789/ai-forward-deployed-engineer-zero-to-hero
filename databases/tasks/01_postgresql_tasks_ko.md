# PostgreSQL 연습 과제 (Korean)

## 단계별 실습

1. **PostgreSQL 설치**
   ```bash
   sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib
   sudo systemctl enable postgresql && sudo systemctl start postgresql
   ```
2. **새 역할과 데이터베이스 생성**
   ```bash
   sudo -u postgres createuser myuser --createdb
   sudo -u postgres createdb mydb -O myuser
   ```
3. **연결 후 테이블 생성**
   ```bash
   psql -U myuser -d mydb -c "\
   CREATE TABLE ai_models (\n       model_id UUID PRIMARY KEY,\n       name TEXT NOT NULL,\n       version TEXT NOT NULL,\n       created_at TIMESTAMPTZ DEFAULT now()\n   );\
   CREATE TABLE model_metrics (\n       metric_id UUID PRIMARY KEY,\n       model_id UUID REFERENCES ai_models(model_id),\n       metric_key TEXT NOT NULL,\n       value NUMERIC,\n       ts TIMESTAMPTZ DEFAULT now()\n   );"
   ```
4. **제공된 Python 스크립트로 샘플 데이터 삽입**
   ```bash
   python3 ../projects/insert_demo.py
   ```
5. **집계 쿼리 실행 및 실행 계획 확인**
   ```sql
   EXPLAIN ANALYZE SELECT model_id, AVG(value) FROM model_metrics GROUP BY model_id;
   ```
6. **성능을 위한 인덱스 생성**
   ```sql
   CREATE INDEX idx_metrics_ts ON model_metrics USING BRIN (ts);
   CREATE INDEX idx_metrics_json ON model_metrics USING GIN (to_jsonb(metric_key));
   ```
7. **스트리밍 복제 설정 (선택)** – 09 HA & DR 모듈을 참고.
8. **데이터베이스 백업**
   ```bash
   pg_basebackup -D /tmp/pg_backup -Fp -Xs -P -R -h localhost
   ```
9. **보안 설정 검증** – `postgresql.conf`에서 SSL을 활성화하고 `psql "sslmode=require"` 로 연결 테스트.
10. **정리** – 테스트 데이터베이스와 역할을 삭제.

---

[전체 실습 스크립트 실행](../projects/insert_demo.py)으로 빠르게 검증할 수 있습니다.

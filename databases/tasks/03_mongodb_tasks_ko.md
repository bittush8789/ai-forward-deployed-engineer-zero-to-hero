# MongoDB 연습 과제 (Korean)

## 단계별 실습

1. **MongoDB 설치**
   ```bash
   sudo apt-get update && sudo apt-get install -y mongodb-org
   sudo systemctl enable mongod && sudo systemctl start mongod
   ```
2. **데이터베이스와 컬렉션 만들기**
   ```bash
   mongo --quiet <<'EOF'
   use ai_platform;
   db.createCollection('model_metrics');
   EOF
   ```
3. **샘플 문서 수동 삽입**
   ```bash
   mongo ai_platform --eval "db.model_metrics.insertOne({\
       metric_id: UUID(),\
       model_id: UUID(),\
       metric_key: 'accuracy',\
       value: 0.94,\
       ts: new Date()\
   })"
   ```
4. **Python 스크립트로 대량 삽입**
   ```bash
   python3 ../projects/mongodb_demo.py
   ```
5. **인덱스 생성**
   ```bash
   mongo ai_platform --eval "db.model_metrics.createIndex({model_id:1, metric_key:1})"
   ```
6. **집계 쿼리 실행**
   ```bash
   mongo ai_platform --eval "printjson(db.model_metrics.aggregate([{$match:{metric_key:'accuracy'}},{$group:{_id:'$model_id', avgVal:{$avg:'$value'}}}]).toArray())"
   ```
7. **레플리카 셋 설정 (선택)** – 09 HA & DR 모듈 참고.
8. **백업**
   ```bash
   mongodump --db ai_platform --out /tmp/mongo_backup
   ```
9. **TLS 활성화** – `/etc/mongod.conf`에 `net.tls.mode: requireTLS` 추가 후 재시작.
10. **정리** – 컬렉션 또는 데이터베이스 삭제.

---

[전체 실습 스크립트 실행](../projects/mongodb_demo.py)으로 빠르게 검증 가능합니다.

# Redis 연습 과제 (Korean)

## 단계별 실습

1. **Redis 설치**
   ```bash
   sudo apt-get update && sudo apt-get install -y redis-server
   sudo systemctl enable redis-server && sudo systemctl start redis-server
   ```
2. **서비스 확인**
   ```bash
   redis-cli ping
   # 예상 출력: PONG
   ```
3. **키‑값 저장**
   ```bash
   redis-cli SET model:1 "gpt‑x"
   redis-cli GET model:1
   ```
4. **해시를 이용한 메타데이터 저장**
   ```bash
   redis-cli HSET model:1 name "gpt‑x" version "v1.0" created_at 1660000000
   redis-cli HGETALL model:1
   ```
5. **정렬된 집합으로 점수 저장**
   ```bash
   redis-cli ZADD model_scores:1 1660000100 0.95
   redis-cli ZADD model_scores:1 1660000200 0.96
   redis-cli ZRANGE model_scores:1 0 -1 WITHSCORES
   ```
6. **TTL 설정**
   ```bash
   redis-cli SETEX temporary_key 10 "temp_value"
   redis-cli TTL temporary_key
   ```
7. **Python 실습 스크립트 실행**
   ```bash
   python3 ../projects/redis_demo.py
   ```
8. **지속성 활성화** – `/etc/redis/redis.conf` 편집:
   ```
   save 900 1   # 15분마다 1개 이상의 키가 변했을 때 스냅샷
   appendonly yes
   ```
   서비스 재시작 후 RDB 파일을 확인해 영속성을 검증합니다.
9. **레플리카 구성 (선택)** – 09 HA & DR 모듈에 있는 Redis Sentinel 설정을 참고.
10. **정리** – 테스트 키 삭제:
    ```bash
    redis-cli DEL model:1 model_scores:1 temporary_key
    ```

---

[전체 실습 스크립트 실행](../projects/redis_demo.py)으로 빠르게 검증 가능합니다.

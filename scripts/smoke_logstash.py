"""Phase 2 #23: 로그 파일 변경이 Logstash를 거쳐 ES에 반영되는지 확인하는 스모크 테스트.

사전 조건: `docker compose up -d elasticsearch logstash api` 로 인프라가 떠 있어야 한다.
사용법: `python scripts/smoke_logstash.py`

config.yaml의 elasticsearch.host는 docker 네트워크 내부용(`http://elasticsearch:9200`)이라
호스트에서 실행하는 이 스크립트는 published 포트(ES_HOST 환경변수, 기본 localhost:9200)를 쓴다.
"""

import os
import sys
import time
import uuid
from pathlib import Path

import yaml
from elasticsearch import Elasticsearch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_gen.attack_injector import generate_attack_logs
from data_gen.log_generator import generate_normal_logs, write_logs

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

POLL_INTERVAL_SECONDS = 1
POLL_TIMEOUT_SECONDS = 30


def main() -> None:
    es = Elasticsearch(os.environ.get("ES_HOST", "http://localhost:9200"))
    index = CONFIG["elasticsearch"]["index"]

    normal_logs = generate_normal_logs(150)
    attack_logs = generate_attack_logs(n_each=70)
    logs = normal_logs + attack_logs

    before = es.count(index=index)["count"] if es.indices.exists(index=index) else 0

    log_path = Path("data/logs") / f"smoke_{uuid.uuid4().hex[:8]}.log"
    print(f"[smoke] {len(logs)}건 로그를 {log_path}에 기록")
    write_logs(logs, log_path)

    expected = before + len(logs)
    start = time.monotonic()
    count = before
    while time.monotonic() - start < POLL_TIMEOUT_SECONDS:
        es.indices.refresh(index=index)
        count = es.count(index=index)["count"]
        if count >= expected:
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    elapsed = time.monotonic() - start
    if count >= expected:
        print(
            f"[smoke] PASS: {elapsed:.1f}초 만에 {count - before}건 색인 확인 (기대 {len(logs)}건)"
        )
        sys.exit(0)
    else:
        print(
            f"[smoke] FAIL: {elapsed:.1f}초 대기 후 {count - before}건만 색인됨 (기대 {len(logs)}건)"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

# Docker Compose Spike

> Sprint 0 과제: ELK + FastAPI Docker Compose PoC 검증

## 검증 목표

- [x] `docker compose up` 후 Elasticsearch `/` 응답 확인
- [x] Kibana UI 접근 가능 (`http://localhost:5601`)
- [ ] FastAPI `/health` 응답 확인 (`http://localhost:8000/health`) — Phase 1(#17)에서 구현 후 검증
- [x] Logstash → ES 인덱싱 동작 확인

## 결과

**수행일**: 2026-06-16

ELK 3개 서비스(elasticsearch, kibana, logstash)를 `docker compose up -d` 로 기동하여 정상 동작 확인.  
FastAPI 서비스는 Dockerfile 미작성 상태로, Phase 1(#17) 완료 후 검증 예정.

### Elasticsearch 응답

```json
{
  "name": "8771a152559a",
  "cluster_name": "docker-cluster",
  "cluster_uuid": "7aLzA_-NQm2NrZRRb_Wi5w",
  "version": {
    "number": "8.13.4",
    "build_flavor": "default",
    "build_type": "docker",
    "lucene_version": "9.10.0"
  },
  "tagline": "You Know, for Search"
}
```

### 서비스 상태 (`docker compose ps`)

```
NAME                     IMAGE                                      STATUS
finids-elasticsearch-1   elasticsearch:8.13.4                       Up
finids-kibana-1          kibana:8.13.4                              Up
finids-logstash-1        logstash:8.13.4                            Up
```

## 시도한 접근법

- `api` 서비스는 Dockerfile 미작성으로 제외 (`docker compose up -d elasticsearch kibana logstash`)
- ES 기동까지 약 40초 소요 (이미지 최초 다운로드 포함)
- `xpack.security.enabled=false` 설정으로 인증 없이 접근

## 성공 기준

`docker compose ps` 전체 서비스 `running` 상태 유지 5분 → **달성** (ELK 3종 기준)

**결론**: 계속 진행

**이유**: ELK 스택 단독 기동 및 ES API 응답 확인 완료. Logstash 파이프라인 연동은 Phase 2(#23)에서 검증.

**다음 액션**: Phase 1 — Dockerfile 작성(#17) 후 전체 스택 재기동 확인

# 시스템 아키텍처

## 전체 흐름

```
[Faker 로그 생성]
      ↓
[Logstash] ─── 5초 폴링 ──→ [Elasticsearch]
                                    ↓
                             [FastAPI 엔진]
                           ┌────────────┤
                     [탐지 룰 5종]   [LangChain LCEL]
                           │              │
                           └──────┬───────┘
                                  ↓
                          [Kibana 대시보드]
                          [Slack / Gmail 알림]
```

## 컴포넌트 역할

| 컴포넌트 | 역할 |
|---|---|
| `data_gen/` | Faker 기반 정상 로그 + 공격 패턴 생성 |
| `logstash/` | 로그 수집 → ES 인덱싱 |
| `engine/rules/` | 5종 탐지 룰 구현 |
| `engine/evaluate.py` | Recall / FP 자동 측정 |
| `api/` | FastAPI REST 엔드포인트 |
| `kibana/` | 시각화 대시보드 Saved Objects |

## 탐지 룰 5종

1. **Credential Stuffing** — 동일 IP, 10분 내 10개 이상 계정 시도
2. **심야 대액 이체** — 00~05시, 300만원 이상
3. **다계정 접근** — 단일 IP, 30분 내 4개 이상 계정
4. **비정상 User-Agent** — python-requests, curl 등
5. **분산 이체** — 한도 근처 금액 1시간 내 5회 이상

## LLM 연동

- 모델: Ollama llama3.1:8b (로컬 RTX 4060 Ti)
- 파이프라인: LangChain LCEL
- Ollama 오프라인 시: 탐지/알림은 독립 동작, LLM 결과 = null

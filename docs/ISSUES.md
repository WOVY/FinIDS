# FinIDS GitHub Issues 목록

GitHub에 이슈를 생성할 때 이 파일을 참고한다.  
이슈 생성 후 각 행의 `#번호` 칸을 채워두면 커밋 메시지(`Closes #3`)와 연결된다.

---

## 라벨 정의

GitHub Labels 탭에서 먼저 생성한다.

| 라벨 | 색상 | 용도 |
|------|------|------|
| `infra` | `#0075ca` | Docker, ELK, Logstash, config |
| `data` | `#2ea44f` | 로그 생성기, 데이터 파이프라인 |
| `rules` | `#e11d48` | 탐지 룰셋 엔진 |
| `llm` | `#8250df` | LangChain, Ollama, 프롬프트 |
| `api` | `#f97316` | FastAPI 엔드포인트 |
| `test` | `#eab308` | TDD, pytest, mock |
| `dashboard` | `#06b6d4` | Kibana 시각화 |
| `alerting` | `#ec4899` | Slack Webhook 알림 |
| `docs` | `#6b7280` | README, 보고서, 제출 서류 |
| `spike` | `#374151` | PoC — 최대 2일, 결과 문서화 |
| `ci` | `#1d4ed8` | GitHub Actions 워크플로우 |
| `setup` | `#d1d5db` | 초기 환경 세팅 |

---

## 마일스톤 정의

| 마일스톤 | 기간 | Due Date |
|---------|------|----------|
| Sprint 0 | 6/16~6/30 | 2026-06-30 |
| Phase 1 | ~7/13 | 2026-07-13 |
| Phase 2 | 7/14~7/20 | 2026-07-20 |
| Phase 3 | 7/21~7/31 | 2026-07-31 |
| Phase 4 | 8/1~8/10 | 2026-08-10 |
| Phase 5 | 8/11~8/20 | 2026-08-20 |
| Phase 6 | 8/21~8/27 | 2026-08-27 |

---

## Sprint 0 — 사전 준비 (6/16~6/30)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #2 | [Sprint 0] 디렉터리 구조 초기화 및 빈 파일 배치 | `setup` | Sprint 0 |
| #3 | [Sprint 0] Python venv + requirements.txt 초안 작성 | `setup` | Sprint 0 |
| #4 | [Sprint 0] MIT LICENSE 파일 생성 | `docs` | Sprint 0 |
| #5 | [Sprint 0] 스파이크: Docker Compose ELK 단독 실행 확인 | `spike`, `infra` | Sprint 0 |
| #6 | [Sprint 0] 스파이크: Ollama llama3.1:8b 응답 속도 측정 | `spike`, `llm` | Sprint 0 |
| #7 | [Sprint 0] AI_MODEL_INFO.md 초안 작성 (Llama 3.1 라이선스 확인) | `docs` | Sprint 0 |
| #8 | [Sprint 0] evaluate.py 뼈대 + test_evaluate.py TDD 작성 | `test` | Sprint 0 |
| #9 | [Sprint 0] conftest.py 뼈대 작성 (sample_logs, mock_slack 픽스처) | `test` | Sprint 0 |
| #10 | [Sprint 0] pyproject.toml 생성 (ruff 컨벤션 + pytest 경로 설정) | `setup`, `ci` | Sprint 0 |
| #11 | [Sprint 0] .pre-commit-config.yaml 생성 및 pre-commit install | `setup`, `ci` | Sprint 0 |
| #12 | [Sprint 0] requirements-dev.txt 생성 (ruff, pytest, httpx, pre-commit) | `setup` | Sprint 0 |
| #13 | [Sprint 0] .coderabbit.yaml 생성 + CodeRabbit GitHub App 설치 | `ci` | Sprint 0 |
| #55 | [Sprint 0] GitHub Actions CI 워크플로우 작성 및 검증 | `ci` | Sprint 0 |

---

## Phase 1 — 인프라 구성 (~7/13)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #14 | [Phase 1] docker-compose.yml: ES + Logstash + Kibana + FastAPI 구성 | `infra` | Phase 1 |
| #15 | [Phase 1] logstash/pipeline.conf 작성 (파일 → ES, polling 5s) | `infra` | Phase 1 |
| #16 | [Phase 1] ES 인덱스 매핑 정의 (finids-logs) | `infra` | Phase 1 |
| #17 | [Phase 1] FastAPI main.py + /health 엔드포인트 구현 | `api` | Phase 1 |
| #18 | [Phase 1] test_api.py: /health TDD (HTTP 200 검증) | `test`, `api` | Phase 1 |
| #19 | [Phase 1] config.yaml 스키마 확정 (탐지 임계값 필드 구조) | `infra` | Phase 1 |

---

## Phase 2 — 데이터 파이프라인 (7/14~7/20)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #20 | [Phase 2] test_data_gen.py: 생성 로그 필드·타입 검증 TDD | `test`, `data` | Phase 2 |
| #21 | [Phase 2] log_generator.py: Faker 정상 금융 웹로그 생성 (label=normal) | `data` | Phase 2 |
| #22 | [Phase 2] attack_injector.py: 5종 공격 패턴 로그 생성 (label=attack) | `data` | Phase 2 |
| #23 | [Phase 2] Logstash 연동 스모크 테스트 (로그 변경 → 5초 내 ES 반영) | `infra`, `data` | Phase 2 |

---

## Phase 3 — 탐지 룰셋 + 측정 (7/21~7/31)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #24 | [Phase 3] test_rules.py: 룰 5종 실패 테스트 먼저 작성 | `test`, `rules` | Phase 3 |
| #25 | [Phase 3] base.py: Rule 추상 클래스 구현 (detect → List[Alert]) | `rules` | Phase 3 |
| #26 | [Phase 3] credential_stuffing.py: 동일 IP 10분 내 10계정 탐지 | `rules` | Phase 3 |
| #27 | [Phase 3] night_transfer.py: 00:00~05:00 300만원 이상 이체 탐지 | `rules` | Phase 3 |
| #28 | [Phase 3] multi_account.py: 단일 IP 30분 내 4계정 이상 탐지 | `rules` | Phase 3 |
| #29 | [Phase 3] abnormal_ua.py: 자동화 스크립트 UA 탐지 | `rules` | Phase 3 |
| #30 | [Phase 3] split_transfer.py: 1시간 내 한도 직전 금액 5회 반복 탐지 | `rules` | Phase 3 |
| #31 | [Phase 3] evaluate.py 완성: Recall·FP율 자동 계산 및 출력 | `test` | Phase 3 |
| #32 | [Phase 3] config.yaml 탐지 임계값 전부 외부화 | `rules`, `infra` | Phase 3 |

---

## Phase 4 — LLM 분석 연동 (8/1~8/10)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #33 | [Phase 4] test_chain.py: Ollama mock TDD (정상 응답 + 오프라인 케이스) | `test`, `llm` | Phase 4 |
| #34 | [Phase 4] chain.py: LangChain LCEL 체인 구현 (탐지 이벤트 → 리포트) | `llm` | Phase 4 |
| #35 | [Phase 4] prompts.py: 한국어 위협 분석 프롬프트 작성 | `llm` | Phase 4 |
| #36 | [Phase 4] Ollama 장애 처리: 타임아웃 30초 + null 저장 | `llm` | Phase 4 |
| #37 | [Phase 4] FastAPI LLM 분석 비동기 연동 | `api`, `llm` | Phase 4 |

---

## Phase 5 — 대시보드 & 알림 (8/11~8/20)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #38 | [Phase 5] slack.py: Slack Webhook 알림 구현 | `alerting` | Phase 5 |
| #39 | [Phase 5] email.py: Gmail SMTP 이메일 알림 구현 (smtplib 내장, 앱 비밀번호 인증) | `alerting` | Phase 5 |
| #40 | [Phase 5] test_alerting.py: Slack Webhook·Gmail SMTP mock 테스트 작성 | `test`, `alerting` | Phase 5 |
| #41 | [Phase 5] Kibana 대시보드 구성 (위험도별 시각화) | `dashboard` | Phase 5 |
| #42 | [Phase 5] Kibana Saved Objects JSON export + docker compose 자동 로드 | `dashboard`, `infra` | Phase 5 |

---

## Phase 6 — 출품 준비 (8/21~8/27)

| # | 제목 | 라벨 | 마일스톤 |
|---|------|------|---------|
| #43 | [Phase 6] README.md 완성 (설치·실행 가이드, 라이선스 명시) | `docs` | Phase 6 |
| #44 | [Phase 6] AI_MODEL_INFO.md 완성 | `docs` | Phase 6 |
| #45 | [Phase 6] 결과보고서 작성 | `docs` | Phase 6 |
| #46 | [Phase 6] 시연영상 촬영 (3분 이내) | `docs` | Phase 6 |
| #47 | [Phase 6] GitHub 저장소 Public 전환 | `docs` | Phase 6 |
| #48 | [Phase 6] 제출 체크리스트 최종 확인 | `docs` | Phase 6 |

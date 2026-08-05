# FinIDS

금융감독원·금융보안원 FDS(이상금융거래탐지시스템) 운영 가이드라인 기반 룰셋 + LangChain LCEL + Ollama(로컬 LLM)로 준실시간 금융 이상거래를 탐지하고 한국어 위협 분석 리포트를 자동 생성하는 개인 학습 프로젝트입니다.

> 이 저장소는 대회 출품용이 아닌, 개인 학습·역량 확장을 목적으로 만들었습니다.

## 주요 기능

- Faker 기반 정상/공격 로그 생성기 (`data_gen/`)
- FDS 가이드라인 기반 탐지 룰 5종 (`engine/rules/`): 크리덴셜 스터핑, 새벽 고액 이체, 다중 계정 접근, 비정상 User-Agent, 분할 이체
- LangChain LCEL + Ollama(llama3.1:8b)로 탐지 이벤트에 대한 한국어 위협 분석 리포트 자동 생성 (`engine/chain.py`)
- Slack Webhook·Gmail SMTP 알림 (`engine/alerting/`)
- Elasticsearch + Kibana 기반 로그 파이프라인·대시보드
- `evaluate.py`로 Recall·FP율을 재현 가능하게 측정 — 목표 수치를 미리 정하지 않고 측정 방법론 자체를 공개

## 기술 스택

- Backend: FastAPI
- 로그 파이프라인: Logstash → Elasticsearch
- AI: LangChain LCEL + Ollama llama3.1:8b (로컬 실행, 외부 전송 없음)
- 대시보드: Kibana
- 배포: Docker Compose

## 빠른 시작

```bash
git clone <repo-url>
cd FinIDS
docker compose up -d
```

기동 후 확인:

- API 문서: http://localhost:8000/docs
- Kibana: http://localhost:5601
- Elasticsearch: http://localhost:9200

로그 생성 및 색인 확인:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash 기준
pip install -r requirements-dev.txt
python -m data_gen.log_generator
python -m data_gen.attack_injector
```

탐지 룰 성능 측정:

```bash
python -m engine.evaluate
```

## 테스트

```bash
pytest
```

## 라이선스

MIT License.

사용한 주요 오픈소스 라이브러리: FastAPI(MIT), LangChain(MIT), Elasticsearch-py(Apache 2.0), Faker(MIT). Elasticsearch·Kibana·Logstash는 Elastic License 2.0을 따릅니다. Llama 3.1 모델 라이선스와 AI 보조 도구 사용 명시는 [AI_MODEL_INFO.md](./AI_MODEL_INFO.md)를 참고하세요.

## 알려진 한계

- `evaluate.py`의 Recall/FP율은 자체 생성 데이터(Faker) 기준 측정치이며, 탐지 룰과 공격 로그를 같은 설계자가 만들었기 때문에 그 자체로 성능을 증명하지 않습니다. 재현 가능한 측정 스크립트를 공개하는 것이 목적입니다.
- Slack/Gmail 알림과 LLM 위협 분석은 실제 자격증명·로컬 Ollama 서버가 있어야 동작하며, 이 저장소에는 포함돼 있지 않습니다.

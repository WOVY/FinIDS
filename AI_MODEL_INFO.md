# AI Model Information

본 프로젝트(FinIDS)에서 사용하는 AI 모델 정보를 2026 오픈소스 개발자대회 규정 제9조⑤에 따라 공개한다.

---

## 사용 모델

| 항목 | 내용 |
|------|------|
| 모델명 | Meta-Llama-3.1-8B |
| 모델 ID | `meta-llama/Meta-Llama-3.1-8B-Instruct` |
| 제공처 | Meta AI |
| 실행 환경 | Ollama (로컬 추론, 인터넷 미전송) |
| Ollama 버전 | 0.9.x (고정 권장: `ollama --version`으로 확인) |

---

## 라이선스

**Meta Llama 3.1 Community License Agreement**

- 원문: https://llama.meta.com/llama3_1/license/
- 비상업적 연구·교육 목적 사용 허용
- **상업적 이용**: 월간 활성 사용자(MAU) 7억 명 미만이면 허용 (본 프로젝트 해당)
- **저작자 표시**: 파생 작업물에 "Built with Meta Llama 3.1" 명시 필요 (README에 기재)
- **금지 사항**: Meta의 허가 없이 다른 AI 모델 학습에 사용 불가, Meta 제품·서비스 흉내 불가

---

## FinIDS 내 사용 목적 및 범위

| 항목 | 내용 |
|------|------|
| 사용 목적 | 탐지된 금융 이상거래 이벤트에 대한 한국어 위협 분석 리포트 자동 생성 |
| 입력 | 탐지 룰 발동 이벤트 (IP, 시간, 금액, User-Agent 등) |
| 출력 | 위협 원인 추정·시나리오·대응 방안 (한국어 자연어) |
| 실행 방식 | 로컬 Ollama 서버 호출 (외부 API 미사용, 데이터 외부 전송 없음) |
| 장애 처리 | Ollama 오프라인 시 LLM 결과 null 저장, 탐지·알림은 독립 동작 |

---

## AI 보조 도구 사용 명시 (대회 규정 제9조⑤)

본 프로젝트의 일부 코드는 Claude (Anthropic)의 AI 코드 보조 도구를 활용하여 작성되었습니다.  
작성된 모든 코드는 개발자가 동작 원리를 직접 이해하고 검증하였습니다.

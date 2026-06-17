# Ollama LLM Spike

> Sprint 0 과제: Ollama llama3.1:8b LangChain LCEL 연동 PoC 검증

## 검증 목표

- [x] `ollama pull llama3.1:8b` 완료
- [x] LangChain `OllamaLLM` 로컬 호출 성공
- [x] 금융 위협 분석 프롬프트 한국어 응답 확인
- [x] Ollama 오프라인 시 예외 처리 동작 확인

## 결과

**수행일**: 2026-06-17

| 항목 | 내용 |
|------|------|
| Ollama 버전 | 0.30.9 |
| 모델 | `llama3.1:8b` (5.3GB, 이미 pull되어 있어 다운로드 단계 스킵) |
| 추론 위치 | GPU 100% (`ollama ps` 확인, RTX 4060 Ti) |
| 응답 시간 (3회) | 13.23s / 9.02s / 11.21s |
| 평균 응답 시간 | **11.15s** |
| 오프라인 예외 | `httpx.ConnectError` (`[WinError 10061] 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다`) |

### 응답 샘플 (Run 1)

```text
**이벤트 분석**

### 1. 위협 원인 추정

*   **금액:** 5,000,000원, 이는 일반적인 개인의 지출 금액보다 훨씬 큰 금액으로 보입니다.
*   **행위:** transfer, 이 이벤트는 특정 금액을 전송하는 행위를 의미합니다.
*   **User-Agent:** python-requests/2.31.0, 이는 사용자가 Python requests 라이브러리를 사용하여 API를 호출한 것으로 추론할 수 있습니다.

### 2. 공격 시나리오

1.  악의적 사용자가 비정상적인 접근 방법(프로그래밍)을 통해 API에 접속합니다.
2.  대량의 금액을 여러 번 전송하여 시스템의 자원과 금전적 손실을 유발합니다.

### 3. 대응 방안

1.  API 보안 강화: 비정상적인 접근 방법 탐지 및 차단 규칙 설정
2.  금액 전송 제한: 전자금융거래법 등 관련 규제에 따른 거래 범위 제한
3.  사용자 자격 관리 및 실시간 모니터링·리포팅 체계 구축
```

3회 모두 형식(원인 추정 / 공격 시나리오 / 대응 방안)을 지켜 한국어로 응답했다.

## 시도한 접근법

- `scripts/spike_ollama.py`에 LangChain LCEL 체인(`PromptTemplate | OllamaLLM`)을 구성해 측정
  - `langchain-ollama` 패키지의 `OllamaLLM` 사용 (`requirements.txt`에 추가)
  - `base_url`은 운영 설정(`config/config.yaml`의 `host.docker.internal`, 컨테이너→호스트용)과 달리 `http://localhost:11434` 사용 — 이 스크립트는 컨테이너가 아닌 호스트에서 직접 실행하기 때문
  - 타임아웃은 `config.yaml`의 `timeout_seconds: 30`과 동일하게 `client_kwargs={"timeout": 30}`로 전달 (`OllamaLLM`에 `timeout` 필드가 없고, 내부 `ollama.Client`가 받는 `**kwargs`가 `httpx` 클라이언트로 전달되는 구조)
  - 프롬프트는 `tests/conftest.py`의 `sample_attack_log` 픽스처와 동일한 필드(timestamp/ip/user_id/action/amount/user_agent)로 심야 대액 이체 탐지 이벤트를 구성
  - 동일 프롬프트로 3회 호출하며 `time.perf_counter()`로 응답시간 측정 후 평균 계산
- 오프라인 처리 확인은 실제 로컬 Ollama 서비스를 중지하지 않고, 아무도 listen하지 않는 포트(`localhost:11435`)로 별도 `OllamaLLM` 인스턴스를 만들어 호출 — 실행 중인 서비스에 영향 없이 connection refused 상황을 재현

## 알려진 이슈

**Windows 콘솔(cp949) 한글 출력 깨짐**

- 원인: Python 기본 `sys.stdout` 인코딩이 Windows 로캘(cp949)을 따라가면서 일부 비-cp949 문자(모델 응답에 섞여 나온 베트남어 성조 기호 등)에서 `UnicodeEncodeError`로 스크립트가 중단됨
- 해결: 스크립트 시작 시 `sys.stdout.reconfigure(encoding="utf-8")` 호출로 표준출력을 UTF-8로 고정. Phase 4에서 실제 LLM 결과를 저장/응답할 때도 동일하게 출력 인코딩을 명시할 필요가 있음 (#34/#37에서 참고)

**응답 시간 변동**

- 3회 응답시간이 8.76s~13.23s로 다소 변동 (네트워크가 아닌 로컬 GPU 추론이므로 변동 원인은 토큰 길이 차이로 추정). 평균 11.15s는 FastAPI 비동기 연동(#37) 시 타임아웃 30s 대비 여유가 있는 수준

## 성공 기준

탐지 이벤트 1건에 대해 한국어 위협 분석 (원인/시나리오/대응) 출력

**달성**: 3회 모두 원인 추정·공격 시나리오·대응 방안 형식으로 한국어 응답 생성 확인

**결론**: 계속 진행

**이유**: `OllamaLLM` 로컬 호출, 한국어 응답 품질, 평균 11초대 응답 시간(타임아웃 30s 이내), 오프라인 시 예외 처리까지 모두 확인되어 Phase 4 LLM 연동(#33~#37) 착수에 무리 없음

**다음 액션**: Phase 4 — `test_chain.py`(#33, Ollama mock TDD) → `chain.py`(#34) → `prompts.py`(#35) → 장애 처리(#36) → FastAPI 비동기 연동(#37) 순서로 진행, 본 스파이크의 프롬프트 구조와 타임아웃 값을 초안으로 참고

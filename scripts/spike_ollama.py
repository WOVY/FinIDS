"""Issue #6 스파이크: Ollama llama3.1:8b 응답 속도 측정.

PoC 전용 1회성 스크립트로 pytest 수집 대상(`tests/`) 밖에 둔다.
운영 환경(`config/config.yaml`)은 Docker 컨테이너에서 호스트의 Ollama를 호출하므로
`base_url`이 `host.docker.internal`이지만, 이 스크립트는 호스트에서 직접 실행하므로
`localhost`를 사용한다.

실행: `python scripts/spike_ollama.py`
"""

import sys
import time

import httpx
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

sys.stdout.reconfigure(encoding="utf-8")

MODEL = "llama3.1:8b"
BASE_URL = "http://localhost:11434"
OFFLINE_URL = "http://localhost:11435"  # 미사용 포트로 오프라인 상태를 시뮬레이션
TIMEOUT_SECONDS = 30
RUNS = 3

EVENT = {
    "timestamp": "2026-06-16T02:30:00Z",
    "ip": "10.0.0.1",
    "user_id": "user_002",
    "action": "transfer",
    "amount": 5_000_000,
    "user_agent": "python-requests/2.31.0",
}

PROMPT = PromptTemplate.from_template(
    "다음은 금융 거래 이상행위 탐지 룰이 발동한 이벤트다.\n"
    "- 시각: {timestamp}\n"
    "- IP: {ip}\n"
    "- 사용자: {user_id}\n"
    "- 행위: {action}\n"
    "- 금액: {amount}원\n"
    "- User-Agent: {user_agent}\n\n"
    "위 이벤트에 대해 한국어로 아래 형식에 맞춰 분석하라.\n"
    "1. 위협 원인 추정\n"
    "2. 공격 시나리오\n"
    "3. 대응 방안"
)


def measure_response_times() -> None:
    llm = OllamaLLM(
        model=MODEL,
        base_url=BASE_URL,
        client_kwargs={"timeout": TIMEOUT_SECONDS},
    )
    chain = PROMPT | llm

    elapsed_times = []
    for i in range(1, RUNS + 1):
        start = time.perf_counter()
        result = chain.invoke(EVENT)
        elapsed = time.perf_counter() - start
        elapsed_times.append(elapsed)
        print(f"\n--- Run {i} ({elapsed:.2f}s) ---")
        print(result)

    average = sum(elapsed_times) / len(elapsed_times)
    print(f"\n응답 시간: {[f'{t:.2f}s' for t in elapsed_times]}")
    print(f"평균 응답 시간: {average:.2f}s")


def check_offline_handling() -> None:
    print("\n--- 오프라인 시뮬레이션 (잘못된 포트 연결) ---")
    llm = OllamaLLM(
        model=MODEL,
        base_url=OFFLINE_URL,
        client_kwargs={"timeout": 5},
    )
    try:
        llm.invoke("ping")
        print("예외가 발생하지 않음 (예상과 다름)")
    except httpx.TransportError as exc:
        print(f"예외 발생 확인: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    try:
        measure_response_times()
    except Exception as exc:
        print(f"measure_response_times 실패: {type(exc).__name__}: {exc}")

    try:
        check_offline_handling()
    except Exception as exc:
        print(f"check_offline_handling 실패: {type(exc).__name__}: {exc}")

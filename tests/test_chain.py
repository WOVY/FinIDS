from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from engine import chain as chain_module

SAMPLE_ALERT = {
    "rule_name": "night_transfer",
    "ip": "10.0.0.1",
    "user_id": "user_002",
    "triggered_at": "2026-06-16T02:30:00Z",
    "description": "새벽 시간대 5,000,000원 고액 이체",
    "log_count": 1,
}


def test_analyze_alert_returns_report_on_success(monkeypatch):
    fake_llm = RunnableLambda(lambda _: AIMessage(content="원인 분석: 테스트 리포트"))
    monkeypatch.setattr(chain_module, "_build_llm", lambda: fake_llm)

    result = chain_module.analyze_alert(SAMPLE_ALERT)

    assert result["status"] == "ok"
    assert "원인 분석" in result["report"]


def test_analyze_alert_returns_null_on_timeout(monkeypatch):
    def _raise_timeout(_input):
        raise TimeoutError("Ollama 응답 없음")

    monkeypatch.setattr(chain_module, "_build_llm", lambda: RunnableLambda(_raise_timeout))

    result = chain_module.analyze_alert(SAMPLE_ALERT)

    assert result["status"] == "offline"
    assert result["report"] is None


def test_analyze_alert_returns_null_on_connection_error(monkeypatch):
    def _raise_connection_error(_input):
        raise ConnectionError("Ollama 연결 실패")

    monkeypatch.setattr(chain_module, "_build_llm", lambda: RunnableLambda(_raise_connection_error))

    result = chain_module.analyze_alert(SAMPLE_ALERT)

    assert result["status"] == "offline"
    assert result["report"] is None

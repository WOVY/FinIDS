from pathlib import Path

import yaml
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

from engine.prompts import THREAT_ANALYSIS_PROMPT

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["llm"]


def _build_llm() -> Runnable:
    return ChatOllama(
        model=CONFIG["model"],
        base_url=CONFIG["base_url"],
        timeout=CONFIG["timeout_seconds"],
    )


def analyze_alert(alert: dict) -> dict:
    """Alert 정보로 LangChain LCEL 체인을 실행해 한국어 위협 분석 리포트를 생성한다.

    Ollama 타임아웃·커넥션 실패 시 예외를 흡수하고 {"status": "offline", "report": None}을 반환한다.
    """
    chain = THREAT_ANALYSIS_PROMPT | _build_llm() | StrOutputParser()
    try:
        report = chain.invoke(alert)
    except Exception:
        return {"status": "offline", "report": None}
    return {"status": "ok", "report": report}

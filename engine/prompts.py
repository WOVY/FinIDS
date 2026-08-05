from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """당신은 금융감독원·금융보안원 FDS(이상금융거래탐지시스템) 위협 분석가입니다.
주어진 탐지 이벤트를 분석해 반드시 한국어로 다음 세 섹션을 작성하세요.

1. 원인 분석 (Root Cause): 왜 이 이벤트가 이상거래로 탐지되었는지
2. 위협 시나리오 (Threat Scenario): 공격자가 노렸을 수 있는 시나리오
3. 대응 방안 (Countermeasure): 지금 취해야 할 조치

각 섹션은 2~3문장으로 간결하게 작성하세요."""

HUMAN_PROMPT = """탐지 룰: {rule_name}
IP: {ip}
계정: {user_id}
탐지 시각: {triggered_at}
설명: {description}
관련 로그 건수: {log_count}"""

THREAT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ]
)

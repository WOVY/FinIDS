from pathlib import Path

import yaml

from engine.rules.base import Alert, Rule

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]["abnormal_ua"]


class AbnormalUARule(Rule):
    """config.yaml의 자동화 스크립트 User-Agent 패턴 탐지."""

    name = "abnormal_ua"

    def detect(self, events: list[dict]) -> list[Alert]:
        patterns = [p.lower() for p in CONFIG["patterns"]]
        alerts = []
        for i, event in enumerate(events):
            user_agent = event.get("user_agent", "")
            if not any(pattern in user_agent.lower() for pattern in patterns):
                continue
            alerts.append(
                Alert(
                    rule_name=self.name,
                    ip=event["ip"],
                    user_id=event.get("user_id"),
                    triggered_at=event["timestamp"],
                    description=f"자동화 스크립트 User-Agent 탐지: {user_agent}",
                    log_indices=[i],
                )
            )
        return alerts

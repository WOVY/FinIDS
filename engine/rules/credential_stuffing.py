from pathlib import Path

import yaml

from engine.rules.base import Alert, Rule, detect_account_burst

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]["credential_stuffing"]


class CredentialStuffingRule(Rule):
    """동일 IP, window_minutes 내 threshold_accounts개 이상 계정 로그인 시도 탐지."""

    name = "credential_stuffing"

    def detect(self, events: list[dict]) -> list[Alert]:
        return detect_account_burst(
            events,
            rule_name=self.name,
            window_minutes=CONFIG["window_minutes"],
            threshold_accounts=CONFIG["threshold_accounts"],
            action="login",
            description="IP {ip}에서 {count}개 계정 로그인 시도 (크리덴셜 스터핑 의심)",
        )

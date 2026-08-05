from pathlib import Path

import yaml

from engine.rules.base import Alert, Rule, detect_account_burst

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]["multi_account"]


class MultiAccountRule(Rule):
    """단일 IP, window_minutes 내 threshold_accounts개 이상 계정 접근 탐지 (액션 무관)."""

    name = "multi_account"

    def detect(self, events: list[dict]) -> list[Alert]:
        return detect_account_burst(
            events,
            rule_name=self.name,
            window_minutes=CONFIG["window_minutes"],
            threshold_accounts=CONFIG["threshold_accounts"],
            action=None,
            description="IP {ip}에서 {count}개 계정 접근 (다중 계정 접근 의심)",
        )

from pathlib import Path

import yaml

from engine.rules.base import Alert, Rule, parse_timestamp

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]["night_transfer"]


class NightTransferRule(Rule):
    """start_hour~end_hour 사이 min_amount 이상 이체 탐지."""

    name = "night_transfer"

    def detect(self, events: list[dict]) -> list[Alert]:
        alerts = []
        for i, event in enumerate(events):
            if event.get("action") != "transfer":
                continue
            hour = parse_timestamp(event).hour
            if not (CONFIG["start_hour"] <= hour < CONFIG["end_hour"]):
                continue
            if event["amount"] < CONFIG["min_amount"]:
                continue
            alerts.append(
                Alert(
                    rule_name=self.name,
                    ip=event["ip"],
                    user_id=event["user_id"],
                    triggered_at=event["timestamp"],
                    description=f"새벽 시간대 {event['amount']:,}원 고액 이체",
                    log_indices=[i],
                )
            )
        return alerts

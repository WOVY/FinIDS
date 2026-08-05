from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import yaml

from engine.rules.base import Alert, Rule, parse_timestamp

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]["split_transfer"]


class SplitTransferRule(Rule):
    """window_minutes 내 transfer_limit 근접 금액으로 threshold_count회 이상 반복 이체 탐지."""

    name = "split_transfer"

    def detect(self, events: list[dict]) -> list[Alert]:
        near_limit_amount = CONFIG["near_limit_ratio"] * CONFIG["transfer_limit"]
        window = timedelta(minutes=CONFIG["window_minutes"])

        by_account: dict[tuple[str, str], list[tuple[int, datetime]]] = defaultdict(list)
        for i, event in enumerate(events):
            if event.get("action") != "transfer":
                continue
            if event.get("amount", 0) < near_limit_amount:
                continue
            key = (event["ip"], event["user_id"])
            by_account[key].append((i, parse_timestamp(event)))

        alerts = []
        for (ip, user_id), items in by_account.items():
            items.sort(key=lambda item: item[1])
            start = 0
            for end in range(len(items)):
                while items[end][1] - items[start][1] > window:
                    start += 1
                current = items[start : end + 1]
                if len(current) >= CONFIG["threshold_count"]:
                    alerts.append(
                        Alert(
                            rule_name=self.name,
                            ip=ip,
                            user_id=user_id,
                            triggered_at=events[current[-1][0]]["timestamp"],
                            description=f"{CONFIG['window_minutes']}분 내 한도 근접 이체 {len(current)}회 반복 (분할 이체 의심)",
                            log_indices=[idx for idx, _ in current],
                        )
                    )
                    break
        return alerts

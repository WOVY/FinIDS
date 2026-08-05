from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Alert:
    rule_name: str
    ip: str
    user_id: str | None
    triggered_at: str
    description: str
    log_indices: list[int] = field(default_factory=list)


class Rule(ABC):
    name: str

    @abstractmethod
    def detect(self, events: list[dict]) -> list[Alert]:
        """이벤트 목록에서 이 룰에 해당하는 이상거래를 탐지해 Alert 목록을 반환한다."""


def parse_timestamp(event: dict) -> datetime:
    return datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")


def detect_account_burst(
    events: list[dict],
    *,
    rule_name: str,
    window_minutes: int,
    threshold_accounts: int,
    action: str | None,
    description: str,
) -> list[Alert]:
    """단일 IP가 window_minutes 내 threshold_accounts개 이상 계정에 접근하면 IP당 1건 Alert."""
    by_ip: dict[str, list[tuple[int, datetime, str]]] = defaultdict(list)
    for i, event in enumerate(events):
        if action is not None and event.get("action") != action:
            continue
        by_ip[event["ip"]].append((i, parse_timestamp(event), event["user_id"]))

    window = timedelta(minutes=window_minutes)
    alerts = []
    for ip, items in by_ip.items():
        items.sort(key=lambda item: item[1])
        start = 0
        triggered = False
        for end in range(len(items)):
            while items[end][1] - items[start][1] > window:
                start += 1
            accounts = {user_id for _, _, user_id in items[start : end + 1]}
            if len(accounts) >= threshold_accounts:
                triggered = True
                break
        if not triggered:
            continue
        all_accounts = {user_id for _, _, user_id in items}
        alerts.append(
            Alert(
                rule_name=rule_name,
                ip=ip,
                user_id=None,
                triggered_at=items[-1][1].strftime("%Y-%m-%dT%H:%M:%SZ"),
                description=description.format(ip=ip, count=len(all_accounts)),
                log_indices=[idx for idx, _, _ in items],
            )
        )
    return alerts

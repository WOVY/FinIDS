# Phase 2: Faker 기반 정상 거래 로그 생성
import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()

ACTIONS = ["login", "logout", "view_balance", "transfer", "view_statement"]


def _make_log(
    timestamp: datetime, ip: str, user_id: str, action: str, user_agent: str, amount: int
) -> dict:
    return {
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ip": ip,
        "user_id": user_id,
        "action": action,
        "user_agent": user_agent,
        "amount": amount,
        "label": "normal",
    }


def generate_normal_logs(n: int, start_time: datetime | None = None) -> list[dict]:
    """Faker로 정상 금융 웹로그 n건을 생성한다. transfer일 때만 amount>0."""
    start_time = start_time or datetime.now(UTC)
    logs = []
    for _ in range(n):
        action = random.choice(ACTIONS)
        amount = random.randint(1_000, 2_000_000) if action == "transfer" else 0
        timestamp = start_time + timedelta(seconds=random.randint(0, 24 * 3600))
        user_id = f"user_{random.randint(1, 5000):06d}"
        logs.append(_make_log(timestamp, fake.ipv4(), user_id, action, fake.user_agent(), amount))
    return logs


def write_logs(logs: list[dict], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for log in logs:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    write_logs(generate_normal_logs(9_500), "data/logs/normal.log")

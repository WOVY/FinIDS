# Phase 2: 탐지 룰 대응 공격 패턴 주입
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml
from faker import Faker

from data_gen.log_generator import write_logs

fake = Faker()

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
DETECTION = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["detection"]


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
        "label": "attack",
    }


def inject_credential_stuffing(start_time: datetime | None = None) -> list[dict]:
    """동일 IP가 window_minutes 내 threshold_accounts개 이상 계정에 로그인 시도."""
    cfg = DETECTION["credential_stuffing"]
    n_accounts = cfg["threshold_accounts"] + 2
    window = cfg["window_minutes"]
    start_time = start_time or datetime.now(UTC)
    ip = fake.ipv4()
    step_seconds = (window * 60) // n_accounts
    return [
        _make_log(
            start_time + timedelta(seconds=i * step_seconds),
            ip,
            f"user_{random.randint(100_000, 999_999)}",
            "login",
            fake.user_agent(),
            0,
        )
        for i in range(n_accounts)
    ]


def inject_night_transfer(n: int = 3, start_time: datetime | None = None) -> list[dict]:
    """start_hour~end_hour 사이 min_amount 이상 이체."""
    cfg = DETECTION["night_transfer"]
    base_date = (start_time or datetime.now(UTC)).date()
    logs = []
    for _ in range(n):
        hour = random.randint(cfg["start_hour"], cfg["end_hour"] - 1)
        timestamp = datetime(
            base_date.year, base_date.month, base_date.day, hour, random.randint(0, 59), tzinfo=UTC
        )
        amount = random.randint(cfg["min_amount"], cfg["min_amount"] * 3)
        logs.append(
            _make_log(
                timestamp,
                fake.ipv4(),
                f"user_{random.randint(100_000, 999_999)}",
                "transfer",
                fake.user_agent(),
                amount,
            )
        )
    return logs


def inject_multi_account(start_time: datetime | None = None) -> list[dict]:
    """단일 IP가 window_minutes 내 threshold_accounts개 이상 계정 접근."""
    cfg = DETECTION["multi_account"]
    n_accounts = cfg["threshold_accounts"] + 1
    window = cfg["window_minutes"]
    start_time = start_time or datetime.now(UTC)
    ip = fake.ipv4()
    step_seconds = (window * 60) // n_accounts
    return [
        _make_log(
            start_time + timedelta(seconds=i * step_seconds),
            ip,
            f"user_{random.randint(200_000, 999_999)}",
            random.choice(["login", "view_balance"]),
            fake.user_agent(),
            0,
        )
        for i in range(n_accounts)
    ]


def inject_abnormal_ua(n: int = 5, start_time: datetime | None = None) -> list[dict]:
    """config.yaml의 자동화 스크립트 UA 패턴으로 로그를 생성한다."""
    patterns = DETECTION["abnormal_ua"]["patterns"]
    start_time = start_time or datetime.now(UTC)
    logs = []
    for i in range(n):
        pattern = random.choice(patterns)
        user_agent = (
            f"{pattern}/{random.randint(1, 9)}.{random.randint(0, 99)}.{random.randint(0, 9)}"
        )
        timestamp = start_time + timedelta(seconds=i * 10)
        logs.append(
            _make_log(
                timestamp,
                fake.ipv4(),
                f"user_{random.randint(300_000, 999_999)}",
                "transfer",
                user_agent,
                random.randint(10_000, 500_000),
            )
        )
    return logs


def inject_split_transfer(start_time: datetime | None = None) -> list[dict]:
    """window_minutes 내 transfer_limit 직전 금액으로 threshold_count회 반복 이체."""
    cfg = DETECTION["split_transfer"]
    n_transfers = cfg["threshold_count"]
    window = cfg["window_minutes"]
    limit = cfg["transfer_limit"]
    start_time = start_time or datetime.now(UTC)
    ip = fake.ipv4()
    user_id = f"user_{random.randint(400_000, 999_999)}"
    step_minutes = window // n_transfers
    return [
        _make_log(
            start_time + timedelta(minutes=i * step_minutes),
            ip,
            user_id,
            "transfer",
            fake.user_agent(),
            int(limit * random.uniform(cfg["near_limit_ratio"], 0.99)),
        )
        for i in range(n_transfers)
    ]


def generate_attack_logs(n_each: int = 5) -> list[dict]:
    """탐지 룰 5종에 각각 대응하는 공격 패턴 로그를 모두 생성해 합친다."""
    logs = []
    logs += inject_credential_stuffing()
    logs += inject_night_transfer(n_each)
    logs += inject_multi_account()
    logs += inject_abnormal_ua(n_each)
    logs += inject_split_transfer()
    return logs


if __name__ == "__main__":
    write_logs(generate_attack_logs(n_each=100), "data/logs/attack.log")

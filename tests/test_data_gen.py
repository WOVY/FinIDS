from datetime import datetime, timedelta

from data_gen.attack_injector import (
    generate_attack_logs,
    inject_abnormal_ua,
    inject_credential_stuffing,
    inject_multi_account,
    inject_night_transfer,
    inject_split_transfer,
)
from data_gen.log_generator import generate_normal_logs

REQUIRED_FIELDS = {"timestamp", "ip", "user_id", "action", "user_agent", "amount", "label"}


def _parse_ts(log: dict) -> datetime:
    return datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%SZ")


def _assert_valid_log(log: dict) -> None:
    assert REQUIRED_FIELDS <= log.keys()
    assert isinstance(log["timestamp"], str)
    assert isinstance(log["ip"], str)
    assert isinstance(log["user_id"], str)
    assert isinstance(log["action"], str)
    assert isinstance(log["user_agent"], str)
    assert isinstance(log["amount"], int)
    _parse_ts(log)


class TestNormalLogs:
    def test_generates_requested_count(self):
        assert len(generate_normal_logs(50)) == 50

    def test_required_fields_and_types(self):
        for log in generate_normal_logs(20):
            _assert_valid_log(log)

    def test_label_is_normal(self):
        assert all(log["label"] == "normal" for log in generate_normal_logs(10))

    def test_valid_ipv4(self):
        import ipaddress

        for log in generate_normal_logs(10):
            ipaddress.ip_address(log["ip"])

    def test_amount_zero_unless_transfer(self):
        for log in generate_normal_logs(50):
            if log["action"] != "transfer":
                assert log["amount"] == 0
            else:
                assert log["amount"] > 0


class TestAttackLogs:
    def test_required_fields_and_types(self):
        for log in generate_attack_logs():
            _assert_valid_log(log)

    def test_label_is_attack(self):
        logs = generate_attack_logs()
        assert logs
        assert all(log["label"] == "attack" for log in logs)

    def test_credential_stuffing_single_ip_many_accounts_within_window(self):
        logs = inject_credential_stuffing()
        assert len({log["ip"] for log in logs}) == 1
        assert len({log["user_id"] for log in logs}) >= 10
        timestamps = [_parse_ts(log) for log in logs]
        assert max(timestamps) - min(timestamps) <= timedelta(minutes=10)

    def test_night_transfer_hour_and_amount(self):
        logs = inject_night_transfer()
        assert logs
        for log in logs:
            hour = _parse_ts(log).hour
            assert 0 <= hour < 5
            assert log["action"] == "transfer"
            assert log["amount"] >= 3_000_000

    def test_multi_account_single_ip_many_accounts_within_window(self):
        logs = inject_multi_account()
        assert len({log["ip"] for log in logs}) == 1
        assert len({log["user_id"] for log in logs}) >= 4
        timestamps = [_parse_ts(log) for log in logs]
        assert max(timestamps) - min(timestamps) <= timedelta(minutes=30)

    def test_abnormal_ua_patterns(self):
        patterns = ("python-requests", "curl", "wget", "go-http-client")
        logs = inject_abnormal_ua()
        assert logs
        for log in logs:
            assert any(p in log["user_agent"].lower() for p in patterns)

    def test_split_transfer_near_limit_repeated_within_window(self):
        logs = inject_split_transfer()
        assert len(logs) >= 5
        for log in logs:
            assert log["action"] == "transfer"
            assert log["amount"] > 0
        timestamps = [_parse_ts(log) for log in logs]
        assert max(timestamps) - min(timestamps) <= timedelta(minutes=60)

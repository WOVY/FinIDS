from data_gen.attack_injector import (
    inject_abnormal_ua,
    inject_credential_stuffing,
    inject_multi_account,
    inject_night_transfer,
    inject_split_transfer,
)
from data_gen.log_generator import generate_normal_logs
from engine.rules.abnormal_ua import AbnormalUARule
from engine.rules.credential_stuffing import CredentialStuffingRule
from engine.rules.multi_account import MultiAccountRule
from engine.rules.night_transfer import NightTransferRule
from engine.rules.split_transfer import SplitTransferRule


def _alerted_indices(alerts) -> set[int]:
    indices: set[int] = set()
    for alert in alerts:
        indices.update(alert.log_indices)
    return indices


class TestCredentialStuffing:
    def test_detects_attack_pattern(self):
        logs = inject_credential_stuffing()
        alerts = CredentialStuffingRule().detect(logs)
        assert alerts
        assert _alerted_indices(alerts) == set(range(len(logs)))

    def test_no_false_positive_on_normal_logs(self):
        logs = generate_normal_logs(300)
        alerts = CredentialStuffingRule().detect(logs)
        assert alerts == []


class TestNightTransfer:
    def test_detects_attack_pattern(self):
        logs = inject_night_transfer(5)
        alerts = NightTransferRule().detect(logs)
        assert len(alerts) == 5
        assert _alerted_indices(alerts) == set(range(len(logs)))

    def test_no_false_positive_on_normal_logs(self):
        logs = generate_normal_logs(300)
        alerts = NightTransferRule().detect(logs)
        assert alerts == []


class TestMultiAccount:
    def test_detects_attack_pattern(self):
        logs = inject_multi_account()
        alerts = MultiAccountRule().detect(logs)
        assert alerts
        assert _alerted_indices(alerts) == set(range(len(logs)))

    def test_no_false_positive_on_normal_logs(self):
        logs = generate_normal_logs(300)
        alerts = MultiAccountRule().detect(logs)
        assert alerts == []


class TestAbnormalUA:
    def test_detects_attack_pattern(self):
        logs = inject_abnormal_ua(5)
        alerts = AbnormalUARule().detect(logs)
        assert len(alerts) == 5
        assert _alerted_indices(alerts) == set(range(len(logs)))

    def test_no_false_positive_on_normal_logs(self):
        logs = generate_normal_logs(300)
        alerts = AbnormalUARule().detect(logs)
        assert alerts == []


class TestSplitTransfer:
    def test_detects_attack_pattern(self):
        logs = inject_split_transfer()
        alerts = SplitTransferRule().detect(logs)
        assert alerts
        assert _alerted_indices(alerts) == set(range(len(logs)))

    def test_no_false_positive_on_normal_logs(self):
        logs = generate_normal_logs(300)
        alerts = SplitTransferRule().detect(logs)
        assert alerts == []

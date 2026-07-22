from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_slack(monkeypatch):
    mock = MagicMock()
    mock.return_value.status_code = 200
    monkeypatch.setattr("requests.post", mock)
    return mock


@pytest.fixture
def mock_es_ping(monkeypatch):
    mock = MagicMock(return_value=True)
    monkeypatch.setattr("elasticsearch.Elasticsearch.ping", mock)
    return mock


@pytest.fixture
def sample_normal_log() -> dict:
    return {
        "timestamp": "2026-06-16T10:00:00Z",
        "ip": "192.168.1.1",
        "user_id": "user_001",
        "action": "login",
        "user_agent": "Mozilla/5.0",
        "amount": 0,
    }


@pytest.fixture
def sample_attack_log() -> dict:
    return {
        "timestamp": "2026-06-16T02:30:00Z",
        "ip": "10.0.0.1",
        "user_id": "user_002",
        "action": "transfer",
        "user_agent": "python-requests/2.31.0",
        "amount": 5_000_000,
    }

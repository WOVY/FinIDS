import pytest
from httpx import ASGITransport, AsyncClient

import api.main
from api.main import app

SAMPLE_ALERT = {
    "rule_name": "night_transfer",
    "ip": "10.0.0.1",
    "user_id": "user_002",
    "triggered_at": "2026-06-16T02:30:00Z",
    "description": "새벽 시간대 5,000,000원 고액 이체",
    "log_count": 1,
}


@pytest.mark.asyncio
async def test_health_returns_200(mock_es_ping):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_reports_elasticsearch_connected(mock_es_ping):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    body = response.json()
    assert body["status"] == "ok"
    assert body["elasticsearch"] == "connected"


@pytest.mark.asyncio
async def test_health_reports_elasticsearch_disconnected(monkeypatch):
    monkeypatch.setattr(
        "elasticsearch.Elasticsearch.ping", lambda self: (_ for _ in ()).throw(ConnectionError())
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["elasticsearch"] == "disconnected"


@pytest.mark.asyncio
async def test_analyze_returns_report_when_ollama_online(monkeypatch):
    monkeypatch.setattr(
        api.main, "analyze_alert", lambda alert: {"status": "ok", "report": "테스트 리포트"}
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/analyze", json=SAMPLE_ALERT)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["report"] == "테스트 리포트"


@pytest.mark.asyncio
async def test_analyze_returns_offline_when_ollama_down(monkeypatch):
    monkeypatch.setattr(
        api.main, "analyze_alert", lambda alert: {"status": "offline", "report": None}
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/analyze", json=SAMPLE_ALERT)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "offline"
    assert body["report"] is None

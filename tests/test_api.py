import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


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

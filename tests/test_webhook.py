"""
Tests for Webhook domain endpoints.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_create_webhook(monkeypatch):
    """Test creating a webhook."""
    webhook_data = {
        "url": "https://example.com/webhook",
        "entity_type": "Order",
        "update_type": "Created",
    }

    mock_response = {"WebhookID": "webhook-123", "Secret": "secret-key-123"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhooks", json=webhook_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["WebhookID"] == "webhook-123"
    assert result["data"]["Secret"] == "secret-key-123"


@pytest.mark.asyncio
async def test_list_webhooks(monkeypatch):
    """Test listing webhooks."""
    mock_response = {
        "Result": [
            {
                "WebhookID": "webhook-123",
                "URL": "https://example.com/webhook",
                "EntityType": "Order",
                "UpdateType": "Created",
                "Active": True,
            }
        ]
    }

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response["Result"], "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/webhooks")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["data"]) == 1
    assert result["data"][0]["WebhookID"] == "webhook-123"


@pytest.mark.asyncio
async def test_delete_webhook(monkeypatch):
    """Test deleting a webhook."""

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": None, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/webhooks/webhook-123")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_refresh_webhook_secret(monkeypatch):
    """Test refreshing webhook secret."""
    mock_response = {"Secret": "new-secret-456"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhooks/webhook-123/refresh-secret")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["Secret"] == "new-secret-456"


@pytest.mark.asyncio
async def test_create_webhook_error(monkeypatch):
    """Test error handling for webhook creation."""
    webhook_data = {"url": "invalid-url", "entity_type": "Order", "update_type": "Created"}

    async def fake_request(method, url, **kwargs):
        return {
            "success": False,
            "data": None,
            "error": [{"Code": "INVALID_URL", "Description": "Invalid webhook URL"}],
            "error_code": "INVALID_URL",
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhooks", json=webhook_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is False
    assert "INVALID_URL" in str(result["error"])

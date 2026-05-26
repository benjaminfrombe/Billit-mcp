"""Tests for accountant domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_register_feed(monkeypatch):
    """Test registering a new feed."""
    expected_response = {
        "success": True,
        "data": {
            "FeedID": "feed-123",
            "FeedName": "TestFeed",
            "FeedType": "Income",
            "Status": "Active",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/feed"
        data = kwargs.get("json", {})
        assert data["FeedName"] == "TestFeed"
        assert data["FeedType"] == "Income"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/feeds", json={"feed_name": "TestFeed", "feed_type": "Income"}
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_list_feeds(monkeypatch):
    """Test listing all feeds."""
    expected_response = {
        "success": True,
        "data": [
            {"FeedID": "feed-123", "FeedName": "TestFeed", "FeedType": "Income", "Status": "Active"}
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/feed"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/feeds")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_feed_items(monkeypatch):
    """Test getting items from a specific feed."""
    expected_response = {
        "success": True,
        "data": [
            {
                "ItemID": "item-456",
                "FeedName": "TestFeed",
                "FileName": "invoice_001.pdf",
                "ReceivedDate": "2024-01-15T10:00:00Z",
            }
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/feed/TestFeed"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/feeds/TestFeed")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_download_feed_item_content(monkeypatch):
    """Test downloading content of a feed item."""
    expected_response = {
        "success": True,
        "data": {
            "Content": "base64encodedcontent==",
            "ContentType": "application/pdf",
            "FileName": "invoice_001.pdf",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/feed/TestFeed/item-456"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/feeds/TestFeed/item-456")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_confirm_feed_item(monkeypatch):
    """Test confirming a feed item as processed."""
    expected_response = {
        "success": True,
        "data": {
            "ItemID": "item-456",
            "Status": "Confirmed",
            "ConfirmedAt": "2024-01-15T11:00:00Z",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/feed/TestFeed/item-456/confirm"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/feeds/TestFeed/item-456/confirm")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_delete_feed(monkeypatch):
    """Test deleting a feed."""
    expected_response = {
        "success": True,
        "data": {"Message": "Feed deleted successfully", "FeedName": "TestFeed"},
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "DELETE"
        assert endpoint == "/feed/TestFeed"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/feeds/TestFeed")
        assert response.status_code == 200
        assert response.json() == expected_response

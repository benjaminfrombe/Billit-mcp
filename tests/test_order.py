"""
Tests for Order domain endpoints.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_list_orders(monkeypatch):
    """Test listing orders."""
    mock_response = {
        "Result": [
            {
                "OrderID": 123,
                "OrderType": "Invoice",
                "OrderDirection": "Income",
                "OrderNumber": "INV-001",
                "OrderDate": "2024-01-01",
                "TotalExcludingVAT": 1000.00,
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
        response = await client.get("/orders")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["data"]) == 1
    assert result["data"][0]["OrderID"] == 123


@pytest.mark.asyncio
async def test_create_order(monkeypatch):
    """Test creating a new order."""
    order_data = {
        "order_type": "Invoice",
        "order_direction": "Income",
        "customer": {"name": "Test Customer", "vat_number": "BE0123456789"},
        "lines": [{"description": "Test Product", "quantity": 1, "unit_price": 100.00}],
    }

    mock_response = {"OrderID": 456, "OrderNumber": "INV-002"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders", json=order_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["OrderID"] == 456


@pytest.mark.asyncio
async def test_get_order(monkeypatch):
    """Test getting a specific order."""
    mock_response = {
        "OrderID": 123,
        "OrderType": "Invoice",
        "OrderDirection": "Income",
        "OrderNumber": "INV-001",
        "TotalExcludingVAT": 1000.00,
        "Lines": [{"Description": "Test Product", "Quantity": 1, "UnitPrice": 1000.00}],
    }

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/orders/123")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["OrderID"] == 123


@pytest.mark.asyncio
async def test_update_order(monkeypatch):
    """Test updating an order."""
    update_data = {"IsSent": True, "Paid": True, "PaidDate": "2024-01-15"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": {"success": True}, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch("/orders/123", json=update_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_delete_order(monkeypatch):
    """Test deleting an order."""

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": None, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/orders/123")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_record_payment(monkeypatch):
    """Test recording a payment."""
    payment_data = {"paid": True, "paid_date": "2024-01-15", "payment_method": "bank_transfer"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": {"success": True}, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/123/payments", json=payment_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_send_order(monkeypatch):
    """Test sending orders."""
    send_data = {"order_ids": [123, 456], "transport_type": "Email", "strict_transport": False}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": {"success": True}, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/send", json=send_data)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_list_deleted_orders(monkeypatch):
    """Test listing deleted orders."""
    mock_response = {"Result": [{"OrderID": 789, "DeletedDate": "2024-01-20"}]}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response["Result"], "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/orders/deleted")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["data"]) == 1

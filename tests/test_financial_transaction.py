"""
Tests for Financial Transaction domain endpoints.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_list_financial_transactions(monkeypatch):
    """Test listing financial transactions."""
    mock_response = {
        "Result": [
            {
                "TransactionID": 123,
                "Amount": 1500.00,
                "Date": "2024-01-15",
                "Description": "Payment from Customer X",
                "Reference": "INV-001",
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
        response = await client.get("/financial-transactions")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["data"]) == 1
    assert result["data"][0]["TransactionID"] == 123


@pytest.mark.asyncio
async def test_list_financial_transactions_with_filter(monkeypatch):
    """Test listing financial transactions with OData filter."""
    mock_response = {"Result": [{"TransactionID": 456, "Amount": 2000.00, "Date": "2024-01-20"}]}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response["Result"], "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/financial-transactions", params={"odata_filter": "Amount gt 1000"}
        )

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_import_transactions_file(monkeypatch):
    """Test importing a bank statement file."""
    mock_response = {"ImportID": "import-123", "Status": "Processing"}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Simulate file upload
        files = {"file": ("statement.csv", b"test,data,here", "text/csv")}
        response = await client.post("/financial-transactions/import", files=files)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["ImportID"] == "import-123"


@pytest.mark.asyncio
async def test_confirm_transaction_import(monkeypatch):
    """Test confirming a transaction import."""
    mock_response = {"Status": "Completed", "ImportedCount": 5}

    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": mock_response, "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/financial-transactions/import-123/confirm")

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["data"]["ImportedCount"] == 5


@pytest.mark.asyncio
async def test_import_transactions_file_error(monkeypatch):
    """Test error handling for file import."""

    async def fake_request(method, url, **kwargs):
        return {
            "success": False,
            "data": None,
            "error": [{"Code": "INVALID_FILE", "Description": "Invalid file format"}],
            "error_code": "INVALID_FILE",
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        files = {"file": ("statement.txt", b"invalid", "text/plain")}
        response = await client.post("/financial-transactions/import", files=files)

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is False
    assert "INVALID_FILE" in str(result["error"])

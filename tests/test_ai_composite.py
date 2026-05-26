"""Tests for AI composite tools."""

from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from server import app

from billit.services import ai_composite


class RecordingClient:
    def __init__(self) -> None:
        self.calls = 0

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        self.calls += 1
        return {"success": True, "data": [], "error": None, "error_code": None}


def test_period_bounds_accepts_only_year_or_month() -> None:
    assert ai_composite.period_bounds("2024") == ("2024-01-01", "2025-01-01")
    assert ai_composite.period_bounds("2024-01") == ("2024-01-01", "2024-02-01")
    assert ai_composite.period_bounds("2024-Q1") is None
    assert ai_composite.period_bounds("last_30_days") is None


@pytest.mark.asyncio
async def test_cashflow_rejects_invalid_period_without_request() -> None:
    client = RecordingClient()

    result = await ai_composite.get_cashflow_overview(client, "last_30_days")

    assert result == {
        "success": False,
        "data": None,
        "error": "Unsupported period 'last_30_days'. Use YYYY or YYYY-MM.",
        "error_code": "INVALID_PERIOD",
    }
    assert client.calls == 0


@pytest.mark.asyncio
async def test_suggest_payment_reconciliation(monkeypatch):
    """Test payment reconciliation suggestion."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        if endpoint == "/orders":
            return {
                "success": True,
                "data": [
                    {
                        "OrderID": 1,
                        "OrderNumber": "INV-001",
                        "ToPay": 1000.00,
                        "StructuredCommunication": "+++123/4567/89012+++",
                    }
                ],
                "error": None,
                "error_code": None,
            }
        elif endpoint == "/financialTransactions":
            return {
                "success": True,
                "data": [
                    {
                        "FinancialTransactionID": 100,
                        "Amount": 1000.00,
                        "Communication": "+++123/4567/89012+++",
                    }
                ],
                "error": None,
                "error_code": None,
            }
        raise AssertionError(f"Unexpected endpoint: {endpoint}")

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/suggest-payment-reconciliation")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) > 0
        # Check that we have a match
        match = data["data"][0]
        assert match["order_id"] == 1
        assert match["transaction_id"] == 100
        assert match["amount"] == 1000.00


@pytest.mark.asyncio
async def test_generate_invoice_summary(monkeypatch):
    """Test invoice summary generation."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "$filter" in params
        return {
            "success": True,
            "data": [
                {"TotalIncl": 10000.00},
                {"TotalIncl": 15000.00},
                {"TotalIncl": 25000.00},
            ],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/invoice-summary?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        # Check the actual response structure
        assert "count" in data["data"]
        assert "total_incl" in data["data"]
        assert data["data"]["count"] == 3
        assert data["data"]["total_incl"] == 50000.00


@pytest.mark.asyncio
async def test_generate_expense_summary(monkeypatch):
    """Test expense summary generation."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "$filter" in params
        assert "OrderDirection eq 'Cost'" in params["$filter"]
        return {
            "success": True,
            "data": [
                {"TotalIncl": 5000.00},
                {"TotalIncl": 10000.00},
                {"TotalIncl": 15000.00},
            ],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/expense-summary?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        # Check the actual response structure
        assert "count" in data["data"]
        assert "total_incl" in data["data"]
        assert data["data"]["count"] == 3
        assert data["data"]["total_incl"] == 30000.00


@pytest.mark.asyncio
async def test_get_cashflow_overview(monkeypatch):
    """Test cashflow overview."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "$filter" in params
        # Return different data based on the filter
        if "OrderDirection eq 'Income'" in params["$filter"]:
            return {
                "success": True,
                "data": [{"TotalIncl": 5000.00}, {"TotalIncl": 10000.00}],
                "error": None,
                "error_code": None,
            }
        else:  # Cost
            return {
                "success": True,
                "data": [
                    {"TotalIncl": 3000.00},
                    {"TotalIncl": 4000.00},
                ],
                "error": None,
                "error_code": None,
            }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/cashflow?period=2024-01")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        # Check the actual response structure
        assert "income" in data["data"]
        assert "cost" in data["data"]
        assert "net" in data["data"]
        assert data["data"]["income"] == 15000.00
        assert data["data"]["cost"] == 7000.00
        assert data["data"]["net"] == 8000.00


@pytest.mark.asyncio
async def test_categorize_expense_invoice(monkeypatch):
    """Test expense invoice categorization."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders/123"
        return {
            "success": True,
            "data": {"OrderLines": [{"Description": "office paper"}]},
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/ai/categorize-expense/123")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        assert data["data"] == {"invoice_id": 123, "category": "Office"}


@pytest.mark.asyncio
async def test_list_overdue_invoices(monkeypatch):
    """Test listing overdue invoices."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "$filter" in params
        assert "Overdue eq true" in params["$filter"]
        return {
            "success": True,
            "data": [
                {"OrderID": 123},
                {"OrderID": 456},
                {"OrderID": 789},
            ],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/overdue-invoices")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        # Check the actual response structure - list of order IDs
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 3
        assert 123 in data["data"]
        assert 456 in data["data"]
        assert 789 in data["data"]


@pytest.mark.asyncio
async def test_get_supplier_spend_summary(monkeypatch):
    """Test supplier spend summary."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "OrderDirection eq 'Cost'" in params["$filter"]
        assert "Party/PartyID eq 456" in params["$filter"]
        return {
            "success": True,
            "data": [{"TotalIncl": 10000.00}, {"TotalIncl": 15000.00}],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/supplier-spend/456?period=2024")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        assert data["data"] == {"supplier_id": 456, "total_incl": 25000.00}


@pytest.mark.asyncio
async def test_get_customer_revenue_summary(monkeypatch):
    """Test customer revenue summary."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        params = kwargs.get("params", {})
        assert "OrderDirection eq 'Income'" in params["$filter"]
        assert "Party/PartyID eq 789" in params["$filter"]
        return {
            "success": True,
            "data": [{"TotalIncl": 25000.00}, {"TotalIncl": 50000.00}],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/customer-revenue/789?period=2024")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        assert data["data"] == {"customer_id": 789, "total_incl": 75000.00}


@pytest.mark.asyncio
async def test_find_duplicate_contacts(monkeypatch):
    """Test finding duplicate contacts."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/parties"
        params = kwargs.get("params", {})
        assert params["$top"] == 120
        return {
            "success": True,
            "data": [
                {"PartyID": 123, "Name": "John Doe Ltd"},
                {"PartyID": 456, "Name": "John Doe Ltd"},
            ],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/duplicate-contacts")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        assert len(data["data"]) == 1
        assert data["data"][0]["party_a"] == 123
        assert data["data"][0]["party_b"] == 456


@pytest.mark.asyncio
async def test_normalize_contact_address(monkeypatch):
    """Test contact address normalization."""

    async def fake_request(self, method, endpoint, **kwargs):
        if method == "GET":
            assert endpoint == "/parties/123"
            return {
                "success": True,
                "data": {
                    "Addresses": [
                        {
                            "Street": "main street",
                            "City": "brussels",
                            "Country": "belgium",
                        }
                    ]
                },
                "error": None,
                "error_code": None,
            }
        assert method == "PATCH"
        assert endpoint == "/parties/123"
        assert kwargs["json"]["Addresses"][0] == {
            "Street": "Main Street",
            "City": "Brussels",
            "Country": "Belgium",
        }
        return {"success": True, "data": {}, "error": None, "error_code": None}

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/ai/normalize-address/123")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None
        assert data["data"] == {"party_id": 123, "normalized": True}


@pytest.mark.asyncio
async def test_create_invoice_from_text(monkeypatch):
    """Test creating invoice from natural language."""
    expected_response = {
        "success": True,
        "data": {
            "OrderID": 999,
            "ParsedData": {
                "Customer": "Tech Corp",
                "Items": [{"Description": "Consulting", "Amount": 5000.00}],
                "TotalAmount": 5000.00,
            },
            "Confidence": 0.88,
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/orders"
        data = kwargs.get("json", {})
        description = data["OrderLines"][0]["Description"]
        assert "Invoice Tech Corp for 5000 euros consulting work" in description
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/ai/create-invoice-from-text",
            json={"text_description": "Invoice Tech Corp for 5000 euros consulting work"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None


@pytest.mark.asyncio
async def test_smart_search_orders(monkeypatch):
    """Test smart search over orders uses the canonical plural endpoint."""

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        assert kwargs["params"] == {"$top": 120}
        return {
            "success": True,
            "data": [
                {
                    "OrderID": 1,
                    "OrderNumber": "INV-001",
                    "CounterParty": {"DisplayName": "Acme Corp"},
                    "TotalIncl": 1000.00,
                }
            ],
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/smart-search?query=acme&entity_type=orders")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total_results"] == 1
        assert data["data"]["results"][0]["entity_type"] == "order"
        assert data["data"]["results"][0]["data"]["OrderID"] == 1


@pytest.mark.asyncio
async def test_smart_search_propagates_upstream_errors(monkeypatch):
    """Test smart search returns upstream API failures."""

    error_response = {
        "success": False,
        "data": None,
        "error": "Billit unavailable",
        "error_code": "REQUEST_ERROR",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/orders"
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ai/smart-search?query=acme&entity_type=orders")
        assert response.status_code == 200
        assert response.json() == error_response


@pytest.mark.asyncio
async def test_ai_composite_error_handling(monkeypatch):
    """Test error handling in AI composite endpoints."""
    error_response = {
        "success": False,
        "data": None,
        "error": "AI processing failed",
        "error_code": "AI_ERROR",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Test various endpoints with error response
        response = await client.get("/ai/suggest-payment-reconciliation")
        assert response.status_code == 200
        assert response.json() == error_response

        response = await client.get("/ai/overdue-invoices")
        assert response.status_code == 200
        assert response.json() == error_response

"""Tests for misc domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_search_company(monkeypatch):
    """Test searching for a company."""
    expected_response = {
        "success": True,
        "data": [
            {
                "CompanyID": "BE0123456789",
                "CompanyName": "Tech Solutions NV",
                "VATNumber": "BE0123456789",
                "Address": {
                    "Street": "Tech Street 123",
                    "City": "Brussels",
                    "PostalCode": "1000",
                    "Country": "BE",
                },
            }
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/misc/companysearch/Tech Solutions"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/search-company?keywords=Tech Solutions")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_type_codes(monkeypatch):
    """Test getting type codes."""
    expected_response = {
        "success": True,
        "data": [
            {"Code": "21", "Description": "21%", "Category": "VATRate"},
            {"Code": "12", "Description": "12%", "Category": "VATRate"},
            {"Code": "6", "Description": "6%", "Category": "VATRate"},
            {"Code": "0", "Description": "0%", "Category": "VATRate"},
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/misc/typecodes/VATRate"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/type-codes/VATRate")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_code_detail(monkeypatch):
    """Test getting detail for a specific code."""
    expected_response = {
        "success": True,
        "data": {
            "Code": "EUR",
            "Description": "Euro",
            "Category": "Currency",
            "Symbol": "€",
            "IsDefault": True,
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/misc/typecodes/Currency/EUR"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/type-codes/Currency/EUR")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_misc_error_handling(monkeypatch):
    """Test error handling for misc operations."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Invalid code type",
        "error_code": "INVALID_TYPE",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/type-codes/InvalidType")
        assert response.status_code == 200
        assert response.json() == error_response


@pytest.mark.asyncio
async def test_search_company_no_results(monkeypatch):
    """Test company search with no results."""
    expected_response = {"success": True, "data": [], "error": None, "error_code": None}

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/misc/companysearch/NonexistentCompany123"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/search-company?keywords=NonexistentCompany123")
        assert response.status_code == 200
        assert response.json() == expected_response

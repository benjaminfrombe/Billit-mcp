"""Tests for GL Account domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_create_gl_account(monkeypatch):
    """Test creating a GL account."""
    expected_response = {
        "success": True,
        "data": {
            "AccountID": 123,
            "AccountCode": "4000",
            "AccountName": "Sales Revenue",
            "AccountType": "Income",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/glAccount"
        data = kwargs.get("json", {})
        assert data["account_code"] == "4000"
        assert data["account_name"] == "Sales Revenue"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/gl-accounts",
            json={
                "account_code": "4000",
                "account_name": "Sales Revenue",
                "account_type": "Income",
            },
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_import_gl_accounts(monkeypatch):
    """Test bulk importing GL accounts."""
    expected_response = {
        "success": True,
        "data": {
            "ImportedCount": 3,
            "FailedCount": 0,
            "Results": [
                {"AccountCode": "4000", "Status": "Success"},
                {"AccountCode": "5000", "Status": "Success"},
                {"AccountCode": "6000", "Status": "Success"},
            ],
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/glAccount/import"
        data = kwargs.get("json", [])
        assert len(data) == 3
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/gl-accounts/import",
            json=[
                {"account_code": "4000", "account_name": "Sales Revenue", "account_type": "Income"},
                {
                    "account_code": "5000",
                    "account_name": "Cost of Goods Sold",
                    "account_type": "Expense",
                },
                {
                    "account_code": "6000",
                    "account_name": "Operating Expenses",
                    "account_type": "Expense",
                },
            ],
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_import_journal_entries(monkeypatch):
    """Test importing journal entries."""
    expected_response = {
        "success": True,
        "data": {
            "ImportedCount": 2,
            "TotalDebit": 5000.00,
            "TotalCredit": 5000.00,
            "JournalIDs": ["JE-001", "JE-002"],
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/journalEntry/import"
        data = kwargs.get("json", [])
        assert len(data) == 2
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/journal-entries/import",
            json=[
                {
                    "entry_date": "2024-01-15",
                    "description": "Sales entry",
                    "lines": [
                        {"account_code": "1200", "debit": 2500.00, "credit": 0},
                        {"account_code": "4000", "debit": 0, "credit": 2500.00},
                    ],
                },
                {
                    "entry_date": "2024-01-16",
                    "description": "Expense entry",
                    "lines": [
                        {"account_code": "6000", "debit": 2500.00, "credit": 0},
                        {"account_code": "1000", "debit": 0, "credit": 2500.00},
                    ],
                },
            ],
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_gl_account_error_handling(monkeypatch):
    """Test error handling for GL account operations."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Account code already exists",
        "error_code": "DUPLICATE_ACCOUNT",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/gl-accounts", json={"account_code": "4000", "account_name": "Sales Revenue"}
        )
        assert response.status_code == 200
        assert response.json() == error_response

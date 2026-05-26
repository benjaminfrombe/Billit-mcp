"""Tests for reports domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_list_available_reports(monkeypatch):
    """Test listing available reports."""
    expected_response = {
        "success": True,
        "data": [
            {
                "ReportID": "sales-summary",
                "ReportName": "Sales Summary Report",
                "Description": "Monthly sales summary with VAT breakdown",
                "Parameters": ["start_date", "end_date", "include_draft"],
            },
            {
                "ReportID": "aged-receivables",
                "ReportName": "Aged Receivables Report",
                "Description": "Outstanding customer invoices by age",
                "Parameters": ["as_of_date", "customer_id"],
            },
            {
                "ReportID": "vat-report",
                "ReportName": "VAT Report",
                "Description": "VAT declaration report for tax authorities",
                "Parameters": ["period", "year"],
            },
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/reports"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/reports")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_report(monkeypatch):
    """Test generating and retrieving a specific report."""
    expected_response = {
        "success": True,
        "data": {
            "ReportID": "sales-summary",
            "GeneratedAt": "2024-01-15T15:00:00Z",
            "Format": "PDF",
            "FileID": "file-report-123",
            "Content": "base64encodedreportcontent==",
            "FileName": "sales_summary_2024_01.pdf",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/reports/sales-summary"
        params = kwargs.get("params", {})
        assert params.get("start_date") == "2024-01-01"
        assert params.get("end_date") == "2024-01-31"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/reports/sales-summary",
            params={"start_date": "2024-01-01", "end_date": "2024-01-31"},
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_report_error_handling(monkeypatch):
    """Test error handling for report generation."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Invalid report parameters: end_date must be after start_date",
        "error_code": "INVALID_PARAMETERS",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/reports/sales-summary",
            params={"start_date": "2024-01-31", "end_date": "2024-01-01"},
        )
        assert response.status_code == 200
        assert response.json() == error_response

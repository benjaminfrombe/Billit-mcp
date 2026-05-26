"""Tests for Peppol domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_check_peppol_participant(monkeypatch):
    """Test checking if a company is a Peppol participant."""
    expected_response = {
        "success": True,
        "data": {
            "IsParticipant": True,
            "Identifier": "BE0123456789",
            "CompanyName": "Tech Solutions NV",
            "PeppolID": "0208:BE0123456789",
            "Capabilities": ["Invoice", "CreditNote", "Order"],
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/peppol/participantInformation/BE0123456789"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/peppol/participantInformation/BE0123456789")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_register_peppol_participant(monkeypatch):
    """Test registering as a Peppol participant."""
    expected_response = {
        "success": True,
        "data": {
            "RegistrationID": "reg-123",
            "Status": "Pending",
            "EstimatedCompletionDate": "2024-01-20",
            "RequiredDocuments": ["CompanyRegistration", "VATCertificate"],
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/peppol/participants"
        assert kwargs.get("json", {}) == {
            "registration_data": {
                "contact_email": "admin@techsolutions.be",
                "contact_name": "John Doe",
            }
        }
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/peppol/participants",
            json={
                "registration_data": {
                    "contact_email": "admin@techsolutions.be",
                    "contact_name": "John Doe",
                }
            },
        )
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_unregister_peppol_participant(monkeypatch):
    """Test unregistering from Peppol."""
    expected_response = {
        "success": True,
        "data": {
            "Message": "Successfully unregistered from Peppol network",
            "EffectiveDate": "2024-01-31",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "DELETE"
        assert endpoint == "/peppol/participants"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/peppol/participants")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_send_peppol_invoice(monkeypatch):
    """Test sending an invoice via Peppol."""
    expected_response = {
        "success": True,
        "data": {
            "TransmissionID": "trans-456",
            "OrderID": 123,
            "Status": "Sent",
            "SentAt": "2024-01-15T14:30:00Z",
            "RecipientPeppolID": "0208:BE0987654321",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/peppol/sendOrder"
        assert kwargs.get("json") == {"order_id": 123}
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/peppol/sendOrder?order_id=123")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_list_peppol_inbox(monkeypatch):
    """Test listing Peppol inbox items."""
    expected_response = {
        "success": True,
        "data": [
            {
                "InboxItemID": "inbox-789",
                "DocumentType": "Invoice",
                "SenderPeppolID": "0208:BE0987654321",
                "SenderName": "Supplier Corp",
                "ReceivedAt": "2024-01-15T10:00:00Z",
                "Status": "New",
            }
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/peppol/inbox"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/peppol/inbox")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_confirm_peppol_invoice(monkeypatch):
    """Test confirming a Peppol invoice."""
    expected_response = {
        "success": True,
        "data": {
            "InboxItemID": "inbox-789",
            "Status": "Confirmed",
            "ProcessedAt": "2024-01-15T11:00:00Z",
            "CreatedOrderID": 456,
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/peppol/inbox/inbox-789/confirm"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/peppol/inbox/inbox-789/confirm")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_refuse_peppol_invoice(monkeypatch):
    """Test refusing a Peppol invoice."""
    expected_response = {
        "success": True,
        "data": {
            "InboxItemID": "inbox-789",
            "Status": "Refused",
            "RefusedAt": "2024-01-15T11:00:00Z",
            "RefusalReason": "Duplicate invoice",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/peppol/inbox/inbox-789/refuse"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/peppol/inbox/inbox-789/refuse")
        assert response.status_code == 200
        assert response.json() == expected_response

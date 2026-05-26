import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_get_account_information(monkeypatch):
    async def fake_request(method, url, **kwargs):
        assert method == "GET"
        assert url == "/account/accountInformation"
        return {
            "success": True,
            "data": {"Name": "Test"},
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/account")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"Name": "Test"},
        "error": None,
        "error_code": None,
    }


@pytest.mark.asyncio
async def test_register_company(monkeypatch):
    async def fake_request(method, url, **kwargs):
        assert method == "POST"
        assert url == "/account/registercompany"
        assert kwargs.get("json") == {"name": "ACME"}
        return {
            "success": True,
            "data": {"CompanyID": 1},
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/account/register", json={"name": "ACME"})
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"CompanyID": 1},
        "error": None,
        "error_code": None,
    }

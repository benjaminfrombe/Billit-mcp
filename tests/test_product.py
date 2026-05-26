import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_list_products(monkeypatch):
    async def fake_request(method, url, **kwargs):
        assert method == "GET"
        assert url == "/products"
        return {"success": True, "data": [], "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/products")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": [],
        "error": None,
        "error_code": None,
    }


@pytest.mark.asyncio
async def test_upsert_product(monkeypatch):
    async def fake_request(method, url, **kwargs):
        assert method == "POST"
        assert url == "/products"
        payload = kwargs.get("json")
        assert payload == {"Description": "Test"}
        return {
            "success": True,
            "data": {"ProductID": 1, "Description": "Test"},
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/products", json={"description": "Test"})
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"ProductID": 1, "Description": "Test"},
        "error": None,
        "error_code": None,
    }


@pytest.mark.asyncio
async def test_get_product(monkeypatch):
    async def fake_request(method, url, **kwargs):
        assert method == "GET"
        assert url == "/products/1"
        return {
            "success": True,
            "data": {"ProductID": 1, "Description": "Item"},
            "error": None,
            "error_code": None,
        }

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"ProductID": 1, "Description": "Item"},
        "error": None,
        "error_code": None,
    }

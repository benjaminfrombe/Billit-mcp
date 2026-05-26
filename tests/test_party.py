import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import ASGITransport, AsyncClient

from server import app


@pytest.mark.asyncio
async def test_list_parties(monkeypatch):
    async def fake_request(method, url, **kwargs):
        return {"success": True, "data": [], "error": None, "error_code": None}

    monkeypatch.setattr(
        "billit.client.BillitAPIClient.request",
        lambda self, method, url, **kwargs: fake_request(method, url, **kwargs),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/parties")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": [],
        "error": None,
        "error_code": None,
    }

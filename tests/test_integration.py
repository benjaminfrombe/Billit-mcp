import os
import pytest
from httpx import AsyncClient, ASGITransport

from server import app

sandbox_key = os.getenv("BILLIT_API_KEY")


@pytest.mark.asyncio
@pytest.mark.skipif(not sandbox_key, reason="Sandbox credentials not configured")
async def test_list_parties_integration():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/parties")
    # In real integration this would call the sandbox
    assert response.status_code == 200

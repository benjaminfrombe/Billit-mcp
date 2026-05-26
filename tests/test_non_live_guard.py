"""Regression tests for the non-live Billit request guard."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_non_live_route_requires_mocked_billit_client() -> None:
    """Normal route tests fail before any unmocked Billit client call can escape."""

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        with pytest.raises(AssertionError, match=r"Unexpected BillitAPIClient\.request"):
            await client.get("/parties")

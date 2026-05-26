"""Tests for BillitAPIClient functionality including rate limiting and error handling."""

import pytest
import respx
from httpx import Response

from billit.client import BillitAPIClient, BillitSettings, RateLimiter

pytestmark = pytest.mark.allow_billit_request


@pytest.mark.asyncio
async def test_rate_limiting():
    """Test that rate limiting initializes correctly."""
    rate_limiter = RateLimiter(rate_per_minute=60)

    # Test initial state
    assert rate_limiter.rate_per_minute == 60
    assert rate_limiter._tokens == 60

    # Test token consumption
    await rate_limiter.acquire()
    assert rate_limiter._tokens == 59

    # Test multiple acquisitions
    for _ in range(5):
        await rate_limiter.acquire()
    assert rate_limiter._tokens == 54


@pytest.mark.asyncio
async def test_error_handling_400(monkeypatch):
    """Test handling of 400 Bad Request errors."""
    monkeypatch.setenv("BILLIT_API_KEY", "test-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "12345")

    client = BillitAPIClient()

    with respx.mock:
        respx.get("https://api.billit.be/v1/test").mock(
            return_value=Response(
                400, json={"errors": [{"Code": "INVALID_VAT", "Description": "Invalid VAT number"}]}
            )
        )

        result = await client.request("GET", "/test")

        assert result["success"] is False
        assert "INVALID_VAT" in str(result["error"])
        assert "Invalid VAT number" in str(result["error"])


@pytest.mark.asyncio
async def test_error_handling_401(monkeypatch):
    """Test handling of 401 Unauthorized errors."""
    monkeypatch.setenv("BILLIT_API_KEY", "invalid-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "12345")

    client = BillitAPIClient()

    with respx.mock:
        respx.get("https://api.billit.be/v1/test").mock(return_value=Response(401))

        result = await client.request("GET", "/test")

        assert result["success"] is False
        assert result["error"] is not None


@pytest.mark.asyncio
async def test_error_handling_404(monkeypatch):
    """Test handling of 404 Not Found errors."""
    monkeypatch.setenv("BILLIT_API_KEY", "test-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "12345")

    client = BillitAPIClient()

    with respx.mock:
        respx.get("https://api.billit.be/v1/test/999").mock(return_value=Response(404))

        result = await client.request("GET", "/test/999")

        assert result["success"] is False
        assert result["error"] is not None


@pytest.mark.asyncio
async def test_error_handling_500(monkeypatch):
    """Test handling of 500 Server Error."""
    monkeypatch.setenv("BILLIT_API_KEY", "test-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "12345")

    client = BillitAPIClient()

    with respx.mock:
        respx.get("https://api.billit.be/v1/test").mock(return_value=Response(500))

        result = await client.request("GET", "/test")

        assert result["success"] is False
        assert result["error"] is not None


@pytest.mark.asyncio
async def test_successful_request(monkeypatch):
    """Test successful API request."""
    monkeypatch.setenv("BILLIT_API_KEY", "test-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "12345")

    client = BillitAPIClient()

    with respx.mock:
        respx.get("https://api.billit.be/v1/test").mock(
            return_value=Response(200, json={"data": "test"})
        )

        result = await client.request("GET", "/test")

        assert result["success"] is True
        assert result["data"] == {"data": "test"}
        assert result["error"] is None


@pytest.mark.asyncio
async def test_explicit_settings_do_not_require_env(monkeypatch):
    """Explicit client settings bypass env-derived Billit configuration."""

    monkeypatch.delenv("BILLIT_API_KEY", raising=False)
    monkeypatch.delenv("BILLIT_BASE_URL", raising=False)
    monkeypatch.delenv("BILLIT_PARTY_ID", raising=False)

    client = BillitAPIClient(
        BillitSettings(
            base_url="https://api.billit.be/v1",
            api_key="explicit-key",
            party_id="67890",
            rate_limit_per_minute=100000,
        )
    )

    with respx.mock:
        route = respx.get("https://api.billit.be/v1/test").mock(
            return_value=Response(200, json={"ok": True})
        )

        result = await client.request("GET", "/test")

    await client.close()
    assert result["success"] is True
    assert route.calls.last.request.headers["apiKey"] == "explicit-key"
    assert route.calls.last.request.headers["partyID"] == "67890"

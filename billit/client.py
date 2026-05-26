"""HTTP client for interacting with the Billit REST API."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
_rate_limiter: RateLimiter | None = None


def get_env(name: str, default: str | None = None) -> str:
    """Return the value of an environment variable or raise if missing."""

    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


@dataclass
class BillitSettings:
    """Explicit Billit API configuration for clients that should not mutate env."""

    base_url: str
    api_key: str
    party_id: str
    context_party_id: str | None = None
    rate_limit_per_minute: int | None = None

    @classmethod
    def from_env(cls) -> BillitSettings:
        """Build settings from the process environment."""

        rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE")
        return cls(
            base_url=get_env("BILLIT_BASE_URL"),
            api_key=get_env("BILLIT_API_KEY"),
            party_id=get_env("BILLIT_PARTY_ID"),
            context_party_id=os.getenv("BILLIT_CONTEXT_PARTY_ID"),
            rate_limit_per_minute=int(rate_limit) if rate_limit else None,
        )


@dataclass
class BillitOAuthSettings:
    """Explicit Billit OAuth configuration for hosted clients."""

    base_url: str
    access_token: str
    party_id: str
    context_party_id: str | None = None
    rate_limit_per_minute: int | None = None


@dataclass
class RateLimiter:
    """Simple token bucket rate limiter for outgoing requests."""

    rate_per_minute: int

    def __post_init__(self) -> None:
        """Initialize token bucket state."""

        self._tokens = self.rate_per_minute
        self._lock = asyncio.Lock()
        self._last_refill = time.monotonic()

    async def acquire(self) -> None:
        """Wait until a token is available."""

        async with self._lock:
            await self._refill()
            while self._tokens <= 0:
                await asyncio.sleep(1)
                await self._refill()
            self._tokens -= 1

    async def _refill(self) -> None:
        """Refill tokens based on elapsed time."""

        now = time.monotonic()
        elapsed = now - self._last_refill
        tokens_to_add = int(elapsed / 60 * self.rate_per_minute)
        if tokens_to_add > 0:
            self._tokens = min(self.rate_per_minute, self._tokens + tokens_to_add)
            self._last_refill = now


def get_rate_limiter(rate: int | None = None) -> RateLimiter:
    """Return the process-wide Billit API rate limiter."""

    global _rate_limiter
    resolved_rate = rate or int(os.getenv("RATE_LIMIT_PER_MINUTE", "50"))
    if _rate_limiter is None or _rate_limiter.rate_per_minute != resolved_rate:
        _rate_limiter = RateLimiter(resolved_rate)
    return _rate_limiter


class BillitAPIClient:
    """Thin wrapper around ``httpx.AsyncClient`` with rate limiting and response handling."""

    def __init__(self, settings: BillitSettings | BillitOAuthSettings | None = None) -> None:
        """Initialize the client using environment variables for configuration."""

        self.settings = settings or BillitSettings.from_env()
        self.base_url = self.settings.base_url
        self.party_id = self.settings.party_id
        self.context_party_id = self.settings.context_party_id
        self.rate_limiter = get_rate_limiter(self.settings.rate_limit_per_minute)

        headers = self._headers_for(self.settings)

        # Add context party ID if available (for accountants)
        if self.context_party_id:
            headers["ContextPartyID"] = self.context_party_id

        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=30.0)

    @staticmethod
    def _headers_for(settings: BillitSettings | BillitOAuthSettings) -> dict[str, str]:
        """Build Billit headers for API-key or OAuth authentication."""

        headers = {
            "PartyID": settings.party_id,
            "Accept": "application/json",
        }
        if isinstance(settings, BillitOAuthSettings):
            headers["Authorization"] = f"Bearer {settings.access_token}"
        else:
            headers["apiKey"] = settings.api_key
        return headers

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        """Perform a request against the Billit API and wrap the response."""

        await self.rate_limiter.acquire()
        try:
            response = await self.client.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            logger.warning("billit_request_failed", extra={"url": url, "error": str(exc)})
            return {
                "success": False,
                "data": None,
                "error": str(exc),
                "error_code": "REQUEST_ERROR",
            }
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> dict[str, Any]:
        """Convert a raw HTTP response into the MCP envelope."""

        if response.status_code // 100 == 2:
            try:
                # Handle both JSON responses and empty successful responses
                if response.text.strip():
                    data = response.json()
                else:
                    # Empty response is success for PATCH operations
                    data = {"message": "Operation completed successfully"}
                return {"success": True, "data": data, "error": None, "error_code": None}
            except ValueError:
                # Handle malformed JSON in successful responses
                return {
                    "success": True,
                    "data": {
                        "message": "Operation completed successfully",
                        "response_text": response.text[:200],
                    },
                    "error": None,
                    "error_code": None,
                }
        try:
            payload = response.json()
        except Exception:
            payload = {}
        error = payload.get("errors") or payload.get("message") or response.text
        if isinstance(error, list) and error and isinstance(error[0], dict):
            error_code = error[0].get("Code") or error[0].get("code")
        else:
            error_code = payload.get("code")
        return {
            "success": False,
            "data": None,
            "error": error,
            "error_code": error_code,
        }

    async def close(self) -> None:
        """Close the underlying HTTP client."""

        await self.client.aclose()

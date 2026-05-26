"""Explicit local API-key settings helpers."""

from __future__ import annotations

import os
from urllib.parse import urlparse

from billit.client import BillitSettings
from billit_mcp.local_api_key.common import LocalToolError


def local_settings_without_context(settings: BillitSettings) -> BillitSettings:
    """Return explicit API-key settings with ContextPartyID disabled."""

    return BillitSettings(
        base_url=settings.base_url,
        api_key=settings.api_key,
        party_id=settings.party_id,
        context_party_id=None,
        rate_limit_per_minute=settings.rate_limit_per_minute,
    )


def settings_from_env() -> BillitSettings:
    """Build explicit local API-key settings from required environment variables."""

    missing = missing_local_settings()
    if missing:
        raise LocalToolError(
            "configuration_error",
            "Missing required local API-key settings: " + ", ".join(missing),
            error_code="CONFIGURATION_ERROR",
        )
    rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE")
    return BillitSettings(
        base_url=str(os.environ["BILLIT_BASE_URL"]),
        api_key=str(os.environ["BILLIT_API_KEY"]),
        party_id=str(os.environ["BILLIT_PARTY_ID"]),
        context_party_id=None,
        rate_limit_per_minute=int(rate_limit) if rate_limit else None,
    )


def missing_local_settings() -> list[str]:
    """Return missing required local API-key env var names without reading secrets."""

    return [
        name
        for name in ("BILLIT_API_KEY", "BILLIT_BASE_URL", "BILLIT_PARTY_ID")
        if not os.getenv(name)
    ]


def environment_name(base_url: str) -> str:
    """Classify the Billit target environment without exposing credentials."""

    if "sandbox" in base_url:
        return "sandbox"
    if "api.billit.be" in base_url:
        return "production"
    return "custom"


def base_url_host(base_url: str) -> str:
    """Return the configured Billit host without credentials."""

    parsed = urlparse(base_url)
    return parsed.netloc or base_url.replace("https://", "").replace("http://", "").split("/")[0]


def local_warnings(settings: BillitSettings) -> list[str]:
    """Return local configuration warnings for explicit settings."""

    warnings: list[str] = []
    if os.getenv("BILLIT_CONTEXT_PARTY_ID"):
        warnings.append("BILLIT_CONTEXT_PARTY_ID is ignored; ContextPartyID is disabled.")
    if not settings.party_id.isdigit():
        warnings.append("BILLIT_PARTY_ID is non-numeric; reads can run, but writes are blocked.")
    if environment_name(settings.base_url) != "sandbox":
        warnings.append("Local API-key runtime is pointed at a non-sandbox Billit base URL.")
    return warnings

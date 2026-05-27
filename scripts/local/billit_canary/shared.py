"""Shared helpers for sanitized Billit live canary probes."""

from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from billit.client import BillitSettings
from billit.smart_search import normalize_items

if TYPE_CHECKING:
    from collections.abc import Callable

SANDBOX_BASE_URL = "https://api.sandbox.billit.be/v1"
SANDBOX_KEYCHAIN_SERVICE = "BILLIT_SANDBOX_API_KEY_K4K"


class CanaryClient(Protocol):
    """Small protocol required by the live canary."""

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]: ...

    async def close(self) -> None: ...


@dataclass(frozen=True)
class CanarySettings:
    """Resolved non-secret canary configuration."""

    billit: BillitSettings
    environment: str
    key_source: str


class ReadOnlyBillitClient:
    """Guard canary probes from accidental writes."""

    def __init__(self, client: CanaryClient, *, allow_writes: bool = False) -> None:
        self._client = client
        self.allow_writes = allow_writes

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        if method.upper() != "GET" and not self.allow_writes:
            return {
                "success": False,
                "data": None,
                "error": f"Canary blocked non-read request: {method.upper()} {url}",
                "error_code": "LIVE_CANARY_WRITE_BLOCKED",
            }
        return await self._client.request(method, url, **kwargs)

    async def close(self) -> None:
        await self._client.close()


def environment_name(base_url: str) -> str:
    """Classify the Billit target environment without exposing credentials."""

    if "sandbox" in base_url:
        return "sandbox"
    if "api.billit.be" in base_url:
        return "production"
    return "custom"


def read_keychain_secret(service: str) -> str | None:
    """Read a macOS Keychain generic-password secret by service name."""

    if platform.system() != "Darwin":
        return None
    result = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", service],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    secret = result.stdout.strip()
    return secret or None


def first_present_env(*names: str) -> tuple[str, str] | None:
    """Return the first non-empty environment variable value and its name."""

    for name in names:
        value = os.getenv(name)
        if value:
            return value, name
    return None


def resolve_canary_party_id(*, sandbox: bool) -> str:
    """Return the explicit sandbox/production PartyID for live canary calls."""

    if sandbox:
        party_id = os.getenv("BILLIT_SANDBOX_PARTY_ID") or os.getenv("BILLIT_PARTY_ID")
        if not party_id:
            raise SystemExit(
                "BILLIT_SANDBOX_PARTY_ID or BILLIT_PARTY_ID is required for the live canary."
            )
        return party_id
    party_id = os.getenv("BILLIT_PARTY_ID")
    if not party_id:
        raise SystemExit("BILLIT_PARTY_ID is required for non-sandbox live canary runs.")
    return party_id


def resolve_canary_settings(
    base_url: str,
    *,
    keychain_reader: Callable[[str], str | None] = read_keychain_secret,
) -> CanarySettings:
    """Resolve Billit settings for the canary without mutating process env."""

    environment = environment_name(base_url)
    if environment == "sandbox":
        env_key = first_present_env("BILLIT_SANDBOX_API_KEY_K4K")
        if env_key is not None:
            api_key, key_source = env_key
        else:
            keychain_secret = keychain_reader(SANDBOX_KEYCHAIN_SERVICE)
            if keychain_secret:
                api_key = keychain_secret
                key_source = f"keychain:{SANDBOX_KEYCHAIN_SERVICE}"
            else:
                raise SystemExit(
                    "Sandbox canary requires BILLIT_SANDBOX_API_KEY_K4K from env "
                    f"or macOS Keychain service {SANDBOX_KEYCHAIN_SERVICE}."
                )
        party_id = resolve_canary_party_id(sandbox=True)
    else:
        generic_key = first_present_env("BILLIT_API_KEY")
        if generic_key is None:
            raise SystemExit("Non-sandbox canary requires BILLIT_API_KEY.")
        api_key, key_source = generic_key
        party_id = resolve_canary_party_id(sandbox=False)

    return CanarySettings(
        billit=BillitSettings(
            base_url=base_url,
            api_key=api_key,
            party_id=party_id,
            context_party_id=None,
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "50")),
        ),
        environment=environment,
        key_source=key_source,
    )


def count_items(data: Any) -> int:
    """Return a sanitized count for arbitrary Billit payloads."""

    items = normalize_items(data)
    if items:
        return len(items)
    if isinstance(data, dict):
        return len(data)
    if isinstance(data, list):
        return len(data)
    return 0


def probe_record(endpoint: str, response: dict[str, Any]) -> dict[str, Any]:
    """Return sanitized probe evidence."""

    return {
        "endpoint": endpoint,
        "success": bool(response.get("success")),
        "error_code": response.get("error_code"),
        "item_count": count_items(response.get("data")),
    }


def api_key_header_proof(
    client: CanaryClient, settings: BillitSettings
) -> dict[str, bool | str | None]:
    """Return sanitized proof that the local API-key client sends required headers."""

    headers = getattr(getattr(client, "client", None), "headers", {})
    return {
        "api_key_header_present": "apiKey" in headers,
        "party_id_header_correct": str(headers.get("PartyID")) == settings.party_id,
        "party_id_header_name": "PartyID" if "PartyID" in headers else None,
        "context_party_id_header_absent": "ContextPartyID" not in headers,
    }

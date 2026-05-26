"""Unit tests for the local Billit live canary runner."""

from __future__ import annotations

import json
import os
from types import SimpleNamespace
from typing import Any

import pytest
from scripts.local import live_billit_canary as canary
from scripts.local.seed_hosted_oauth_grant import secret_from_env_or_keychain
from sqlalchemy import text

from billit.client import BillitSettings
from billit_mcp.persistence.database import HostedDatabase


class FakeCanaryClient:
    def __init__(self, settings: BillitSettings) -> None:
        self.settings = settings
        self.client = SimpleNamespace(
            is_closed=False,
            headers={
                "apiKey": settings.api_key,
                "PartyID": settings.party_id,
                "Accept": "application/json",
            },
        )
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((method, url, kwargs))
        if url == "/account/accountInformation":
            return {
                "success": True,
                "data": {"Companies": [{"PartyID": int(self.settings.party_id)}]},
                "error": None,
                "error_code": None,
            }
        if method.upper() == "POST":
            return {"success": True, "data": {"OrderID": 1}, "error": None, "error_code": None}
        return {"success": True, "data": {"Items": [{"id": 1}]}, "error": None, "error_code": None}

    async def close(self) -> None:
        self.closed = True
        self.client.is_closed = True


def test_canary_prefers_sandbox_specific_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLIT_SANDBOX_API_KEY_K4K", "sandbox-k4k")
    monkeypatch.setenv("BILLIT_SANDBOX_API_KEY", "sandbox-generic")
    monkeypatch.setenv("BILLIT_API_KEY", "prod")
    monkeypatch.setenv("BILLIT_SANDBOX_PARTY_ID", "999")
    monkeypatch.setenv("BILLIT_PARTY_ID", "111")

    settings = canary.resolve_canary_settings(
        canary.SANDBOX_BASE_URL,
        keychain_reader=lambda service: None,
    )

    assert settings.billit.api_key == "sandbox-k4k"
    assert settings.billit.party_id == "999"
    assert settings.key_source == "BILLIT_SANDBOX_API_KEY_K4K"


def test_canary_uses_keychain_before_generic_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BILLIT_SANDBOX_API_KEY_K4K", raising=False)
    monkeypatch.delenv("BILLIT_SANDBOX_API_KEY", raising=False)
    monkeypatch.setenv("BILLIT_API_KEY", "generic")
    monkeypatch.setenv("BILLIT_PARTY_ID", "111")

    settings = canary.resolve_canary_settings(
        canary.SANDBOX_BASE_URL,
        keychain_reader=lambda service: "keychain-secret",
    )

    assert settings.billit.api_key == "keychain-secret"
    assert settings.key_source == "keychain:BILLIT_SANDBOX_API_KEY_K4K"


def test_seed_helper_secret_lookup_prefers_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN", "access-from-env")

    value = secret_from_env_or_keychain(
        "BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN",
        "BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN_SANDBOX",
    )

    assert value == "access-from-env"


@pytest.mark.asyncio
async def test_read_only_client_blocks_write_requests() -> None:
    client = canary.ReadOnlyBillitClient(
        FakeCanaryClient(BillitSettings(base_url="url", api_key="key", party_id="party"))
    )

    result = await client.request("POST", "/orders")

    assert result["success"] is False
    assert result["error_code"] == "LIVE_CANARY_WRITE_BLOCKED"


@pytest.mark.asyncio
async def test_run_canary_writes_sanitized_report_without_env_mutation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setenv("BILLIT_SANDBOX_API_KEY_K4K", "sandbox-k4k")
    monkeypatch.setenv("BILLIT_PARTY_ID", "111")
    monkeypatch.delenv("BILLIT_API_KEY", raising=False)
    before = dict(os.environ)

    created_clients: list[FakeCanaryClient] = []

    def fake_factory(settings: BillitSettings) -> FakeCanaryClient:
        client = FakeCanaryClient(settings)
        created_clients.append(client)
        return client

    report_path = await canary.run_canary(
        output_root=tmp_path,
        keychain_reader=lambda service: None,
        client_factory=fake_factory,
    )

    report = json.loads(report_path.read_text())
    assert report["passed"] is True
    assert report["mode"] == "api-key-readonly"
    assert report["key_source"] == "BILLIT_SANDBOX_API_KEY_K4K"
    assert report["header_proof"]["api_key_header_present"] is True
    assert report["header_proof"]["party_id_header_correct"] is True
    assert report["header_proof"]["party_id_header_name"] == "PartyID"
    assert report["header_proof"]["context_party_id_header_absent"] is True
    assert "sandbox-k4k" not in report_path.read_text()
    assert os.environ.get("BILLIT_API_KEY") == before.get("BILLIT_API_KEY")
    assert created_clients[0].settings.api_key == "sandbox-k4k"
    assert created_clients[0].closed is True
    assert any(
        probe["endpoint"] == "curated:billit.invoice.create_draft.write_blocked"
        and probe["success"]
        for probe in report["probes"]
    )


@pytest.mark.asyncio
async def test_hosted_canary_schema_stamps_legacy_local_sqlite_db(tmp_path) -> None:
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'hosted.db'}"
    database = HostedDatabase(database_url)
    try:
        await database.create_all_for_tests_only()
        state = await canary.ensure_hosted_canary_schema(database_url)
        async with database.engine.connect() as connection:
            revision = (
                await connection.execute(text("select version_num from alembic_version"))
            ).scalar_one()
    finally:
        await database.close()

    assert state == "stamped_existing_local_sqlite_schema"
    assert revision == "20260526_0001"

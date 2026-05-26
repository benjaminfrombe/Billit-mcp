"""Unit tests for the local Billit live canary runner."""

from __future__ import annotations

import json
import os
from typing import Any

import pytest
from scripts.local import live_billit_canary as canary

from billit.client import BillitSettings


class FakeCanaryClient:
    def __init__(self, settings: BillitSettings) -> None:
        self.settings = settings
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((method, url, kwargs))
        return {"success": True, "data": {"Items": [{"id": 1}]}, "error": None, "error_code": None}

    async def close(self) -> None:
        self.closed = True


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
    assert report["key_source"] == "BILLIT_SANDBOX_API_KEY_K4K"
    assert "sandbox-k4k" not in report_path.read_text()
    assert os.environ.get("BILLIT_API_KEY") == before.get("BILLIT_API_KEY")
    assert created_clients[0].settings.api_key == "sandbox-k4k"
    assert created_clients[0].closed is True

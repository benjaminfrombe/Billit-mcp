"""Focused tests for the curated local API-key MCP stdio runtime."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import billit_mcp.server as mcp_server
from billit.client import BillitSettings
from billit_mcp.local_api_key.runtime import LOCAL_API_KEY_TOOL_NAMES, LocalAPIKeyRuntime
from billit_mcp.local_api_key.state import LocalStateStore


class FakeBillitClient:
    """Small async Billit client double for local API-key runtime tests."""

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
        if settings.context_party_id:
            self.client.headers["ContextPartyID"] = settings.context_party_id
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    async def request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((method.upper(), endpoint, kwargs))
        if endpoint == "/account/accountInformation":
            return {
                "success": True,
                "data": {"Companies": [{"PartyID": 1, "Name": "Own Company"}]},
                "error": None,
                "error_code": None,
            }
        if endpoint == "/orders" and method.upper() == "GET":
            return {
                "success": True,
                "data": {"Items": [{"OrderID": 99, "TotalIncl": 121}]},
                "error": None,
                "error_code": None,
            }
        if endpoint == "/orders" and method.upper() == "POST":
            return {"success": True, "data": {"OrderID": 99}, "error": None, "error_code": None}
        if endpoint == "/orders/99":
            return {
                "success": True,
                "data": {
                    "OrderID": 99,
                    "OrderNumber": "2026-099",
                    "Customer": {"Name": "ACME", "VATNumber": "BE0123456789"},
                    "TotalIncl": 121,
                    "Currency": "EUR",
                    "IsSent": False,
                    "Paid": False,
                    "DeliveryStatus": "ToSend",
                },
                "error": None,
                "error_code": None,
            }
        if endpoint == "/orders/commands/send" and method.upper() == "POST":
            return {"success": True, "data": {"sent": True}, "error": None, "error_code": None}
        if endpoint == "/financialTransactions":
            return {"success": True, "data": {"Items": []}, "error": None, "error_code": None}
        if endpoint == "/reports":
            return {"success": True, "data": {"Items": []}, "error": None, "error_code": None}
        return {"success": True, "data": {}, "error": None, "error_code": None}

    async def close(self) -> None:
        self.closed = True
        self.client.is_closed = True


def _runtime(
    tmp_path: Any, monkeypatch: pytest.MonkeyPatch
) -> tuple[LocalAPIKeyRuntime, list[FakeBillitClient]]:
    monkeypatch.delenv("BILLIT_MCP_LOCAL_ALLOW_WRITES", raising=False)
    monkeypatch.delenv("BILLIT_MCP_LOCAL_ALLOW_SENDS", raising=False)
    clients: list[FakeBillitClient] = []

    def factory(settings: BillitSettings) -> FakeBillitClient:
        client = FakeBillitClient(settings)
        clients.append(client)
        return client

    runtime = LocalAPIKeyRuntime(
        settings=BillitSettings(
            base_url="https://api.sandbox.billit.be/v1",
            api_key="local-key",
            party_id="1",
            context_party_id="must-not-be-sent",
            rate_limit_per_minute=100000,
        ),
        state=LocalStateStore(tmp_path / "state.db"),
        client_factory=factory,
    )
    return runtime, clients


@pytest.mark.asyncio
async def test_mcp_get_client_reuses_and_closes_process_client(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    fake = FakeBillitClient(
        BillitSettings(
            base_url="https://api.sandbox.billit.be/v1",
            api_key="local-key",
            party_id="1",
            rate_limit_per_minute=100000,
        )
    )
    runtime = LocalAPIKeyRuntime(
        settings=fake.settings,
        state=LocalStateStore(tmp_path / "test-mcp-runtime.db"),
        client_factory=lambda settings: fake,
    )
    monkeypatch.setattr(mcp_server, "_runtime", runtime)

    first = await mcp_server.get_client()
    second = await mcp_server.get_client()
    await mcp_server.close_mcp_client()

    assert first is fake
    assert second is fake
    assert fake.closed is True


@pytest.mark.asyncio
async def test_connection_status_reports_missing_env_without_poisoning_runtime(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    for name in ("BILLIT_API_KEY", "BILLIT_BASE_URL", "BILLIT_PARTY_ID"):
        monkeypatch.delenv(name, raising=False)
    clients: list[FakeBillitClient] = []

    def factory(settings: BillitSettings) -> FakeBillitClient:
        client = FakeBillitClient(settings)
        clients.append(client)
        return client

    runtime = LocalAPIKeyRuntime(
        state=LocalStateStore(tmp_path / "state.db"),
        client_factory=factory,
    )

    missing = await runtime.connection_status()

    assert missing["success"] is True
    assert missing["data"]["connected"] is False
    assert missing["data"]["configuration_complete"] is False
    assert missing["data"]["missing_settings"] == [
        "BILLIT_API_KEY",
        "BILLIT_BASE_URL",
        "BILLIT_PARTY_ID",
    ]
    assert clients == []

    monkeypatch.setenv("BILLIT_API_KEY", "local-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.sandbox.billit.be/v1")
    monkeypatch.setenv("BILLIT_PARTY_ID", "1")

    connected = await runtime.connection_status()

    assert connected["success"] is True
    assert connected["data"]["connected"] is True
    assert connected["data"]["configuration_complete"] is True
    assert clients[0].settings.api_key == "local-key"


@pytest.mark.asyncio
async def test_local_stdio_tool_surface_is_curated_only() -> None:
    """The packaged stdio server exposes no raw legacy MCP tools."""

    tool_names = {tool.name for tool in await mcp_server.mcp.list_tools()}

    assert tool_names == LOCAL_API_KEY_TOOL_NAMES
    assert "create_order" not in tool_names
    assert "send_order" not in tool_names
    assert "delete_order" not in tool_names
    assert "download_file" not in tool_names
    assert "smart_search" not in tool_names


@pytest.mark.asyncio
async def test_local_runtime_sends_api_key_and_explicit_party_id_without_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    runtime, clients = _runtime(tmp_path, monkeypatch)

    result = await runtime.connection_status()

    assert result["success"] is True
    assert clients[0].client.headers["apiKey"] == "local-key"
    assert clients[0].client.headers["PartyID"] == "1"
    assert "ContextPartyID" not in clients[0].client.headers
    assert result["data"]["company_authorization"] == "verified"


@pytest.mark.asyncio
async def test_local_search_orders_uses_structured_filters(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    runtime, clients = _runtime(tmp_path, monkeypatch)

    result = await runtime.search_orders(
        direction="income",
        order_type="invoice",
        customer_name="O'Connor",
        limit=500,
    )

    assert result["success"] is True
    _, endpoint, kwargs = clients[0].calls[-1]
    assert endpoint == "/orders"
    assert kwargs["params"]["$top"] == 120
    assert "OrderDirection eq 'Income'" in kwargs["params"]["$filter"]
    assert "contains(Customer/Name,'O''Connor')" in kwargs["params"]["$filter"]


@pytest.mark.asyncio
async def test_local_write_gate_blocks_draft_before_billit_post(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    runtime, clients = _runtime(tmp_path, monkeypatch)

    result = await runtime.invoice_create_draft(
        customer={"name": "ACME"},
        lines=[{"description": "Work", "quantity": 1, "unit_price": 100}],
        order_date="2026-05-26",
        expiry_date="2026-06-25",
        idempotency_key="draft-1",
    )

    assert result["success"] is False
    assert result["error_code"] == "LOCAL_WRITES_DISABLED"
    assert not clients or all(call[0] != "POST" for call in clients[0].calls)


@pytest.mark.asyncio
async def test_local_create_draft_uses_idempotency_and_redacted_state(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    runtime, clients = _runtime(tmp_path, monkeypatch)
    monkeypatch.setenv("BILLIT_MCP_LOCAL_ALLOW_WRITES", "1")

    result = await runtime.invoice_create_draft(
        customer={"name": "ACME"},
        lines=[{"description": "Work", "quantity": 1, "unit_price": 100}],
        order_date="2026-05-26",
        expiry_date="2026-06-25",
        idempotency_key="draft-1",
    )
    replay = await runtime.invoice_create_draft(
        customer={"name": "ACME"},
        lines=[{"description": "Work", "quantity": 1, "unit_price": 100}],
        order_date="2026-05-26",
        expiry_date="2026-06-25",
        idempotency_key="draft-1",
    )

    assert result["success"] is True
    assert replay["data"]["idempotent_replay"] is True
    assert ("POST", "/orders") in [(method, endpoint) for method, endpoint, _ in clients[0].calls]
    assert b"ACME" not in (tmp_path / "state.db").read_bytes()
    assert any(event["event_type"] == "billit_api_call" for event in runtime.state.audit_events())


@pytest.mark.asyncio
async def test_local_confirm_send_refetches_consumes_once_and_redacts_challenge(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    runtime, clients = _runtime(tmp_path, monkeypatch)
    monkeypatch.setenv("BILLIT_MCP_LOCAL_ALLOW_SENDS", "1")

    prepared = await runtime.invoice_prepare_send(
        order_id=99,
        transport_type="Peppol",
        strict_transport=True,
    )
    challenge = prepared["data"]
    confirmed = await runtime.invoice_confirm_send(
        challenge_id=challenge["challenge_id"],
        confirmation_token=challenge["confirmation_token"],
        operation_hash=challenge["operation_hash"],
    )
    repeated = await runtime.invoice_confirm_send(
        challenge_id=challenge["challenge_id"],
        confirmation_token=challenge["confirmation_token"],
        operation_hash=challenge["operation_hash"],
    )

    assert prepared["success"] is True
    assert confirmed["success"] is True
    assert repeated["success"] is False
    assert repeated["error_code"] == "CHALLENGE_EXPIRED"
    assert ("POST", "/orders/commands/send") in [
        (method, endpoint) for method, endpoint, _ in clients[0].calls
    ]
    assert b"ACME" not in (tmp_path / "state.db").read_bytes()

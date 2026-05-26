"""Focused tests for the packaged MCP server helpers."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import pytest

import billit_mcp.server as mcp_server

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class FakeBillitClient:
    """Small async Billit client double for MCP helper tests."""

    def __init__(self) -> None:
        self.client = SimpleNamespace(is_closed=False)
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    async def request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((method, endpoint, kwargs))
        if endpoint == "/orders":
            return {
                "success": True,
                "data": {
                    "Items": [
                        {
                            "OrderID": 10,
                            "ToPay": 42.5,
                            "PaymentReference": "ABC",
                        }
                    ]
                },
                "error": None,
                "error_code": None,
            }
        if endpoint == "/financialTransactions":
            return {
                "success": True,
                "data": {
                    "Items": [
                        {
                            "FinancialTransactionID": 20,
                            "Amount": 42.5,
                            "PaymentReference": "ABC",
                        }
                    ]
                },
                "error": None,
                "error_code": None,
            }
        return {"success": True, "data": [], "error": None, "error_code": None}

    async def close(self) -> None:
        self.closed = True
        self.client.is_closed = True


@pytest.fixture(autouse=True)
async def reset_mcp_client() -> AsyncGenerator[None, None]:
    """Keep process-scoped MCP client state isolated between tests."""

    await mcp_server.close_mcp_client()
    yield
    await mcp_server.close_mcp_client()


@pytest.mark.asyncio
async def test_mcp_get_client_reuses_and_closes_process_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = FakeBillitClient()
    monkeypatch.setattr(mcp_server, "build_client", lambda: fake)

    first = await mcp_server.get_client()
    second = await mcp_server.get_client()
    await mcp_server.close_mcp_client()

    assert first is fake
    assert second is fake
    assert fake.closed is True


@pytest.mark.asyncio
async def test_mcp_composite_uses_shared_helpers_not_local_ai_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = FakeBillitClient()
    monkeypatch.setattr(mcp_server, "build_client", lambda: fake)

    result = await mcp_server.suggest_payment_reconciliation()

    assert result["success"] is True
    endpoints = [endpoint for _, endpoint, _ in fake.calls]
    assert "/orders" in endpoints
    assert "/financialTransactions" in endpoints
    assert all(not endpoint.startswith("/ai/") for endpoint in endpoints)


@pytest.mark.asyncio
async def test_mcp_reports_use_canonical_report_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeBillitClient()
    monkeypatch.setattr(mcp_server, "build_client", lambda: fake)

    await mcp_server.list_available_reports()
    await mcp_server.get_report("sales-summary", start="2024-01-01")

    assert ("GET", "/reports", {}) in fake.calls
    assert ("GET", "/reports/sales-summary", {"params": {"start": "2024-01-01"}}) in fake.calls


@pytest.mark.asyncio
async def test_mcp_list_tools_clamp_page_size(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeBillitClient()
    monkeypatch.setattr(mcp_server, "build_client", lambda: fake)

    await mcp_server.list_orders(skip=-10, top=500)

    assert ("GET", "/orders", {"params": {"$skip": 0, "$top": 120}}) in fake.calls

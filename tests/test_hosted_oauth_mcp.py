"""Hosted MCP OAuth and transport smoke tests."""

from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Any
from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient

from billit.client import BillitSettings
from billit_mcp.http_app import create_app
from billit_mcp.services.filters import compile_order_params
from billit_mcp.services.invoice import build_invoice_preflight

HOSTED_TOOL_NAMES = {
    "billit.connection_status",
    "billit.list_companies",
    "billit.search_orders",
    "billit.get_order",
    "billit.resolve_party",
    "billit.lookup_peppol_receiver",
    "billit.invoice.prepare",
    "billit.invoice.create_draft",
    "billit.invoice.prepare_send",
    "billit.invoice.confirm_send",
    "billit.invoice.get_delivery_status",
}


def test_hosted_oauth_flow_and_curated_mcp_tools(
    monkeypatch,
    tmp_path,
) -> None:
    """Hosted /mcp initializes and exposes only the hosted MVP tool surface."""

    monkeypatch.setenv(
        "BILLIT_MCP_DATABASE_URL",
        f"sqlite+aiosqlite:///{tmp_path / 'hosted.db'}",
    )
    client = TestClient(create_app(), base_url="http://localhost:8000")
    with client:
        token = _issue_token(client)
        headers = {
            "accept": "application/json, text/event-stream",
            "authorization": f"Bearer {token}",
        }
        init = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "0"},
            },
        }
        response = client.post("/mcp", json=init, headers=headers)
        assert response.status_code == 200

        response = client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            headers=headers,
        )
        assert response.status_code == 200
        tool_names = {tool["name"] for tool in response.json()["result"]["tools"]}
        assert tool_names == HOSTED_TOOL_NAMES
        assert "send_order" not in tool_names
        assert "delete_order" not in tool_names
        assert "billit.webhooks.create" not in tool_names


def test_hosted_oauth_rejects_code_reuse(monkeypatch, tmp_path) -> None:
    """MCP authorization codes are one-time use."""

    monkeypatch.setenv(
        "BILLIT_MCP_DATABASE_URL",
        f"sqlite+aiosqlite:///{tmp_path / 'hosted.db'}",
    )
    client = TestClient(create_app(), base_url="http://localhost:8000")
    with client:
        verifier, challenge = _pkce_pair()
        code = _authorize(client, challenge)
        first = _exchange(client, code=code, verifier=verifier)
        second = _exchange(client, code=code, verifier=verifier)

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["error"] == "invalid_grant"


def test_hosted_app_never_reads_local_billit_settings(
    monkeypatch,
    tmp_path,
) -> None:
    """Hosted startup must not fall back to API-key BillitSettings.from_env."""

    monkeypatch.setenv(
        "BILLIT_MCP_DATABASE_URL",
        f"sqlite+aiosqlite:///{tmp_path / 'hosted.db'}",
    )

    def fail_from_env() -> BillitSettings:
        raise AssertionError("hosted mode must not call BillitSettings.from_env()")

    monkeypatch.setattr(BillitSettings, "from_env", staticmethod(fail_from_env))
    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        assert client.get("/healthz").status_code == 200


def test_hosted_order_filters_are_structured_and_allowlisted() -> None:
    """Hosted search compiles structured filters and rejects OData-like injection."""

    params = compile_order_params(
        direction="income",
        order_type="invoice",
        customer_name="O'Connor",
        paid=False,
        limit=500,
    )

    assert params["$top"] == 120
    assert "OrderDirection eq 'Income'" in str(params["$filter"])
    assert "contains(Customer/Name,'O''Connor')" in str(params["$filter"])

    try:
        compile_order_params(customer_name="Name;delete", limit=1)
    except ValueError as exc:
        assert "Unsupported characters" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected OData-like customer name to be rejected")


def test_shared_invoice_preflight_has_no_write_side_effects() -> None:
    """Invoice prepare is a shared read-only preflight helper."""

    result = build_invoice_preflight(
        customer={"name": "ACME"},
        lines=[{"description": "Consulting", "quantity": 1, "unit_price": 100}],
        order_date="2026-05-26",
        expiry_date="2026-06-25",
        desired_transport="Peppol",
    )

    assert result["ready"] is True
    assert result["next_action"]["tool"] == "billit.invoice.create_draft"


def _issue_token(client: TestClient) -> str:
    verifier, challenge = _pkce_pair()
    code = _authorize(client, challenge)
    response = _exchange(client, code=code, verifier=verifier)
    assert response.status_code == 200
    return str(response.json()["access_token"])


def _authorize(client: TestClient, challenge: str) -> str:
    response = client.get(
        "/oauth/authorize",
        params={
            "response_type": "code",
            "client_id": "local-dev-client",
            "redirect_uri": "http://localhost:8765/callback",
            "scope": "billit:read billit:invoice.create billit:invoice.send",
            "state": "pytest-state",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        },
        follow_redirects=False,
    )
    assert response.status_code == 307
    location = response.headers["location"]
    return str(parse_qs(urlparse(location).query)["code"][0])


def _exchange(client: TestClient, *, code: str, verifier: str) -> Any:
    return client.post(
        "/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": "local-dev-client",
            "redirect_uri": "http://localhost:8765/callback",
            "code": code,
            "code_verifier": verifier,
        },
    )


def _pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge

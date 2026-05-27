"""Hosted MCP OAuth and transport smoke tests."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import secrets
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient
from sqlalchemy import select

from billit.client import BillitSettings
from billit_mcp.auth.billit_oauth import BillitOAuthBridge
from billit_mcp.auth.security import FernetCipher, JWTService, sha256_text
from billit_mcp.hosted_config import HostedSettings
from billit_mcp.http_app import create_app
from billit_mcp.persistence.database import HostedDatabase
from billit_mcp.persistence.migrations import run_migrations
from billit_mcp.persistence.models import (
    Actor,
    BillitCompany,
    BillitConnection,
    BillitOAuthGrant,
    IdempotencyRecord,
    OAuthClient,
)
from billit_mcp.services.filters import compile_order_params, compile_party_params
from billit_mcp.services.hosted_runtime import (
    HostedToolError,
    HostedToolRuntime,
    error_result,
    hash_payload,
)
from billit_mcp.services.invoice import build_invoice_payload, build_invoice_preflight

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
        _hosted_db_url(tmp_path),
    )
    run_migrations(_hosted_db_url(tmp_path))
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


def test_hosted_mcp_tools_call_through_curated_runtime(monkeypatch, tmp_path) -> None:
    """Hosted tool calls use the curated runtime, company checks, and Billit wrapper."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    run_migrations(_hosted_db_url(tmp_path))
    app = create_app()
    fake_client = FakeBillitClient()

    async def fake_make_client(*, connection_id: str, company_party_id: int) -> FakeBillitClient:
        assert connection_id
        assert company_party_id == 123
        return fake_client

    monkeypatch.setattr(app.state.hosted_billit_bridge, "make_client", fake_make_client)
    client = TestClient(app, base_url="http://localhost:8000")
    with client:
        token = _issue_token(client)
        claims = app.state.hosted_jwt_service.decode(token)
        asyncio.run(_seed_active_connection(app, str(claims["sub"]), 123))
        headers = _mcp_headers(token)
        _initialize_mcp(client, headers)

        tool_cases: list[tuple[str, dict[str, Any]]] = [
            ("billit.connection_status", {"environment": "sandbox"}),
            ("billit.list_companies", {"environment": "sandbox"}),
            (
                "billit.search_orders",
                {
                    "environment": "sandbox",
                    "company_party_id": 123,
                    "direction": "income",
                    "order_type": "invoice",
                },
            ),
            (
                "billit.get_order",
                {"environment": "sandbox", "company_party_id": 123, "order_id": 99},
            ),
            (
                "billit.resolve_party",
                {
                    "environment": "sandbox",
                    "company_party_id": 123,
                    "role": "customer",
                    "vat_number": "BE0123456789",
                },
            ),
            (
                "billit.lookup_peppol_receiver",
                {"environment": "sandbox", "company_party_id": 123, "identifier": "BE0123456789"},
            ),
            (
                "billit.invoice.prepare",
                {
                    "environment": "sandbox",
                    "company_party_id": 123,
                    "customer": {"name": "ACME"},
                    "lines": [{"description": "Work", "quantity": 1, "unit_price": 100}],
                    "order_date": "2026-05-26",
                    "expiry_date": "2026-06-25",
                },
            ),
            (
                "billit.invoice.create_draft",
                {
                    "environment": "sandbox",
                    "company_party_id": 123,
                    "customer": {"name": "ACME"},
                    "lines": [{"description": "Work", "quantity": 1, "unit_price": 100}],
                    "order_date": "2026-05-26",
                    "expiry_date": "2026-06-25",
                    "idempotency_key": "pytest-draft",
                },
            ),
            (
                "billit.invoice.get_delivery_status",
                {"environment": "sandbox", "company_party_id": 123, "order_id": 99},
            ),
        ]
        for name, arguments in tool_cases:
            assert _call_tool(client, headers, name, arguments)["isError"] is False

        prepare_send = _call_tool(
            client,
            headers,
            "billit.invoice.prepare_send",
            {
                "environment": "sandbox",
                "company_party_id": 123,
                "order_id": 99,
                "transport_type": "Peppol",
                "strict_transport": True,
            },
        )
        assert prepare_send["isError"] is False
        challenge = _tool_json(prepare_send)["data"]
        confirm_send = _call_tool(
            client,
            headers,
            "billit.invoice.confirm_send",
            {
                "environment": "sandbox",
                "company_party_id": 123,
                "challenge_id": challenge["challenge_id"],
                "confirmation_token": challenge["confirmation_token"],
                "operation_hash": challenge["operation_hash"],
            },
        )
        assert confirm_send["isError"] is False
        assert _tool_json(confirm_send)["success"] is True, _tool_json(confirm_send)

    assert ("POST", "/orders/commands/send") in fake_client.calls


def test_hosted_create_draft_blocks_unsafe_idempotency_replay(monkeypatch, tmp_path) -> None:
    """Hosted invoice draft replays do not repeat Billit writes for unsafe states."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    run_migrations(_hosted_db_url(tmp_path))
    app = create_app()
    fake_client = FakeBillitClient()

    async def fake_make_client(*, connection_id: str, company_party_id: int) -> FakeBillitClient:
        assert connection_id
        assert company_party_id == 123
        return fake_client

    monkeypatch.setattr(app.state.hosted_billit_bridge, "make_client", fake_make_client)
    client = TestClient(app, base_url="http://localhost:8000")
    with client:
        token = _issue_token(client)
        claims = app.state.hosted_jwt_service.decode(token)
        connection_id = asyncio.run(_seed_active_connection(app, str(claims["sub"]), 123))
        operation_hash = hash_payload(
            build_invoice_payload(
                customer={"name": "ACME"},
                lines=[{"description": "Work", "quantity": 1, "unit_price": 100}],
                order_date="2026-05-26",
                expiry_date="2026-06-25",
                external_provider_id=None,
            )
        )
        asyncio.run(
            _seed_hosted_idempotency(
                app,
                connection_id=connection_id,
                operation_hash=operation_hash,
                status="started",
            )
        )
        headers = _mcp_headers(token)
        _initialize_mcp(client, headers)

        result = _call_tool(
            client,
            headers,
            "billit.invoice.create_draft",
            {
                "environment": "sandbox",
                "company_party_id": 123,
                "customer": {"name": "ACME"},
                "lines": [{"description": "Work", "quantity": 1, "unit_price": 100}],
                "order_date": "2026-05-26",
                "expiry_date": "2026-06-25",
                "idempotency_key": "pytest-draft",
            },
        )

    payload = _tool_json(result)
    assert payload["success"] is False
    assert payload["error_code"] == "IDEMPOTENCY_REPLAY_BLOCKED"
    assert ("POST", "/orders") not in fake_client.calls


def test_hosted_create_draft_replays_succeeded_idempotency(monkeypatch, tmp_path) -> None:
    """Hosted invoice draft replay returns the stored order id without a Billit write."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    run_migrations(_hosted_db_url(tmp_path))
    app = create_app()
    fake_client = FakeBillitClient()

    async def fake_make_client(*, connection_id: str, company_party_id: int) -> FakeBillitClient:
        assert connection_id
        assert company_party_id == 123
        return fake_client

    monkeypatch.setattr(app.state.hosted_billit_bridge, "make_client", fake_make_client)
    client = TestClient(app, base_url="http://localhost:8000")
    with client:
        token = _issue_token(client)
        claims = app.state.hosted_jwt_service.decode(token)
        connection_id = asyncio.run(_seed_active_connection(app, str(claims["sub"]), 123))
        operation_hash = hash_payload(
            build_invoice_payload(
                customer={"name": "ACME"},
                lines=[{"description": "Work", "quantity": 1, "unit_price": 100}],
                order_date="2026-05-26",
                expiry_date="2026-06-25",
                external_provider_id=None,
            )
        )
        asyncio.run(
            _seed_hosted_idempotency(
                app,
                connection_id=connection_id,
                operation_hash=operation_hash,
                status="succeeded",
                billit_resource_id="99",
            )
        )
        headers = _mcp_headers(token)
        _initialize_mcp(client, headers)

        result = _call_tool(
            client,
            headers,
            "billit.invoice.create_draft",
            {
                "environment": "sandbox",
                "company_party_id": 123,
                "customer": {"name": "ACME"},
                "lines": [{"description": "Work", "quantity": 1, "unit_price": 100}],
                "order_date": "2026-05-26",
                "expiry_date": "2026-06-25",
                "idempotency_key": "pytest-draft",
            },
        )

    payload = _tool_json(result)
    assert payload["success"] is True
    assert payload["data"] == {"idempotent_replay": True, "order_id": "99"}
    assert ("POST", "/orders") not in fake_client.calls


def test_hosted_oauth_rejects_code_reuse(monkeypatch, tmp_path) -> None:
    """MCP authorization codes are one-time use."""

    monkeypatch.setenv(
        "BILLIT_MCP_DATABASE_URL",
        _hosted_db_url(tmp_path),
    )
    run_migrations(_hosted_db_url(tmp_path))
    client = TestClient(create_app(), base_url="http://localhost:8000")
    with client:
        verifier, challenge = _pkce_pair()
        code = _authorize(client, challenge)
        first = _exchange(client, code=code, verifier=verifier)
        second = _exchange(client, code=code, verifier=verifier)

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["error"] == "invalid_grant"


def test_hosted_metadata_and_oauth_error_paths(monkeypatch, tmp_path) -> None:
    """Metadata endpoints and OAuth failures are reachable without schema mutation."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    run_migrations(_hosted_db_url(tmp_path))
    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        assert client.get("/.well-known/oauth-protected-resource").status_code == 200
        assert client.get("/.well-known/oauth-authorization-server").status_code == 200
        assert client.get("/oauth/jwks.json").status_code == 200
        assert client.get("/privacy").status_code == 200
        assert client.get("/docs").status_code == 200

        authorize_error = client.get(
            "/oauth/authorize",
            params={
                "response_type": "token",
                "client_id": "local-dev-client",
            },
        )
        assert authorize_error.status_code == 400
        assert authorize_error.json()["error"] == "unsupported_response_type"

        token_error = client.post("/oauth/token", data={"grant_type": "refresh_token"})
        assert token_error.status_code == 400
        assert token_error.json()["error"] == "unsupported_grant_type"

        assert client.post("/oauth/revoke", data={}).status_code == 200
        assert client.get("/billit/callback").status_code == 400
        denied = client.get("/billit/callback", params={"error": "access_denied"})
        assert denied.status_code == 400


def test_hosted_app_never_reads_local_billit_settings(
    monkeypatch,
    tmp_path,
) -> None:
    """Hosted startup must not fall back to API-key BillitSettings.from_env."""

    monkeypatch.setenv(
        "BILLIT_MCP_DATABASE_URL",
        _hosted_db_url(tmp_path),
    )
    run_migrations(_hosted_db_url(tmp_path))

    def fail_from_env() -> BillitSettings:
        raise AssertionError("hosted mode must not call BillitSettings.from_env()")

    monkeypatch.setattr(BillitSettings, "from_env", staticmethod(fail_from_env))
    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        assert client.get("/healthz").status_code == 200


def test_hosted_readyz_requires_migration(monkeypatch, tmp_path) -> None:
    """Hosted readiness proves the DB is migrated instead of mutating schema."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))

    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        response = client.get("/readyz")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "unready"
    assert body["database"]["expected_revision"] == "20260526_0001"


def test_hosted_readyz_reports_migrated_head(monkeypatch, tmp_path) -> None:
    """Hosted readiness reports DB connectivity and the exact Alembic head."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    run_migrations(_hosted_db_url(tmp_path))

    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        response = client.get("/readyz")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"]["connected"] is True
    assert body["database"]["alembic_revision"] == "20260526_0001"


def test_hosted_migration_is_explicit_ddl() -> None:
    """Historical migrations must not import live ORM metadata."""

    migration = "alembic/versions/20260526_0001_hosted_oauth_schema.py"
    text = Path(migration).read_text()

    assert "Base" not in text
    assert "metadata.create_all" not in text
    assert "metadata.drop_all" not in text


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


def test_hosted_filter_and_invoice_blocker_edges() -> None:
    """Hosted filter compilers reject unsupported values and invoice blockers are explicit."""

    invalid_filter_calls = [
        lambda: compile_order_params(direction="sideways"),
        lambda: compile_order_params(order_type="receipt"),
        lambda: compile_order_params(modified_since="not-a-date"),
    ]
    for invalid_filter_call in invalid_filter_calls:
        try:
            invalid_filter_call()
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError("expected filter rejection")

    supplier = compile_party_params(role="supplier", email="supplier@example.test")
    assert "PartyType eq 'Supplier'" in str(supplier["$filter"])
    try:
        compile_party_params(role="customer", name="ACME or PartyType eq 'Supplier'")
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected OData-looking party name to be rejected")

    preflight = build_invoice_preflight(
        customer={},
        lines=[{"quantity": None, "unit_price": None}],
        order_date="",
        expiry_date="",
    )
    assert preflight["ready"] is False
    assert len(preflight["blockers"]) >= 5


def test_hosted_party_filters_require_strict_role() -> None:
    """Party resolution accepts only customer or supplier roles."""

    params = compile_party_params(role="customer", vat_number="BE0123456789")
    assert "PartyType eq 'Customer'" in str(params["$filter"])

    try:
        compile_party_params(role="vendor", name="ACME")
    except ValueError as exc:
        assert "customer or supplier" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected invalid party role to be rejected")


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


async def test_company_sync_deactivates_stale_companies(monkeypatch, tmp_path) -> None:
    """Successful accountInformation sync is authoritative for company access."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    await asyncio.to_thread(run_migrations, _hosted_db_url(tmp_path))
    database, _, bridge = _runtime_parts(tmp_path)
    try:
        async with database.session() as session:
            actor = Actor(subject_hash="actor-hash")
            session.add(actor)
            await session.flush()
            connection = BillitConnection(
                actor_id=actor.actor_id,
                environment="sandbox",
                status="active",
            )
            session.add(connection)
            await session.flush()
            connection_id = connection.connection_id

        assert (
            await bridge.sync_companies_from_items(
                connection_id=connection_id,
                environment="sandbox",
                companies=[{"PartyID": 1}, {"PartyID": 2}],
            )
        ) == 2
        assert (
            await bridge.sync_companies_from_items(
                connection_id=connection_id,
                environment="sandbox",
                companies=[{"PartyID": 2}],
            )
        ) == 1

        async with database.session() as session:
            companies = (
                await session.scalars(
                    select(BillitCompany).where(BillitCompany.connection_id == connection_id)
                )
            ).all()

        states = {company.company_party_id: company.active for company in companies}
        assert states == {1: False, 2: True}
    finally:
        await database.close()


async def test_confirmation_mismatch_does_not_consume(monkeypatch, tmp_path) -> None:
    """Wrong company/env details cannot burn a valid confirmation challenge."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    await asyncio.to_thread(run_migrations, _hosted_db_url(tmp_path))
    database, runtime, _ = _runtime_parts(tmp_path)
    try:
        async with database.session() as session:
            actor = Actor(subject_hash="actor-hash")
            client = OAuthClient(
                client_id="client",
                redirect_uris=["http://localhost/callback"],
                allowed_scopes=["billit:invoice.send"],
            )
            session.add_all([actor, client])
            await session.flush()
            connection = BillitConnection(
                actor_id=actor.actor_id,
                environment="sandbox",
                status="active",
            )
            session.add(connection)
            await session.flush()
            actor_id = actor.actor_id
            connection_id = connection.connection_id

        challenge = await runtime.create_confirmation_challenge(
            actor_id=actor_id,
            client_id="client",
            connection_id=connection_id,
            environment="sandbox",
            company_party_id=123,
            operation_type="invoice_send",
            resource_type="order",
            resource_id="99",
            required_scope="billit:invoice.send",
            summary={"order_id": 99, "company_party_id": 123},
        )
        try:
            await runtime.consume_confirmation_challenge(
                challenge_id=str(challenge["challenge_id"]),
                confirmation_token=str(challenge["confirmation_token"]),
                operation_hash=str(challenge["operation_hash"]),
                actor_id=actor_id,
                client_id="client",
                connection_id=connection_id,
                environment="sandbox",
                company_party_id=456,
                operation_type="invoice_send",
                resource_type="order",
                resource_id="99",
                required_scope="billit:invoice.send",
            )
        except HostedToolError as exc:
            assert exc.error_type == "challenge_mismatch"
        else:  # pragma: no cover
            raise AssertionError("expected mismatched company to be rejected")

        pending = await runtime.get_pending_confirmation_challenge(
            challenge_id=str(challenge["challenge_id"]),
            actor_id=actor_id,
            client_id="client",
            environment="sandbox",
            company_party_id=123,
            operation_type="invoice_send",
            resource_type="order",
            required_scope="billit:invoice.send",
        )
        assert pending.status == "pending"
    finally:
        await database.close()


async def test_runtime_idempotency_and_error_helpers(monkeypatch, tmp_path) -> None:
    """Runtime helper branches stay covered without live Billit calls."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    await asyncio.to_thread(run_migrations, _hosted_db_url(tmp_path))
    database, runtime, _ = _runtime_parts(tmp_path)
    try:
        assert error_result(RuntimeError("boom"))["error_code"] == "HOSTED_TOOL_ERROR"
        assert HostedToolError("x", "message").to_result()["error"]["type"] == "x"
        async with database.session() as session:
            actor = Actor(subject_hash="actor-hash")
            session.add(actor)
            await session.flush()
            connection = BillitConnection(
                actor_id=actor.actor_id,
                environment="sandbox",
                status="active",
            )
            session.add(connection)
            await session.flush()
            connection_id = connection.connection_id

        first = await runtime.record_idempotency_started(
            connection_id=connection_id,
            company_party_id=123,
            operation_type="invoice_create_draft",
            idempotency_key="idem",
            operation_hash=hash_payload({"a": 1}),
        )
        replay = await runtime.record_idempotency_started(
            connection_id=connection_id,
            company_party_id=123,
            operation_type="invoice_create_draft",
            idempotency_key="idem",
            operation_hash=hash_payload({"a": 1}),
        )
        assert first.created is True
        assert replay.created is False
        assert replay.record.idempotency_id == first.record.idempotency_id
        await runtime.record_idempotency_outcome(
            idempotency_id=first.record.idempotency_id,
            status="conflict",
            billit_error_code="409",
        )
        try:
            await runtime.record_idempotency_outcome(
                idempotency_id=first.record.idempotency_id,
                status="done",
            )
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError("expected unsupported idempotency state to fail")
    finally:
        await database.close()


async def test_billit_oauth_current_token_and_make_client_do_not_use_env(
    monkeypatch, tmp_path
) -> None:
    """Hosted Billit clients use stored OAuth grant material and explicit PartyID."""

    monkeypatch.setenv("BILLIT_MCP_DATABASE_URL", _hosted_db_url(tmp_path))
    await asyncio.to_thread(run_migrations, _hosted_db_url(tmp_path))
    database, _, bridge = _runtime_parts(tmp_path)
    try:
        async with database.session() as session:
            actor = Actor(subject_hash="actor-hash")
            session.add(actor)
            await session.flush()
            connection = BillitConnection(
                actor_id=actor.actor_id,
                environment="sandbox",
                status="active",
            )
            session.add(connection)
            await session.flush()
            session.add(
                BillitOAuthGrant(
                    connection_id=connection.connection_id,
                    access_token_ciphertext=bridge.cipher.encrypt("stored-access"),
                    access_token_expires_at=datetime.now(UTC) + timedelta(hours=1),
                    refresh_token_ciphertext=bridge.cipher.encrypt("stored-refresh"),
                    refresh_token_hash="stored-refresh-hash",
                    encryption_context={"environment": "sandbox"},
                    updated_at=datetime.now(UTC),
                )
            )
            connection_id = connection.connection_id

        token = await bridge.get_billit_access_token(connection_id=connection_id)
        client = await bridge.make_client(connection_id=connection_id, company_party_id=123)
        try:
            assert token == "stored-access"
            assert client.client.headers["Authorization"] == "Bearer stored-access"
            assert client.client.headers["PartyID"] == "123"
            assert "apiKey" not in client.client.headers
        finally:
            await client.close()
    finally:
        await database.close()


def _issue_token(client: TestClient) -> str:
    verifier, challenge = _pkce_pair()
    code = _authorize(client, challenge)
    response = _exchange(client, code=code, verifier=verifier)
    assert response.status_code == 200
    return str(response.json()["access_token"])


def _mcp_headers(token: str) -> dict[str, str]:
    return {
        "accept": "application/json, text/event-stream",
        "authorization": f"Bearer {token}",
    }


def _initialize_mcp(client: TestClient, headers: dict[str, str]) -> None:
    response = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 101,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "0"},
            },
        },
        headers=headers,
    )
    assert response.status_code == 200


def _call_tool(
    client: TestClient,
    headers: dict[str, str],
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    response = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": secrets.randbelow(10_000),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        headers=headers,
    )
    assert response.status_code == 200
    return dict(response.json()["result"])


def _tool_json(result: dict[str, Any]) -> dict[str, Any]:
    parsed = json.loads(result["content"][0]["text"])
    assert isinstance(parsed, dict)
    return parsed


def _hosted_db_url(tmp_path: Any) -> str:
    return f"sqlite+aiosqlite:///{tmp_path / 'hosted.db'}"


def _runtime_parts(tmp_path: Any) -> tuple[HostedDatabase, HostedToolRuntime, BillitOAuthBridge]:
    settings = HostedSettings.from_env()
    database = HostedDatabase(_hosted_db_url(tmp_path))
    bridge = BillitOAuthBridge(database, settings, FernetCipher.from_settings(settings))
    runtime = HostedToolRuntime(
        settings=settings,
        database=database,
        jwt_service=JWTService(settings),
        billit_bridge=bridge,
    )
    return database, runtime, bridge


async def _seed_active_connection(app: Any, actor_id: str, company_party_id: int) -> str:
    async with app.state.hosted_database.session() as session:
        connection = BillitConnection(
            actor_id=actor_id,
            environment="sandbox",
            status="active",
            connected_at=datetime.now(UTC),
        )
        session.add(connection)
        await session.flush()
        session.add(
            BillitCompany(
                connection_id=connection.connection_id,
                environment="sandbox",
                company_party_id=company_party_id,
                active=True,
                last_seen_at=datetime.now(UTC),
            )
        )
        return str(connection.connection_id)


async def _seed_hosted_idempotency(
    app: Any,
    *,
    connection_id: str,
    operation_hash: str,
    status: str,
    billit_resource_id: str | None = None,
) -> None:
    async with app.state.hosted_database.session() as session:
        session.add(
            IdempotencyRecord(
                connection_id=connection_id,
                company_party_id=123,
                operation_type="invoice_create_draft",
                idempotency_key_hash=sha256_text("pytest-draft"),
                operation_hash=operation_hash,
                status=status,
                billit_resource_type="order" if billit_resource_id else None,
                billit_resource_id=billit_resource_id,
            )
        )


class FakeBillitClient:
    """Small fake for hosted MCP tool-call coverage."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((method.upper(), url))
        if method.upper() == "POST" and url == "/orders":
            return {"success": True, "data": {"OrderID": 99}, "error": None, "error_code": None}
        if method.upper() == "POST" and url == "/orders/commands/send":
            return {"success": True, "data": {"sent": True}, "error": None, "error_code": None}
        if url == "/orders/99":
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
        if url == "/orders":
            return {
                "success": True,
                "data": {"Items": [{"OrderID": 99}]},
                "error": None,
                "error_code": None,
            }
        if url == "/parties":
            return {
                "success": True,
                "data": {"Items": [{"PartyID": 7}]},
                "error": None,
                "error_code": None,
            }
        if url.startswith("/peppol/participantInformation/"):
            return {
                "success": True,
                "data": {"registered": True},
                "error": None,
                "error_code": None,
            }
        return {"success": True, "data": {}, "error": None, "error_code": None}

    async def close(self) -> None:
        return None


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

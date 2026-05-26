"""Read-only live canary for hosted OAuth mode."""

from __future__ import annotations

import asyncio
import json
import os
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from scripts.local.billit_canary.shared import (
    ReadOnlyBillitClient,
    environment_name,
    probe_record,
    resolve_canary_party_id,
)
from sqlalchemy import select

from billit.client import BillitAPIClient, BillitOAuthSettings
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.smart_search import normalize_items
from billit_mcp.auth.billit_oauth import BillitOAuthBridge
from billit_mcp.auth.security import FernetCipher, JWTService, sha256_text
from billit_mcp.hosted_config import HostedSettings
from billit_mcp.persistence.database import HostedDatabase
from billit_mcp.persistence.migrations import HOSTED_ALEMBIC_HEAD, run_migrations, stamp_migrations
from billit_mcp.persistence.models import Actor, BillitCompany, BillitConnection, BillitOAuthGrant
from billit_mcp.services.hosted_runtime import HostedToolRuntime
from billit_mcp.services.invoice import build_invoice_preflight

HOSTED_TABLES = {
    "actors",
    "oauth_clients",
    "oauth_authorization_transactions",
    "oauth_auth_codes",
    "oauth_token_revocations",
    "billit_connections",
    "billit_oauth_grants",
    "billit_companies",
    "confirmation_challenges",
    "idempotency_records",
    "audit_events",
}


async def run_hosted_oauth_canary(
    *,
    base_url: str,
    output_root: Path,
    write_override_requested: bool = False,
) -> Path:
    """Run the hosted OAuth read-only canary against a pre-seeded local grant."""

    if environment_name(base_url) != "sandbox":
        raise SystemExit("hosted-oauth-readonly canary only runs against sandbox.")
    party_id = resolve_canary_party_id(sandbox=True)
    settings = HostedSettings.from_env()
    database = HostedDatabase(settings.database_url)
    jwt_service = JWTService(settings)
    bridge = BillitOAuthBridge(database, settings, FernetCipher.from_settings(settings))
    runtime = HostedToolRuntime(
        settings=settings,
        database=database,
        jwt_service=jwt_service,
        billit_bridge=bridge,
    )
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)

    probes: list[dict[str, Any]] = []
    try:
        migration_state = await ensure_hosted_canary_schema(settings.database_url)
        connection = await _resolve_hosted_canary_connection(database)
        await _force_hosted_refresh(database, connection.connection_id)
        token = await bridge.get_billit_access_token(connection_id=connection.connection_id)
        raw_client = BillitAPIClient(
            BillitOAuthSettings(
                base_url=base_url,
                access_token=token,
                party_id=party_id,
            )
        )
        client = ReadOnlyBillitClient(raw_client, allow_writes=False)
        try:
            account_endpoint = "/account/accountInformation"
            account_resp = await client.request("GET", account_endpoint)
            probes.append(probe_record(account_endpoint, account_resp))

            await _sync_canary_companies(
                bridge=bridge,
                connection_id=connection.connection_id,
                environment="sandbox",
                party_id=party_id,
                account_data=account_resp.get("data"),
            )
            await runtime.validate_company(
                connection_id=connection.connection_id,
                environment="sandbox",
                company_party_id=int(party_id),
            )
            probes.append(
                {
                    "endpoint": "hosted:company_party_id_validation",
                    "success": True,
                    "error_code": None,
                    "item_count": 1,
                }
            )

            params = list_params(skip=None, top=5)
            for endpoint in ["/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT]:
                response = await client.request("GET", endpoint, params=params)
                probes.append(probe_record(endpoint, response))

            reports_endpoint = report_endpoint()
            reports_resp = await client.request("GET", reports_endpoint)
            probes.append(probe_record(reports_endpoint, reports_resp))

            preflight = build_invoice_preflight(
                customer={"name": "Live canary placeholder"},
                lines=[
                    {
                        "description": "Read-only canary line",
                        "quantity": 1,
                        "unit_price": 1,
                        "vat_percentage": 21,
                    }
                ],
                order_date=datetime.now(UTC).date().isoformat(),
                expiry_date=(datetime.now(UTC) + timedelta(days=30)).date().isoformat(),
                desired_transport="Peppol",
            )
            probes.append(
                {
                    "endpoint": "hosted:invoice.prepare",
                    "success": bool(preflight["ready"]),
                    "error_code": None,
                    "item_count": len(preflight["blockers"]),
                }
            )
        finally:
            await client.close()
    finally:
        await database.close()

    passed = all(
        [
            any(
                probe["endpoint"] == "/account/accountInformation" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"]
                in {"/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT}
                and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == FINANCIAL_TRANSACTIONS_ENDPOINT and probe["success"]
                for probe in probes
            ),
            any(probe["endpoint"] == report_endpoint() and probe["success"] for probe in probes),
            any(
                probe["endpoint"] == "hosted:company_party_id_validation" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "hosted:invoice.prepare" and probe["success"]
                for probe in probes
            ),
        ]
    )
    report = {
        "timestamp": timestamp,
        "mode": "hosted-oauth-readonly",
        "environment": "sandbox",
        "base_url_host": base_url.replace("https://", "").replace("http://", "").split("/")[0],
        "read_only": True,
        "writes_enabled": False,
        "write_override_ignored": write_override_requested,
        "party_id_present": True,
        "hosted_oauth_refresh_forced": True,
        "hosted_schema_state": migration_state,
        "endpoint_decisions": {
            "financial_transactions": FINANCIAL_TRANSACTIONS_ENDPOINT,
            "reports": report_endpoint(),
        },
        "probes": probes,
        "passed": passed,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if not passed:
        raise SystemExit(f"Hosted OAuth live canary failed; sanitized report: {report_path}")
    return report_path


async def ensure_hosted_canary_schema(database_url: str) -> str:
    """Run migrations, or stamp a compatible local SQLite schema from old canary runs."""

    try:
        await asyncio.to_thread(run_migrations, database_url)
        return "migrated_or_current"
    except Exception:
        if not _can_stamp_existing_local_sqlite_schema(database_url):
            raise
        await asyncio.to_thread(stamp_migrations, database_url)
        return "stamped_existing_local_sqlite_schema"


def _can_stamp_existing_local_sqlite_schema(database_url: str) -> bool:
    """Return true for local SQLite hosted DBs that already have all hosted tables."""

    path = _sqlite_file_path(database_url)
    if path is None or not path.exists():
        return False
    connection = sqlite3.connect(path)
    try:
        tables = {
            str(row[0])
            for row in connection.execute(
                "select name from sqlite_master where type = 'table'"
            ).fetchall()
        }
        if not HOSTED_TABLES.issubset(tables):
            return False
        if "alembic_version" not in tables:
            return True
        revisions = [
            str(row[0])
            for row in connection.execute("select version_num from alembic_version").fetchall()
        ]
        return not revisions or revisions == [HOSTED_ALEMBIC_HEAD]
    finally:
        connection.close()


def _sqlite_file_path(database_url: str) -> Path | None:
    prefix = "sqlite+aiosqlite:///"
    if not database_url.startswith(prefix):
        return None
    raw_path = unquote(database_url.removeprefix(prefix))
    if raw_path == ":memory:":
        return None
    return Path(raw_path)


async def _resolve_hosted_canary_connection(database: HostedDatabase) -> BillitConnection:
    """Find the pre-seeded sandbox OAuth grant used by hosted canary mode."""

    connection_id = os.getenv("BILLIT_MCP_CANARY_CONNECTION_ID")
    actor_subject = os.getenv("BILLIT_MCP_CANARY_ACTOR_SUBJECT", "local-dev-actor")
    async with database.session() as session:
        if connection_id:
            connection = await session.get(BillitConnection, connection_id)
        else:
            actor = await session.scalar(
                select(Actor).where(Actor.subject_hash == sha256_text(actor_subject))
            )
            connection = None
            if actor is not None:
                connection = await session.scalar(
                    select(BillitConnection).where(
                        BillitConnection.actor_id == actor.actor_id,
                        BillitConnection.environment == "sandbox",
                    )
                )
        if connection is None:
            raise SystemExit(
                "hosted-oauth-readonly requires a pre-seeded sandbox Billit OAuth grant. "
                "Set BILLIT_MCP_CANARY_CONNECTION_ID or seed local-dev-actor first."
            )
        if connection.environment != "sandbox":
            raise SystemExit("hosted-oauth-readonly requires a sandbox Billit connection.")
        if connection.status != "active":
            raise SystemExit(f"Billit connection is not active: {connection.status}")
        session.expunge(connection)
        return connection


async def _force_hosted_refresh(database: HostedDatabase, connection_id: str) -> None:
    """Force the hosted canary through the refresh-token rotation code path."""

    async with database.session() as session:
        grant = await session.get(BillitOAuthGrant, connection_id, with_for_update=True)
        if grant is None:
            raise SystemExit("hosted-oauth-readonly requires a stored Billit OAuth grant.")
        grant.access_token_expires_at = datetime.now(UTC) - timedelta(seconds=1)


async def _sync_canary_companies(
    *,
    bridge: BillitOAuthBridge,
    connection_id: str,
    environment: str,
    party_id: str,
    account_data: Any,
) -> None:
    """Sync accountInformation companies, falling back to the explicit sandbox PartyID."""

    companies = normalize_items(account_data)
    if isinstance(account_data, dict):
        companies.append(account_data)
    if not companies:
        companies = [{"PartyID": party_id}]
    await bridge.sync_companies_from_items(
        connection_id=connection_id,
        environment=environment,
        companies=companies,
    )
    async with bridge.database.session() as session:
        explicit = await session.scalar(
            select(BillitCompany).where(
                BillitCompany.connection_id == connection_id,
                BillitCompany.environment == environment,
                BillitCompany.company_party_id == int(party_id),
            )
        )
        if explicit is None:
            session.add(
                BillitCompany(
                    connection_id=connection_id,
                    environment=environment,
                    company_party_id=int(party_id),
                    company_name_hash=sha256_text("explicit-canary-party-id"),
                    last_seen_at=datetime.now(UTC),
                )
            )

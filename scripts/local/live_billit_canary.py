"""Local read-only Billit canary with sanitized evidence output."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from dotenv import load_dotenv
from sqlalchemy import select

from billit.client import BillitAPIClient, BillitOAuthSettings, BillitSettings
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.services.ai_composite import generate_invoice_summary
from billit.smart_search import normalize_items
from billit_mcp.auth.billit_oauth import BillitOAuthBridge
from billit_mcp.auth.security import FernetCipher, JWTService, sha256_text
from billit_mcp.hosted_config import HostedSettings
from billit_mcp.persistence.database import HostedDatabase
from billit_mcp.persistence.models import Actor, BillitCompany, BillitConnection, BillitOAuthGrant
from billit_mcp.services.hosted_runtime import HostedToolRuntime
from billit_mcp.services.invoice import build_invoice_preflight

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
        env_key = first_present_env("BILLIT_SANDBOX_API_KEY_K4K", "BILLIT_SANDBOX_API_KEY")
        if env_key is not None:
            api_key, key_source = env_key
        else:
            keychain_secret = keychain_reader(SANDBOX_KEYCHAIN_SERVICE)
            if keychain_secret:
                api_key = keychain_secret
                key_source = f"keychain:{SANDBOX_KEYCHAIN_SERVICE}"
            else:
                generic_key = first_present_env("BILLIT_API_KEY")
                if generic_key is None:
                    raise SystemExit(
                        "Sandbox canary requires BILLIT_SANDBOX_API_KEY_K4K, "
                        f"BILLIT_SANDBOX_API_KEY, Keychain service {SANDBOX_KEYCHAIN_SERVICE}, "
                        "or BILLIT_API_KEY."
                    )
                api_key, key_source = generic_key
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
            context_party_id=os.getenv("BILLIT_CONTEXT_PARTY_ID"),
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


async def run_canary(
    *,
    base_url: str = SANDBOX_BASE_URL,
    output_root: Path = Path(".local/billit-live-canary"),
    allow_writes: bool = False,
    mode: str = "legacy-api-key-readonly",
    keychain_reader: Callable[[str], str | None] = read_keychain_secret,
    client_factory: Callable[[BillitSettings], CanaryClient] = BillitAPIClient,
) -> Path:
    """Run the selected local live Billit canary mode."""

    if mode == "legacy-api-key-readonly":
        return await _run_legacy_api_key_canary(
            base_url=base_url,
            output_root=output_root,
            allow_writes=allow_writes,
            keychain_reader=keychain_reader,
            client_factory=client_factory,
        )
    if mode == "hosted-oauth-readonly":
        return await _run_hosted_oauth_canary(
            base_url=base_url,
            output_root=output_root,
            allow_writes=allow_writes,
        )
    raise SystemExit(f"Unsupported live canary mode: {mode}")


async def _run_legacy_api_key_canary(
    *,
    base_url: str,
    output_root: Path,
    allow_writes: bool,
    keychain_reader: Callable[[str], str | None],
    client_factory: Callable[[BillitSettings], CanaryClient],
) -> Path:
    """Run the legacy local/private API-key canary path."""

    settings = resolve_canary_settings(base_url, keychain_reader=keychain_reader)
    raw_client = client_factory(settings.billit)
    client = ReadOnlyBillitClient(raw_client, allow_writes=allow_writes)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)

    probes: list[dict[str, Any]] = []
    try:
        account_endpoint = "/account/accountInformation"
        account_resp = await client.request("GET", account_endpoint)
        probes.append(probe_record(account_endpoint, account_resp))

        for endpoint in ["/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT]:
            response = await client.request("GET", endpoint, params=list_params(skip=None, top=5))
            probes.append(probe_record(endpoint, response))

        reports_endpoint = report_endpoint()
        reports_resp = await client.request("GET", reports_endpoint)
        probes.append(probe_record(reports_endpoint, reports_resp))

        composite_resp = await generate_invoice_summary(client, "2000-01-01", "2099-12-31")
        probes.append(probe_record("composite:generate_invoice_summary", composite_resp))
    finally:
        await client.close()

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
                probe["endpoint"] == "composite:generate_invoice_summary" and probe["success"]
                for probe in probes
            ),
        ]
    )

    report = {
        "timestamp": timestamp,
        "mode": "legacy-api-key-readonly",
        "environment": settings.environment,
        "base_url_host": base_url.replace("https://", "").replace("http://", "").split("/")[0],
        "read_only": True,
        "writes_enabled": allow_writes,
        "key_source": settings.key_source,
        "keychain_service": SANDBOX_KEYCHAIN_SERVICE,
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
        raise SystemExit(f"Live Billit canary failed; sanitized report: {report_path}")
    return report_path


async def _run_hosted_oauth_canary(
    *,
    base_url: str,
    output_root: Path,
    allow_writes: bool,
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
        await database.create_all()
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
        client = ReadOnlyBillitClient(raw_client, allow_writes=allow_writes)
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
        "writes_enabled": allow_writes,
        "party_id_present": True,
        "hosted_oauth_refresh_forced": True,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--read-only",
        action="store_true",
        help="Required acknowledgement that this canary will not perform writes.",
    )
    parser.add_argument(
        "--base-url",
        default=SANDBOX_BASE_URL,
        help="Billit API base URL. Defaults to sandbox.",
    )
    parser.add_argument(
        "--output-root",
        default=Path(".local/billit-live-canary"),
        type=Path,
        help="Directory for sanitized canary evidence.",
    )
    parser.add_argument(
        "--mode",
        choices=["legacy-api-key-readonly", "hosted-oauth-readonly"],
        default="legacy-api-key-readonly",
        help="Canary mode. Hosted mode requires a pre-seeded sandbox OAuth grant.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    if os.getenv("CI"):
        raise SystemExit("Refusing to run the live Billit canary in CI.")
    if not args.read_only:
        raise SystemExit("Pass --read-only to acknowledge that no write probes will run.")
    if args.base_url != SANDBOX_BASE_URL and os.getenv("BILLIT_LIVE_CANARY_ENV") != "production":
        raise SystemExit(
            "Non-sandbox canary runs require BILLIT_LIVE_CANARY_ENV=production "
            "and still remain read-only."
        )

    allow_writes = os.getenv("BILLIT_LIVE_CANARY_ALLOW_WRITES") == "1"
    report_path = asyncio.run(
        run_canary(
            base_url=args.base_url,
            output_root=args.output_root,
            allow_writes=allow_writes,
            mode=args.mode,
        )
    )
    print(f"Live Billit canary passed; sanitized report: {report_path}")


if __name__ == "__main__":
    main()

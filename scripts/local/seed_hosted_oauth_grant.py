"""Seed a local hosted Billit OAuth grant from existing sandbox tokens.

This helper intentionally does not automate Billit login. It imports an
already-obtained Billit OAuth access/refresh token pair into the local hosted
database, fetches accountInformation with the access token, syncs authorized
companies, and activates the connection only after at least one company is
synced.
"""

from __future__ import annotations

import argparse
import asyncio
import os
from datetime import UTC, datetime, timedelta
from typing import Any

from scripts.local.live_billit_canary import (
    ensure_hosted_canary_schema,
    read_keychain_secret,
)
from sqlalchemy import select

from billit_mcp.auth.billit_oauth import BillitOAuthBridge
from billit_mcp.auth.security import FernetCipher, sha256_text
from billit_mcp.hosted_config import HostedSettings
from billit_mcp.persistence.database import HostedDatabase
from billit_mcp.persistence.models import Actor, BillitConnection, BillitOAuthGrant

DEFAULT_ACCESS_TOKEN_ENV = "BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN"
DEFAULT_REFRESH_TOKEN_ENV = "BILLIT_MCP_CANARY_BILLIT_REFRESH_TOKEN"
DEFAULT_SANDBOX_ACCESS_TOKEN_KEYCHAIN = "BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN_SANDBOX"
DEFAULT_SANDBOX_REFRESH_TOKEN_KEYCHAIN = "BILLIT_MCP_CANARY_BILLIT_REFRESH_TOKEN_SANDBOX"


async def seed_grant(
    *,
    environment: str,
    actor_subject: str,
    access_token: str,
    refresh_token: str,
    expires_in_seconds: int,
) -> dict[str, Any]:
    """Seed a local hosted Billit OAuth grant and return sanitized metadata."""

    if environment != "sandbox":
        raise SystemExit("This local canary seed helper only supports sandbox.")
    settings = HostedSettings.from_env()
    await ensure_hosted_canary_schema(settings.database_url)
    database = HostedDatabase(settings.database_url)
    bridge = BillitOAuthBridge(database, settings, FernetCipher.from_settings(settings))
    try:
        actor_id = await _actor_for_subject(database, actor_subject)
        connection_id = await _store_pending_grant(
            database=database,
            bridge=bridge,
            actor_id=actor_id,
            environment=environment,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in_seconds=expires_in_seconds,
        )
        account_information = await bridge.fetch_account_information(
            environment=environment,
            access_token=access_token,
        )
        company_count = await bridge.sync_companies_from_items(
            connection_id=connection_id,
            environment=environment,
            companies=_account_information_items(account_information),
        )
        if company_count < 1:
            raise SystemExit("Billit accountInformation returned no authorized companies.")
        async with database.session() as session:
            connection = await session.get(BillitConnection, connection_id, with_for_update=True)
            if connection is None:
                raise SystemExit("Seeded Billit connection disappeared before activation.")
            connection.status = "active"
            connection.connected_at = datetime.now(UTC)
        return {
            "connection_id": connection_id,
            "environment": environment,
            "actor_subject": actor_subject,
            "company_count": company_count,
            "database_url": _redact_database_url(settings.database_url),
        }
    finally:
        await database.close()


async def _actor_for_subject(database: HostedDatabase, actor_subject: str) -> str:
    subject_hash = sha256_text(actor_subject)
    async with database.session() as session:
        actor = await session.scalar(select(Actor).where(Actor.subject_hash == subject_hash))
        if actor is None:
            actor = Actor(subject_hash=subject_hash, last_seen_at=datetime.now(UTC))
            session.add(actor)
            await session.flush()
        else:
            actor.last_seen_at = datetime.now(UTC)
        return actor.actor_id


async def _store_pending_grant(
    *,
    database: HostedDatabase,
    bridge: BillitOAuthBridge,
    actor_id: str,
    environment: str,
    access_token: str,
    refresh_token: str,
    expires_in_seconds: int,
) -> str:
    async with database.session() as session:
        connection = await session.scalar(
            select(BillitConnection).where(
                BillitConnection.actor_id == actor_id,
                BillitConnection.environment == environment,
            )
        )
        if connection is None:
            connection = BillitConnection(
                actor_id=actor_id,
                environment=environment,
                status="pending_company_sync",
            )
            session.add(connection)
            await session.flush()
        else:
            connection.status = "pending_company_sync"
            connection.connected_at = None
            connection.reauthorization_required_at = None
        grant = await session.get(BillitOAuthGrant, connection.connection_id)
        expires_at = datetime.now(UTC) + timedelta(seconds=max(1, expires_in_seconds))
        if grant is None:
            grant = BillitOAuthGrant(
                connection_id=connection.connection_id,
                access_token_ciphertext=bridge.cipher.encrypt(access_token),
                access_token_expires_at=expires_at,
                refresh_token_ciphertext=bridge.cipher.encrypt(refresh_token),
                refresh_token_hash=sha256_text(refresh_token),
                encryption_key_version=bridge.cipher.key_version,
                encryption_context={"environment": environment},
                updated_at=datetime.now(UTC),
            )
            session.add(grant)
        else:
            grant.access_token_ciphertext = bridge.cipher.encrypt(access_token)
            grant.access_token_expires_at = expires_at
            grant.refresh_token_ciphertext = bridge.cipher.encrypt(refresh_token)
            grant.refresh_token_hash = sha256_text(refresh_token)
            grant.refresh_token_version += 1
            grant.encryption_key_version = bridge.cipher.key_version
            grant.encryption_context = {"environment": environment}
            grant.updated_at = datetime.now(UTC)
        return connection.connection_id


def secret_from_env_or_keychain(env_name: str, keychain_service: str) -> str | None:
    """Read a secret from env first, then macOS Keychain."""

    value = os.getenv(env_name)
    if value:
        return value
    return read_keychain_secret(keychain_service)


def _account_information_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    items: list[dict[str, Any]] = []
    for key in ("Items", "items", "value", "Companies", "companies", "Company", "company"):
        value = data.get(key)
        if isinstance(value, list):
            items.extend(item for item in value if isinstance(item, dict))
        elif isinstance(value, dict):
            items.append(value)
    items.append(data)
    return items


def _redact_database_url(database_url: str) -> str:
    if "@" not in database_url:
        return database_url
    scheme, rest = database_url.split("://", 1)
    return f"{scheme}://<redacted>@{rest.split('@', 1)[1]}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", default="sandbox", choices=["sandbox"])
    parser.add_argument(
        "--actor-subject",
        default=os.getenv("BILLIT_MCP_CANARY_ACTOR_SUBJECT", "local-dev-actor"),
    )
    parser.add_argument("--database-url", default=os.getenv("BILLIT_MCP_DATABASE_URL"))
    parser.add_argument("--access-token-env", default=DEFAULT_ACCESS_TOKEN_ENV)
    parser.add_argument("--refresh-token-env", default=DEFAULT_REFRESH_TOKEN_ENV)
    parser.add_argument(
        "--access-token-keychain",
        default=DEFAULT_SANDBOX_ACCESS_TOKEN_KEYCHAIN,
    )
    parser.add_argument(
        "--refresh-token-keychain",
        default=DEFAULT_SANDBOX_REFRESH_TOKEN_KEYCHAIN,
    )
    parser.add_argument("--expires-in", type=int, default=3600)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.database_url:
        os.environ["BILLIT_MCP_DATABASE_URL"] = args.database_url
    access_token = secret_from_env_or_keychain(args.access_token_env, args.access_token_keychain)
    refresh_token = secret_from_env_or_keychain(args.refresh_token_env, args.refresh_token_keychain)
    if not access_token or not refresh_token:
        raise SystemExit(
            "Set Billit OAuth access/refresh tokens in env or Keychain before seeding. "
            f"Expected env names: {args.access_token_env}, {args.refresh_token_env}."
        )
    result = asyncio.run(
        seed_grant(
            environment=str(args.environment),
            actor_subject=str(args.actor_subject),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in_seconds=int(args.expires_in),
        )
    )
    print(
        "Seeded hosted sandbox Billit OAuth grant: "
        f"connection_id={result['connection_id']} "
        f"company_count={result['company_count']} "
        f"actor_subject={result['actor_subject']}"
    )


if __name__ == "__main__":
    main()

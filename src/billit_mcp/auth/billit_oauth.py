"""Billit OAuth bridge for hosted mode."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

import httpx
from sqlalchemy import select

from billit.client import BillitAPIClient, BillitOAuthSettings
from billit_mcp.persistence.models import (
    BillitCompany,
    BillitConnection,
    BillitOAuthGrant,
)

from .security import FernetCipher, ensure_aware_utc, random_token_urlsafe, sha256_text

if TYPE_CHECKING:
    from billit_mcp.hosted_config import HostedSettings
    from billit_mcp.persistence.database import HostedDatabase

BILLIT_BASE_URLS = {
    "sandbox": "https://api.sandbox.billit.be/v1",
    "production": "https://api.billit.be/v1",
}

BILLIT_LOGIN_URLS = {
    "sandbox": "https://my.sandbox.billit.be/Account/Logon",
    "production": "https://my.billit.be/Account/Logon",
}

BILLIT_TOKEN_URLS = {
    "sandbox": "https://api.sandbox.billit.be/OAuth2/token",
    "production": "https://api.billit.be/OAuth2/token",
}


class BillitOAuthBridge:
    """Bridge from hosted MCP actors to Billit OAuth grants."""

    def __init__(
        self,
        database: HostedDatabase,
        settings: HostedSettings,
        cipher: FernetCipher,
    ) -> None:
        """Create the Billit OAuth bridge."""

        self.database = database
        self.settings = settings
        self.cipher = cipher

    def authorization_url(self, *, environment: str, state: str) -> str:
        """Return a Billit authorization URL."""

        client_id, _, redirect_uri = self.settings.billit_oauth_client(environment)
        params = {"client_id": client_id, "redirect_uri": redirect_uri, "state": state}
        return f"{BILLIT_LOGIN_URLS[environment]}?{urlencode(params)}"

    async def exchange_callback(
        self,
        *,
        actor_id: str,
        environment: str,
        code: str,
    ) -> str:
        """Exchange a Billit authorization code and store encrypted grant material."""

        client_id, client_secret, redirect_uri = self.settings.billit_oauth_client(environment)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                BILLIT_TOKEN_URLS[environment],
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                },
            )
            response.raise_for_status()
            payload = response.json()
        access_token = str(payload["access_token"])
        refresh_token = str(payload["refresh_token"])
        expires_in = int(payload.get("expires_in", 3600))
        async with self.database.session() as session:
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
            if grant is None:
                grant = BillitOAuthGrant(
                    connection_id=connection.connection_id,
                    access_token_ciphertext=self.cipher.encrypt(access_token),
                    refresh_token_ciphertext=self.cipher.encrypt(refresh_token),
                    refresh_token_hash=sha256_text(refresh_token),
                    access_token_expires_at=datetime.now(UTC) + timedelta(seconds=expires_in),
                    encryption_key_version=self.cipher.key_version,
                    encryption_context={"environment": environment},
                )
                session.add(grant)
            else:
                grant.access_token_ciphertext = self.cipher.encrypt(access_token)
                grant.refresh_token_ciphertext = self.cipher.encrypt(refresh_token)
                grant.refresh_token_hash = sha256_text(refresh_token)
                grant.access_token_expires_at = datetime.now(UTC) + timedelta(seconds=expires_in)
                grant.refresh_token_version += 1
            connection_id = connection.connection_id
        try:
            account_information = await self.fetch_account_information(
                environment=environment,
                access_token=access_token,
            )
            company_count = await self.sync_companies_from_items(
                connection_id=connection_id,
                environment=environment,
                companies=_account_information_items(account_information),
            )
            if company_count < 1:
                raise RuntimeError("Billit accountInformation returned no authorized companies")
        except Exception:
            async with self.database.session() as session:
                connection = await session.get(
                    BillitConnection, connection_id, with_for_update=True
                )
                if connection is not None:
                    connection.status = "company_sync_failed"
                    connection.connected_at = None
            raise
        async with self.database.session() as session:
            connection = await session.get(BillitConnection, connection_id, with_for_update=True)
            if connection is None:
                raise RuntimeError("Billit connection disappeared during company sync")
            connection.status = "active"
            connection.connected_at = datetime.now(UTC)
        return connection_id

    async def fetch_account_information(
        self,
        *,
        environment: str,
        access_token: str,
    ) -> Any:
        """Fetch Billit account information for company authorization sync."""

        async with httpx.AsyncClient(
            base_url=BILLIT_BASE_URLS[environment],
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            timeout=30.0,
        ) as client:
            response = await client.get("/account/accountInformation")
            response.raise_for_status()
            return response.json()

    async def get_billit_access_token(self, *, connection_id: str) -> str:
        """Return a valid Billit access token, refreshing if needed."""

        async with self.database.session() as session:
            connection = await session.get(BillitConnection, connection_id, with_for_update=True)
            if connection is None or connection.status != "active":
                raise RuntimeError("Billit connection is not active")
            grant = await session.get(BillitOAuthGrant, connection_id, with_for_update=True)
            if grant is None:
                raise RuntimeError("Billit OAuth grant is missing")
            if ensure_aware_utc(grant.access_token_expires_at) > datetime.now(UTC) + timedelta(
                minutes=5
            ):
                return self.cipher.decrypt(grant.access_token_ciphertext)
            client_id, client_secret, _ = self.settings.billit_oauth_client(connection.environment)
            refresh_token = self.cipher.decrypt(grant.refresh_token_ciphertext)
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        BILLIT_TOKEN_URLS[connection.environment],
                        json={
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "grant_type": "refresh_token",
                            "refresh_token": refresh_token,
                        },
                    )
                    response.raise_for_status()
                    payload = response.json()
            except Exception:
                connection.status = "reauthorization_required"
                connection.reauthorization_required_at = datetime.now(UTC)
                raise
            access_token = str(payload["access_token"])
            new_refresh_token = str(payload["refresh_token"])
            grant.access_token_ciphertext = self.cipher.encrypt(access_token)
            grant.refresh_token_ciphertext = self.cipher.encrypt(new_refresh_token)
            grant.refresh_token_hash = sha256_text(new_refresh_token)
            grant.access_token_expires_at = datetime.now(UTC) + timedelta(
                seconds=int(payload.get("expires_in", 3600))
            )
            grant.refresh_token_version += 1
            connection.last_refresh_at = datetime.now(UTC)
            return access_token

    async def make_client(self, *, connection_id: str, company_party_id: int) -> BillitAPIClient:
        """Build a Billit API client for a hosted request."""

        async with self.database.session() as session:
            connection = await session.get(BillitConnection, connection_id)
            if connection is None:
                raise RuntimeError("Billit connection is missing")
            base_url = BILLIT_BASE_URLS[connection.environment]
        access_token = await self.get_billit_access_token(connection_id=connection_id)
        return BillitAPIClient(
            BillitOAuthSettings(
                base_url=base_url,
                access_token=access_token,
                party_id=str(company_party_id),
            )
        )

    async def sync_companies_from_items(
        self,
        *,
        connection_id: str,
        environment: str,
        companies: list[dict[str, Any]],
    ) -> int:
        """Sync authorized Billit companies from sanitized account data."""

        seen_party_ids: set[int] = set()
        async with self.database.session() as session:
            for item in companies:
                party_id = _extract_party_id(item)
                if party_id is None:
                    continue
                seen_party_ids.add(party_id)
                existing = await session.scalar(
                    select(BillitCompany).where(
                        BillitCompany.connection_id == connection_id,
                        BillitCompany.environment == environment,
                        BillitCompany.company_party_id == party_id,
                    )
                )
                if existing is None:
                    session.add(
                        BillitCompany(
                            connection_id=connection_id,
                            environment=environment,
                            company_party_id=party_id,
                            company_name_hash=sha256_text(str(item.get("Name", ""))),
                            vat_number_hash=sha256_text(str(item.get("VATNumber", ""))),
                            last_seen_at=datetime.now(UTC),
                        )
                    )
                else:
                    existing.active = True
                    existing.last_seen_at = datetime.now(UTC)
            existing_companies = (
                await session.scalars(
                    select(BillitCompany).where(
                        BillitCompany.connection_id == connection_id,
                        BillitCompany.environment == environment,
                        BillitCompany.active.is_(True),
                    )
                )
            ).all()
            for company in existing_companies:
                if company.company_party_id not in seen_party_ids:
                    company.active = False
                    company.last_seen_at = datetime.now(UTC)
        return len(seen_party_ids)


def new_billit_state() -> str:
    """Return a Billit OAuth state token."""

    return random_token_urlsafe()


def _extract_party_id(item: dict[str, Any]) -> int | None:
    for key in ("PartyID", "CompanyPartyID", "CompanyID", "ID", "party_id", "company_party_id"):
        value = item.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


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

"""MCP OAuth authorization service for hosted mode."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from mcp.server.auth.provider import AccessToken, TokenVerifier
from sqlalchemy import select

from billit_mcp.persistence.models import (
    Actor,
    OAuthAuthCode,
    OAuthAuthorizationTransaction,
    OAuthClient,
    OAuthTokenRevocation,
)

from .security import (
    JWTService,
    ensure_aware_utc,
    random_token_urlsafe,
    sha256_text,
    verify_pkce_s256,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from billit_mcp.hosted_config import HostedSettings, OAuthClientConfig
    from billit_mcp.persistence.database import HostedDatabase


class OAuthError(ValueError):
    """Expected OAuth validation failure."""

    def __init__(self, error: str, description: str) -> None:
        """Create an OAuth error."""

        super().__init__(description)
        self.error = error
        self.description = description


class MCPOAuthService:
    """Static-client MCP OAuth service."""

    def __init__(self, database: HostedDatabase, settings: HostedSettings, jwt_service: JWTService):
        """Create the OAuth service."""

        self.database = database
        self.settings = settings
        self.jwt_service = jwt_service

    async def seed_static_clients(self) -> None:
        """Upsert configured static OAuth clients."""

        async with self.database.session() as session:
            for client in self.settings.static_clients:
                await self._upsert_client(session, client)

    async def actor_for_subject(self, subject: str) -> str:
        """Return a stable actor ID for a hosted subject."""

        async with self.database.session() as session:
            actor = await self._get_or_create_actor(session, subject)
            return actor.actor_id

    async def _upsert_client(self, session: AsyncSession, config: OAuthClientConfig) -> None:
        existing = await session.get(OAuthClient, config.client_id)
        secret_hash = sha256_text(config.client_secret) if config.client_secret else None
        if existing is None:
            session.add(
                OAuthClient(
                    client_id=config.client_id,
                    client_name=config.client_id,
                    client_type="confidential" if config.client_secret else "public",
                    client_secret_hash=secret_hash,
                    redirect_uris=list(config.redirect_uris),
                    allowed_scopes=list(config.allowed_scopes),
                    status="active",
                )
            )
            return
        existing.redirect_uris = list(config.redirect_uris)
        existing.allowed_scopes = list(config.allowed_scopes)
        existing.client_secret_hash = secret_hash
        existing.client_type = "confidential" if config.client_secret else "public"
        existing.status = "active"

    async def authorize(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: str,
        state: str | None,
        code_challenge: str,
        code_challenge_method: str,
        actor_subject: str,
        environment: str,
    ) -> str:
        """Validate an authorize request and return a redirect URI with code."""

        async with self.database.session() as session:
            client = await self._load_client(session, client_id)
            if redirect_uri not in client.redirect_uris:
                raise OAuthError("invalid_request", "redirect_uri is not registered")
            if code_challenge_method != "S256":
                raise OAuthError("invalid_request", "code_challenge_method must be S256")
            scopes = _normalize_requested_scopes(scope, client.allowed_scopes)
            actor = await self._get_or_create_actor(session, actor_subject)
            code = random_token_urlsafe()
            expires_at = datetime.now(UTC) + timedelta(minutes=10)
            transaction = OAuthAuthorizationTransaction(
                client_id=client_id,
                actor_id=actor.actor_id,
                redirect_uri=redirect_uri,
                scopes=scopes,
                state_hash=sha256_text(state) if state else None,
                environment=environment,
                status="code_issued",
                expires_at=expires_at,
            )
            session.add(transaction)
            session.add(
                OAuthAuthCode(
                    code_hash=sha256_text(code),
                    client_id=client_id,
                    actor_id=actor.actor_id,
                    redirect_uri=redirect_uri,
                    code_challenge=code_challenge,
                    code_challenge_method="S256",
                    scopes=scopes,
                    state_hash=sha256_text(state) if state else None,
                    expires_at=expires_at,
                )
            )
        params = {"code": code}
        if state:
            params["state"] = state
        return f"{redirect_uri}?{urlencode(params)}"

    async def exchange_code(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        code: str,
        code_verifier: str,
        client_secret: str | None = None,
    ) -> dict[str, Any]:
        """Exchange an authorization code for an MCP access token."""

        async with self.database.session() as session:
            client = await self._load_client(session, client_id)
            if (
                client.client_secret_hash
                and sha256_text(client_secret or "") != client.client_secret_hash
            ):
                raise OAuthError("invalid_client", "client authentication failed")
            auth_code = await session.get(OAuthAuthCode, sha256_text(code), with_for_update=True)
            now = datetime.now(UTC)
            if auth_code is None:
                raise OAuthError("invalid_grant", "authorization code is invalid")
            if auth_code.used_at is not None:
                raise OAuthError("invalid_grant", "authorization code was already used")
            if ensure_aware_utc(auth_code.expires_at) < now:
                raise OAuthError("invalid_grant", "authorization code expired")
            if auth_code.client_id != client_id or auth_code.redirect_uri != redirect_uri:
                raise OAuthError("invalid_grant", "authorization code binding mismatch")
            if not verify_pkce_s256(code_verifier, auth_code.code_challenge):
                raise OAuthError("invalid_grant", "PKCE verifier does not match")
            auth_code.used_at = now
            access_token, claims = self.jwt_service.issue_access_token(
                actor_id=auth_code.actor_id,
                client_id=client_id,
                scopes=list(auth_code.scopes),
            )
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": claims["exp"] - claims["iat"],
            "scope": " ".join(auth_code.scopes),
        }

    async def revoke_token(self, token: str, reason: str = "client_revoked") -> None:
        """Revoke an MCP access token by JTI."""

        claims = self.jwt_service.decode(token)
        async with self.database.session() as session:
            session.add(
                OAuthTokenRevocation(
                    jti_hash=sha256_text(str(claims["jti"])),
                    actor_id=str(claims.get("sub")),
                    client_id=str(claims.get("client_id")),
                    expires_at=datetime.fromtimestamp(int(claims["exp"]), UTC),
                    reason=reason,
                )
            )

    async def verify_access_token_claims(self, token: str) -> dict[str, Any] | None:
        """Verify an MCP access token and revocation status."""

        try:
            claims = self.jwt_service.decode(token)
        except Exception:
            return None
        async with self.database.session() as session:
            revoked = await session.get(OAuthTokenRevocation, sha256_text(str(claims["jti"])))
            if revoked is not None:
                return None
        return claims

    async def _load_client(self, session: AsyncSession, client_id: str) -> OAuthClient:
        client = await session.get(OAuthClient, client_id)
        if client is None or client.status != "active":
            raise OAuthError("invalid_client", "client is not registered or active")
        return client

    async def _get_or_create_actor(self, session: AsyncSession, subject: str) -> Actor:
        subject_hash = sha256_text(subject)
        existing = await session.scalar(select(Actor).where(Actor.subject_hash == subject_hash))
        if existing is not None:
            existing.last_seen_at = datetime.now(UTC)
            return existing
        actor = Actor(subject_hash=subject_hash, last_seen_at=datetime.now(UTC))
        session.add(actor)
        await session.flush()
        return actor


class MCPJWTVerifier(TokenVerifier):
    """MCP SDK token verifier backed by the hosted OAuth service."""

    def __init__(self, oauth_service: MCPOAuthService) -> None:
        """Create the verifier."""

        self.oauth_service = oauth_service

    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify a bearer token and return MCP access metadata."""

        claims = await self.oauth_service.verify_access_token_claims(token)
        if claims is None:
            return None
        scopes = str(claims.get("scope", "")).split()
        return AccessToken(
            token=token,
            client_id=str(claims.get("client_id", "")),
            scopes=scopes,
            expires_at=int(claims["exp"]),
            resource=str(claims.get("aud")),
        )


def _normalize_requested_scopes(scope: str, allowed_scopes: list[str]) -> list[str]:
    requested = [item for item in scope.replace(",", " ").split() if item]
    if not requested:
        requested = ["billit:read"]
    disallowed = sorted(set(requested) - set(allowed_scopes))
    if disallowed:
        raise OAuthError("invalid_scope", f"scope not allowed: {' '.join(disallowed)}")
    return requested

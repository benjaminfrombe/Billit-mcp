"""Hosted Billit client construction and outbound audit wrappers."""

from __future__ import annotations

from contextlib import asynccontextmanager, suppress
from time import perf_counter
from typing import TYPE_CHECKING, Any

from billit_mcp.auth.security import random_token_urlsafe

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from billit.client import BillitAPIClient
    from billit_mcp.auth.billit_oauth import BillitOAuthBridge
    from billit_mcp.persistence.models import BillitConnection
    from billit_mcp.services.hosted_audit import HostedAuditService
    from billit_mcp.services.hosted_authorization import HostedAuthorizationService
    from billit_mcp.services.hosted_claims import HostedClaims


class HostedBillitClientService:
    """Create authorized Billit clients for hosted tool calls."""

    def __init__(
        self,
        *,
        billit_bridge: BillitOAuthBridge,
        authorization: HostedAuthorizationService,
        audit: HostedAuditService,
    ) -> None:
        self._billit_bridge = billit_bridge
        self._authorization = authorization
        self._audit = audit

    async def billit_client(
        self,
        *,
        actor_id: str,
        environment: str,
        company_party_id: int,
        client_id: str | None = None,
        correlation_id: str | None = None,
        tool_name: str | None = None,
    ) -> tuple[BillitConnection, AuditedBillitClient]:
        """Return a Billit client for an authorized hosted request."""

        connection = await self._authorization.resolve_connection(
            actor_id=actor_id,
            environment=environment,
        )
        await self._authorization.validate_company(
            connection_id=connection.connection_id,
            environment=environment,
            company_party_id=company_party_id,
        )
        try:
            client = await self._billit_bridge.make_client(
                connection_id=connection.connection_id,
                company_party_id=company_party_id,
            )
        except Exception:
            await self._audit.audit(
                actor_id=actor_id,
                client_id=client_id,
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
                event_type="billit_oauth_refresh_failed",
                operation_class="auth",
                outcome="failure",
                correlation_id=correlation_id or random_token_urlsafe(),
                tool_name=tool_name,
                error_code="BILLIT_REFRESH_FAILED",
            )
            raise
        return (
            connection,
            AuditedBillitClient(
                client=client,
                audit=self._audit,
                actor_id=actor_id,
                client_id=client_id,
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
                correlation_id=correlation_id or random_token_urlsafe(),
                tool_name=tool_name,
            ),
        )

    @asynccontextmanager
    async def authorized_billit_client(
        self,
        *,
        claims: HostedClaims,
        environment: str,
        company_party_id: int,
        tool_name: str,
    ) -> AsyncIterator[tuple[BillitConnection, AuditedBillitClient]]:
        """Yield an authorized Billit client and always close it."""

        connection, client = await self.billit_client(
            actor_id=claims.actor_id,
            client_id=claims.client_id,
            correlation_id=claims.correlation_id,
            tool_name=tool_name,
            environment=environment,
            company_party_id=company_party_id,
        )
        try:
            yield connection, client
        finally:
            await client.close()


class AuditedBillitClient:
    """Hosted Billit API client wrapper that records redacted outbound audit."""

    def __init__(
        self,
        *,
        client: BillitAPIClient,
        audit: HostedAuditService,
        actor_id: str,
        client_id: str | None,
        connection_id: str,
        environment: str,
        company_party_id: int,
        correlation_id: str,
        tool_name: str | None,
    ) -> None:
        self._client = client
        self._audit = audit
        self._actor_id = actor_id
        self._client_id = client_id
        self._connection_id = connection_id
        self._environment = environment
        self._company_party_id = company_party_id
        self._correlation_id = correlation_id
        self._tool_name = tool_name

    async def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        """Proxy a Billit request and audit only method/path/status metadata."""

        started = perf_counter()
        outcome = "success"
        error_code: str | None = None
        try:
            response = await self._client.request(method, path, **kwargs)
            if not response.get("success", False):
                outcome = "failure"
                error_code = str(response.get("error_code") or "BILLIT_API_ERROR")
            return response
        except Exception:
            outcome = "failure"
            error_code = "BILLIT_API_EXCEPTION"
            raise
        finally:
            with suppress(Exception):
                await self._audit.audit(
                    actor_id=self._actor_id,
                    client_id=self._client_id,
                    connection_id=self._connection_id,
                    environment=self._environment,
                    company_party_id=self._company_party_id,
                    event_type="billit_api_call",
                    operation_class="external_api",
                    outcome=outcome,
                    correlation_id=self._correlation_id,
                    tool_name=self._tool_name,
                    summary={"method": method.upper(), "path": path},
                    error_code=error_code,
                    latency_ms=int((perf_counter() - started) * 1000),
                )

    async def close(self) -> None:
        """Close the underlying Billit API client."""

        await self._client.close()

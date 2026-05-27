"""Hosted runtime facade for curated MCP tools."""

from __future__ import annotations

from contextlib import asynccontextmanager, suppress
from time import perf_counter
from typing import TYPE_CHECKING, Any

from billit_mcp.auth.security import random_token_urlsafe
from billit_mcp.services.hosted_audit import HostedAuditService
from billit_mcp.services.hosted_authorization import HostedAuthorizationService
from billit_mcp.services.hosted_claims import HostedClaims, HostedClaimsVerifier
from billit_mcp.services.hosted_clients import AuditedBillitClient, HostedBillitClientService
from billit_mcp.services.hosted_confirmation import HostedConfirmationService
from billit_mcp.services.hosted_errors import (
    SECURITY_DENIALS,
    HostedToolError,
    error_result,
    success,
)
from billit_mcp.services.hosted_idempotency import HostedIdempotencyService
from billit_mcp.services.invoice_workflow import (
    IdempotencyStart,
)
from billit_mcp.services.invoice_workflow import (
    hash_payload as shared_hash_payload,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from billit_mcp.auth.billit_oauth import BillitOAuthBridge
    from billit_mcp.auth.security import JWTService
    from billit_mcp.hosted_config import HostedSettings
    from billit_mcp.persistence.database import HostedDatabase
    from billit_mcp.persistence.models import BillitConnection, ConfirmationChallenge

__all__ = [
    "AuditedBillitClient",
    "HostedClaims",
    "HostedToolError",
    "HostedToolRuntime",
    "error_result",
    "hash_payload",
    "success",
]


class HostedToolRuntime:
    """Stable facade shared by hosted MCP tools."""

    def __init__(
        self,
        *,
        settings: HostedSettings,
        database: HostedDatabase,
        jwt_service: JWTService,
        billit_bridge: BillitOAuthBridge,
    ) -> None:
        """Create the hosted tool runtime."""

        self.settings = settings
        self.database = database
        self.jwt_service = jwt_service
        self.billit_bridge = billit_bridge
        self._claims = HostedClaimsVerifier(jwt_service)
        self._audit = HostedAuditService(database)
        self._authorization = HostedAuthorizationService(database)
        self._clients = HostedBillitClientService(
            billit_bridge=billit_bridge,
            authorization=self._authorization,
            audit=self._audit,
        )
        self._confirmations = HostedConfirmationService(database=database, audit=self._audit)
        self._idempotency = HostedIdempotencyService(database)

    async def claims(self, required_scope: str = "billit:read") -> dict[str, Any]:
        """Return verified current MCP claims from the auth context."""

        return await self._claims.claims(required_scope)

    def typed_claims(self, claims: dict[str, Any]) -> HostedClaims:
        """Return typed claim fields required by hosted tools."""

        return self._claims.typed_claims(claims)

    async def execute_tool(
        self,
        *,
        tool_name: str,
        required_scope: str,
        operation_class: str,
        handler: Any,
        environment: str | None = None,
        company_party_id: int | None = None,
    ) -> dict[str, Any]:
        """Run a hosted tool with centralized scope checks, errors, and audit."""

        started = perf_counter()
        claims: dict[str, Any] | None = None
        result: dict[str, Any]
        outcome = "success"
        error_code: str | None = None
        try:
            claims = await self.claims(required_scope)
            result = await handler(claims)
            if not result.get("success", False):
                outcome = "failure"
                error_code = str(result.get("error_code") or "HOSTED_TOOL_FAILURE")
            return result
        except Exception as exc:
            result = error_result(exc)
            if isinstance(exc, HostedToolError) and exc.error_type in SECURITY_DENIALS:
                outcome = "denied"
            else:
                outcome = "failure"
            error_code = str(result.get("error_code") or "HOSTED_TOOL_ERROR")
            return result
        finally:
            correlation_id = str((claims or {}).get("jti") or random_token_urlsafe())
            with suppress(Exception):
                await self.audit(
                    actor_id=str(claims["sub"]) if claims and claims.get("sub") else None,
                    client_id=str(claims["client_id"])
                    if claims and claims.get("client_id")
                    else None,
                    event_type="tool_call",
                    operation_class=operation_class,
                    outcome=outcome,
                    correlation_id=correlation_id,
                    environment=environment,
                    company_party_id=company_party_id,
                    tool_name=tool_name,
                    error_code=error_code,
                    latency_ms=int((perf_counter() - started) * 1000),
                )

    async def resolve_connection(
        self,
        *,
        actor_id: str,
        environment: str,
    ) -> BillitConnection:
        """Return the active Billit connection for an actor/environment."""

        return await self._authorization.resolve_connection(
            actor_id=actor_id,
            environment=environment,
        )

    async def validate_company(
        self,
        *,
        connection_id: str,
        environment: str,
        company_party_id: int,
    ) -> None:
        """Fail unless the company is authorized for this connection."""

        await self._authorization.validate_company(
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
        )

    async def list_authorized_companies(
        self,
        *,
        connection_id: str,
        environment: str,
    ) -> list[dict[str, Any]]:
        """Return sanitized company rows authorized for a hosted connection."""

        return await self._authorization.list_authorized_companies(
            connection_id=connection_id,
            environment=environment,
        )

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

        return await self._clients.billit_client(
            actor_id=actor_id,
            client_id=client_id,
            correlation_id=correlation_id,
            tool_name=tool_name,
            environment=environment,
            company_party_id=company_party_id,
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

        async with self._clients.authorized_billit_client(
            claims=claims,
            environment=environment,
            company_party_id=company_party_id,
            tool_name=tool_name,
        ) as client:
            yield client

    async def create_confirmation_challenge(
        self,
        *,
        actor_id: str,
        client_id: str,
        connection_id: str,
        environment: str,
        company_party_id: int,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        required_scope: str,
        summary: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a single-use confirmation challenge."""

        return await self._confirmations.create_confirmation_challenge(
            actor_id=actor_id,
            client_id=client_id,
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            required_scope=required_scope,
            summary=summary,
        )

    async def consume_confirmation_challenge(
        self,
        *,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
        actor_id: str,
        client_id: str,
        connection_id: str,
        environment: str,
        company_party_id: int,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        required_scope: str,
    ) -> ConfirmationChallenge:
        """Atomically consume a pending confirmation challenge."""

        return await self._confirmations.consume_confirmation_challenge(
            challenge_id=challenge_id,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
            actor_id=actor_id,
            client_id=client_id,
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            required_scope=required_scope,
        )

    async def get_pending_confirmation_challenge(
        self,
        *,
        challenge_id: str,
        actor_id: str,
        client_id: str,
        environment: str,
        company_party_id: int,
        operation_type: str,
        resource_type: str,
        required_scope: str,
    ) -> ConfirmationChallenge:
        """Load a pending challenge without consuming it for pre-send revalidation."""

        return await self._confirmations.get_pending_confirmation_challenge(
            challenge_id=challenge_id,
            actor_id=actor_id,
            client_id=client_id,
            environment=environment,
            company_party_id=company_party_id,
            operation_type=operation_type,
            resource_type=resource_type,
            required_scope=required_scope,
        )

    async def record_idempotency_started(
        self,
        *,
        connection_id: str,
        company_party_id: int,
        operation_type: str,
        idempotency_key: str,
        operation_hash: str,
    ) -> IdempotencyStart:
        """Record an idempotency key and indicate whether it was newly inserted."""

        return await self._idempotency.record_idempotency_started(
            connection_id=connection_id,
            company_party_id=company_party_id,
            operation_type=operation_type,
            idempotency_key=idempotency_key,
            operation_hash=operation_hash,
        )

    async def record_idempotency_outcome(
        self,
        *,
        idempotency_id: str,
        status: str,
        billit_resource_type: str | None = None,
        billit_resource_id: str | None = None,
        billit_error_code: str | None = None,
    ) -> None:
        """Persist the final state of a hosted idempotent operation."""

        await self._idempotency.record_idempotency_outcome(
            idempotency_id=idempotency_id,
            status=status,
            billit_resource_type=billit_resource_type,
            billit_resource_id=billit_resource_id,
            billit_error_code=billit_error_code,
        )

    async def audit(
        self,
        *,
        actor_id: str | None,
        client_id: str | None,
        event_type: str,
        operation_class: str,
        outcome: str,
        correlation_id: str,
        environment: str | None = None,
        company_party_id: int | None = None,
        connection_id: str | None = None,
        tool_name: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
        latency_ms: int | None = None,
        billit_request_id: str | None = None,
    ) -> None:
        """Record a redacted audit event."""

        await self._audit.audit(
            actor_id=actor_id,
            client_id=client_id,
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
            event_type=event_type,
            operation_class=operation_class,
            tool_name=tool_name,
            summary=summary,
            outcome=outcome,
            error_code=error_code,
            correlation_id=correlation_id,
            billit_request_id=billit_request_id,
            latency_ms=latency_ms,
        )


def hash_payload(payload: dict[str, Any]) -> str:
    """Return a stable hash for a JSON-compatible operation payload."""

    return shared_hash_payload(payload)

"""Hosted runtime services for curated MCP tools."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from mcp.server.auth.middleware.auth_context import get_access_token
from sqlalchemy import select, update

from billit_mcp.auth.security import ensure_aware_utc, random_token_urlsafe, sha256_text
from billit_mcp.persistence.models import (
    AuditEvent,
    BillitCompany,
    BillitConnection,
    ConfirmationChallenge,
    IdempotencyRecord,
)

if TYPE_CHECKING:
    from billit.client import BillitAPIClient
    from billit_mcp.auth.billit_oauth import BillitOAuthBridge
    from billit_mcp.auth.security import JWTService
    from billit_mcp.hosted_config import HostedSettings
    from billit_mcp.persistence.database import HostedDatabase


class HostedToolError(RuntimeError):
    """Structured hosted tool error."""

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        severity: str = "blocking",
        retryable: bool = False,
        user_action_required: bool = True,
        error_code: str | None = None,
    ) -> None:
        """Create a structured tool error."""

        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.retryable = retryable
        self.user_action_required = user_action_required
        self.error_code = error_code or error_type.upper()

    def to_result(self) -> dict[str, Any]:
        """Return the stable Billit MCP envelope."""

        return {
            "success": False,
            "data": None,
            "error": {
                "type": self.error_type,
                "severity": self.severity,
                "retryable": self.retryable,
                "user_action_required": self.user_action_required,
                "message": self.message,
            },
            "error_code": self.error_code,
        }


class HostedToolRuntime:
    """Services shared by hosted MCP tools."""

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

    async def claims(self, required_scope: str = "billit:read") -> dict[str, Any]:
        """Return verified current MCP claims from the auth context."""

        access_token = get_access_token()
        if access_token is None:
            raise HostedToolError("unauthenticated", "Hosted tool requires an MCP bearer token")
        claims = self.jwt_service.decode(access_token.token)
        scopes = set(str(claims.get("scope", "")).split())
        if required_scope not in scopes:
            raise HostedToolError(
                "insufficient_scope",
                f"Missing required scope: {required_scope}",
                error_code="INSUFFICIENT_SCOPE",
            )
        return claims

    async def resolve_connection(
        self,
        *,
        actor_id: str,
        environment: str,
    ) -> BillitConnection:
        """Return the active Billit connection for an actor/environment."""

        async with self.database.session() as session:
            connection = await session.scalar(
                select(BillitConnection).where(
                    BillitConnection.actor_id == actor_id,
                    BillitConnection.environment == environment,
                )
            )
            if connection is None:
                raise HostedToolError(
                    "billit_not_connected",
                    f"No Billit OAuth connection exists for {environment}",
                )
            if connection.status != "active":
                raise HostedToolError(
                    "billit_reauthorization_required",
                    "Billit connection requires reauthorization",
                )
            session.expunge(connection)
            return connection

    async def validate_company(
        self,
        *,
        connection_id: str,
        environment: str,
        company_party_id: int,
    ) -> None:
        """Fail unless the company is authorized for this connection."""

        async with self.database.session() as session:
            company = await session.scalar(
                select(BillitCompany).where(
                    BillitCompany.connection_id == connection_id,
                    BillitCompany.environment == environment,
                    BillitCompany.company_party_id == company_party_id,
                    BillitCompany.active.is_(True),
                )
            )
        if company is None:
            raise HostedToolError(
                "unauthorized_company",
                "company_party_id is not authorized for this Billit connection",
                error_code="UNAUTHORIZED_COMPANY",
            )

    async def billit_client(
        self,
        *,
        actor_id: str,
        environment: str,
        company_party_id: int,
    ) -> tuple[BillitConnection, BillitAPIClient]:
        """Return a Billit client for an authorized hosted request."""

        connection = await self.resolve_connection(actor_id=actor_id, environment=environment)
        await self.validate_company(
            connection_id=connection.connection_id,
            environment=environment,
            company_party_id=company_party_id,
        )
        client = await self.billit_bridge.make_client(
            connection_id=connection.connection_id,
            company_party_id=company_party_id,
        )
        return connection, client

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

        token = random_token_urlsafe()
        nonce = random_token_urlsafe()
        operation_hash = hash_payload(summary)
        challenge = ConfirmationChallenge(
            actor_id=actor_id,
            client_id=client_id,
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            summary_json=summary,
            operation_hash=operation_hash,
            required_scope=required_scope,
            nonce_hash=sha256_text(nonce),
            confirmation_token_hash=sha256_text(token),
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
        )
        async with self.database.session() as session:
            session.add(challenge)
        return {
            "challenge_id": challenge.challenge_id,
            "confirmation_token": token,
            "operation_hash": operation_hash,
            "expires_at": challenge.expires_at.isoformat(),
            "summary": summary,
        }

    async def consume_confirmation_challenge(
        self,
        *,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
        actor_id: str,
        client_id: str,
    ) -> ConfirmationChallenge:
        """Atomically consume a pending confirmation challenge."""

        async with self.database.session() as session:
            challenge = await session.get(
                ConfirmationChallenge,
                challenge_id,
                with_for_update=True,
            )
            if challenge is None:
                raise HostedToolError("challenge_not_found", "Confirmation challenge not found")
            now = datetime.now(UTC)
            if challenge.status != "pending" or ensure_aware_utc(challenge.expires_at) <= now:
                raise HostedToolError("challenge_expired", "Confirmation challenge is not pending")
            if challenge.actor_id != actor_id or challenge.client_id != client_id:
                raise HostedToolError("challenge_actor_mismatch", "Challenge actor/client mismatch")
            if challenge.confirmation_token_hash != sha256_text(confirmation_token):
                raise HostedToolError("challenge_token_invalid", "Confirmation token is invalid")
            if challenge.operation_hash != operation_hash:
                raise HostedToolError("challenge_changed", "Operation hash changed")
            await session.execute(
                update(ConfirmationChallenge)
                .where(
                    ConfirmationChallenge.challenge_id == challenge_id,
                    ConfirmationChallenge.status == "pending",
                )
                .values(status="consumed", consumed_at=now)
            )
            session.expunge(challenge)
            return challenge

    async def record_idempotency_started(
        self,
        *,
        connection_id: str,
        company_party_id: int,
        operation_type: str,
        idempotency_key: str,
        operation_hash: str,
    ) -> None:
        """Record a local idempotency key if one is provided."""

        async with self.database.session() as session:
            existing = await session.scalar(
                select(IdempotencyRecord).where(
                    IdempotencyRecord.connection_id == connection_id,
                    IdempotencyRecord.company_party_id == company_party_id,
                    IdempotencyRecord.operation_type == operation_type,
                    IdempotencyRecord.idempotency_key_hash == sha256_text(idempotency_key),
                )
            )
            if existing is not None and existing.operation_hash != operation_hash:
                raise HostedToolError(
                    "idempotency_conflict",
                    "Idempotency key was already used for a different operation",
                )
            if existing is None:
                session.add(
                    IdempotencyRecord(
                        connection_id=connection_id,
                        company_party_id=company_party_id,
                        operation_type=operation_type,
                        idempotency_key_hash=sha256_text(idempotency_key),
                        operation_hash=operation_hash,
                    )
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
    ) -> None:
        """Record a redacted audit event."""

        async with self.database.session() as session:
            session.add(
                AuditEvent(
                    actor_id=actor_id,
                    client_id=client_id,
                    connection_id=connection_id,
                    environment=environment,
                    company_party_id=company_party_id,
                    event_type=event_type,
                    operation_class=operation_class,
                    tool_name=tool_name,
                    resource_refs={},
                    summary_json=summary or {},
                    outcome=outcome,
                    error_code=error_code,
                    correlation_id=correlation_id,
                )
            )


def success(data: Any) -> dict[str, Any]:
    """Return a successful tool result."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def error_result(exc: Exception) -> dict[str, Any]:
    """Convert an exception into the stable MCP envelope."""

    if isinstance(exc, HostedToolError):
        return exc.to_result()
    return {
        "success": False,
        "data": None,
        "error": {
            "type": "hosted_tool_error",
            "severity": "blocking",
            "retryable": False,
            "user_action_required": True,
            "message": str(exc),
        },
        "error_code": "HOSTED_TOOL_ERROR",
    }


def hash_payload(payload: dict[str, Any]) -> str:
    """Return a stable hash for a JSON-compatible operation payload."""

    return sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))

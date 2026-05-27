"""Hosted runtime services for curated MCP tools."""

from __future__ import annotations

from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from time import perf_counter
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
from billit_mcp.services.invoice_workflow import (
    IdempotencyStart,
    IdempotencyState,
    hash_payload as shared_hash_payload,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from billit.client import BillitAPIClient
    from billit_mcp.auth.billit_oauth import BillitOAuthBridge
    from billit_mcp.auth.security import JWTService
    from billit_mcp.hosted_config import HostedSettings
    from billit_mcp.persistence.database import HostedDatabase


SECURITY_DENIALS = {
    "unauthenticated",
    "insufficient_scope",
    "billit_not_connected",
    "billit_reauthorization_required",
    "unauthorized_company",
}


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


@dataclass(frozen=True)
class HostedClaims:
    """Typed hosted MCP claims used by tool handlers."""

    actor_id: str
    client_id: str
    correlation_id: str
    raw: dict[str, Any]


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

    def typed_claims(self, claims: dict[str, Any]) -> HostedClaims:
        """Return typed claim fields required by hosted tools."""

        return HostedClaims(
            actor_id=str(claims["sub"]),
            client_id=str(claims["client_id"]),
            correlation_id=str(claims["jti"]),
            raw=claims,
        )

    async def list_authorized_companies(
        self,
        *,
        connection_id: str,
        environment: str,
    ) -> list[dict[str, Any]]:
        """Return sanitized company rows authorized for a hosted connection."""

        async with self.database.session() as session:
            companies = (
                await session.scalars(
                    select(BillitCompany).where(
                        BillitCompany.connection_id == connection_id,
                        BillitCompany.environment == environment,
                        BillitCompany.active.is_(True),
                    )
                )
            ).all()
        return [
            {
                "company_party_id": company.company_party_id,
                "environment": company.environment,
                "active": company.active,
                "is_default": company.is_default,
            }
            for company in companies
        ]

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

        connection = await self.resolve_connection(actor_id=actor_id, environment=environment)
        await self.validate_company(
            connection_id=connection.connection_id,
            environment=environment,
            company_party_id=company_party_id,
        )
        try:
            client = await self.billit_bridge.make_client(
                connection_id=connection.connection_id,
                company_party_id=company_party_id,
            )
        except Exception:
            await self.audit(
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
                runtime=self,
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
        await self.audit(
            actor_id=actor_id,
            client_id=client_id,
            connection_id=connection_id,
            environment=environment,
            company_party_id=company_party_id,
            event_type="confirmation_challenge_created",
            operation_class="confirmation",
            outcome="challenge_created",
            correlation_id=nonce,
            summary={"operation_type": operation_type, "resource_type": resource_type},
        )
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
        connection_id: str,
        environment: str,
        company_party_id: int,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        required_scope: str,
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
            if (
                challenge.connection_id != connection_id
                or challenge.environment != environment
                or challenge.company_party_id != company_party_id
                or challenge.operation_type != operation_type
                or challenge.resource_type != resource_type
                or challenge.resource_id != resource_id
                or challenge.required_scope != required_scope
            ):
                raise HostedToolError("challenge_mismatch", "Challenge invariants do not match")
            if challenge.confirmation_token_hash != sha256_text(confirmation_token):
                raise HostedToolError("challenge_token_invalid", "Confirmation token is invalid")
            if challenge.operation_hash != operation_hash:
                raise HostedToolError("challenge_changed", "Operation hash changed")
            comparison_now = now if challenge.expires_at.tzinfo else now.replace(tzinfo=None)
            result = await session.execute(
                update(ConfirmationChallenge)
                .where(
                    ConfirmationChallenge.challenge_id == challenge_id,
                    ConfirmationChallenge.status == "pending",
                    ConfirmationChallenge.actor_id == actor_id,
                    ConfirmationChallenge.client_id == client_id,
                    ConfirmationChallenge.connection_id == connection_id,
                    ConfirmationChallenge.environment == environment,
                    ConfirmationChallenge.company_party_id == company_party_id,
                    ConfirmationChallenge.operation_type == operation_type,
                    ConfirmationChallenge.resource_type == resource_type,
                    ConfirmationChallenge.resource_id == resource_id,
                    ConfirmationChallenge.required_scope == required_scope,
                    ConfirmationChallenge.operation_hash == operation_hash,
                    ConfirmationChallenge.confirmation_token_hash
                    == sha256_text(confirmation_token),
                    ConfirmationChallenge.expires_at > comparison_now,
                )
                .values(status="consumed", consumed_at=now)
            )
            if getattr(result, "rowcount", 0) != 1:
                raise HostedToolError("challenge_consume_failed", "Confirmation was not consumed")
            challenge.status = "consumed"
            challenge.consumed_at = now
            session.expunge(challenge)
        with suppress(Exception):
            await self.audit(
                actor_id=actor_id,
                client_id=client_id,
                connection_id=connection_id,
                environment=environment,
                company_party_id=company_party_id,
                event_type="confirmation_challenge_consumed",
                operation_class="confirmation",
                outcome="challenge_consumed",
                correlation_id=random_token_urlsafe(),
                summary={"operation_type": operation_type, "resource_type": resource_type},
            )
        return challenge

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

        async with self.database.session() as session:
            challenge = await session.get(ConfirmationChallenge, challenge_id)
            if challenge is None:
                raise HostedToolError("challenge_not_found", "Confirmation challenge not found")
            if challenge.status != "pending" or ensure_aware_utc(
                challenge.expires_at
            ) <= datetime.now(UTC):
                raise HostedToolError("challenge_expired", "Confirmation challenge is not pending")
            if (
                challenge.actor_id != actor_id
                or challenge.client_id != client_id
                or challenge.environment != environment
                or challenge.company_party_id != company_party_id
                or challenge.operation_type != operation_type
                or challenge.resource_type != resource_type
                or challenge.required_scope != required_scope
            ):
                raise HostedToolError("challenge_mismatch", "Challenge invariants do not match")
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
    ) -> IdempotencyStart:
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
            if existing is not None:
                session.expunge(existing)
                return IdempotencyStart(
                    record=IdempotencyState(
                        idempotency_id=existing.idempotency_id,
                        status=existing.status,
                        operation_hash=existing.operation_hash,
                        billit_resource_id=existing.billit_resource_id,
                    ),
                    created=False,
                )
            record = IdempotencyRecord(
                connection_id=connection_id,
                company_party_id=company_party_id,
                operation_type=operation_type,
                idempotency_key_hash=sha256_text(idempotency_key),
                operation_hash=operation_hash,
            )
            session.add(record)
            await session.flush()
            started = IdempotencyStart(
                record=IdempotencyState(
                    idempotency_id=record.idempotency_id,
                    status=record.status,
                    operation_hash=record.operation_hash,
                    billit_resource_id=record.billit_resource_id,
                ),
                created=True,
            )
            session.expunge(record)
            return started

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

        allowed = {"started", "succeeded", "failed", "conflict", "unknown_side_effect"}
        if status not in allowed:
            raise ValueError(f"Unsupported idempotency status: {status}")
        async with self.database.session() as session:
            record = await session.get(IdempotencyRecord, idempotency_id, with_for_update=True)
            if record is None:
                return
            record.status = status
            record.billit_resource_type = billit_resource_type
            record.billit_resource_id = billit_resource_id
            record.billit_error_code = billit_error_code
            record.updated_at = datetime.now(UTC)

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
                    billit_request_id=billit_request_id,
                    latency_ms=latency_ms,
                )
            )


class AuditedBillitClient:
    """Hosted Billit API client wrapper that records redacted outbound audit."""

    def __init__(
        self,
        *,
        client: BillitAPIClient,
        runtime: HostedToolRuntime,
        actor_id: str,
        client_id: str | None,
        connection_id: str,
        environment: str,
        company_party_id: int,
        correlation_id: str,
        tool_name: str | None,
    ) -> None:
        self._client = client
        self._runtime = runtime
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
                await self._runtime.audit(
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

    return shared_hash_payload(payload)

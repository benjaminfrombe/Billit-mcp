"""Hosted audit persistence helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit_mcp.persistence.models import AuditEvent

if TYPE_CHECKING:
    from billit_mcp.persistence.database import HostedDatabase


class HostedAuditService:
    """Write redacted hosted audit events."""

    def __init__(self, database: HostedDatabase) -> None:
        self._database = database

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

        async with self._database.session() as session:
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

"""Hosted idempotency state service."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from billit_mcp.auth.security import sha256_text
from billit_mcp.persistence.models import IdempotencyRecord
from billit_mcp.services.invoice_workflow import IdempotencyStart, IdempotencyState

if TYPE_CHECKING:
    from billit_mcp.persistence.database import HostedDatabase


class HostedIdempotencyService:
    """Manage hosted idempotency records for write workflows."""

    def __init__(self, database: HostedDatabase) -> None:
        self._database = database

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

        async with self._database.session() as session:
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
        async with self._database.session() as session:
            record = await session.get(IdempotencyRecord, idempotency_id, with_for_update=True)
            if record is None:
                return
            record.status = status
            record.billit_resource_type = billit_resource_type
            record.billit_resource_id = billit_resource_id
            record.billit_error_code = billit_error_code
            record.updated_at = datetime.now(UTC)

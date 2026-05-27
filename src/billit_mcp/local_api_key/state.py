"""Local-only SQLite state for API-key stdio safety controls."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LocalConfirmationChallenge:
    """A pending or consumed local confirmation challenge."""

    challenge_id: str
    status: str
    operation_type: str
    resource_type: str
    resource_id: str
    company_party_id: int
    operation_hash: str
    confirmation_token_hash: str
    expires_at: datetime
    summary_json: dict[str, Any]


@dataclass(frozen=True)
class LocalIdempotencyRecord:
    """A local idempotency operation record."""

    idempotency_id: str
    status: str
    operation_hash: str
    billit_resource_type: str | None
    billit_resource_id: str | None
    billit_error_code: str | None


@dataclass(frozen=True)
class LocalIdempotencyStart:
    """Local idempotency record plus insertion state."""

    record: LocalIdempotencyRecord
    created: bool


class LocalStateStore:
    """SQLite-backed local state that stores only redacted operational metadata."""

    def __init__(self, path: Path | str = Path(".local/billit-mcp-api-key-state.db")) -> None:
        self.path = Path(path)
        self._schema_ready = False

    def audit(
        self,
        *,
        audit_id: str,
        event_type: str,
        operation_class: str,
        tool_name: str | None,
        outcome: str,
        correlation_id: str,
        environment: str | None = None,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
        latency_ms: int | None = None,
    ) -> None:
        """Append a redacted local audit event."""

        with self._connect() as connection:
            connection.execute(
                """
                insert into local_audit_events (
                    audit_id, created_at, event_type, operation_class, tool_name,
                    outcome, error_code, correlation_id, environment, company_party_id,
                    resource_type, resource_id, summary_json, latency_ms
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    _now_iso(),
                    event_type,
                    operation_class,
                    tool_name,
                    outcome,
                    error_code,
                    correlation_id,
                    environment,
                    company_party_id,
                    resource_type,
                    resource_id,
                    _json(summary or {}),
                    latency_ms,
                ),
            )

    def create_confirmation_challenge(
        self,
        *,
        challenge_id: str,
        confirmation_token_hash: str,
        expires_at: datetime,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        company_party_id: int,
        operation_hash: str,
        summary: dict[str, Any],
    ) -> None:
        """Create a pending confirmation challenge."""

        with self._connect() as connection:
            connection.execute(
                """
                insert into local_confirmation_challenges (
                    challenge_id, created_at, expires_at, status, operation_type,
                    resource_type, resource_id, company_party_id, operation_hash,
                    confirmation_token_hash, summary_json
                )
                values (?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    challenge_id,
                    _now_iso(),
                    expires_at.isoformat(),
                    operation_type,
                    resource_type,
                    resource_id,
                    company_party_id,
                    operation_hash,
                    confirmation_token_hash,
                    _json(summary),
                ),
            )

    def get_confirmation_challenge(self, challenge_id: str) -> LocalConfirmationChallenge | None:
        """Return a confirmation challenge by id."""

        with self._connect() as connection:
            row = connection.execute(
                """
                select challenge_id, status, operation_type, resource_type, resource_id,
                       company_party_id, operation_hash, confirmation_token_hash,
                       expires_at, summary_json
                from local_confirmation_challenges
                where challenge_id = ?
                """,
                (challenge_id,),
            ).fetchone()
        if row is None:
            return None
        return LocalConfirmationChallenge(
            challenge_id=str(row["challenge_id"]),
            status=str(row["status"]),
            operation_type=str(row["operation_type"]),
            resource_type=str(row["resource_type"]),
            resource_id=str(row["resource_id"]),
            company_party_id=int(row["company_party_id"]),
            operation_hash=str(row["operation_hash"]),
            confirmation_token_hash=str(row["confirmation_token_hash"]),
            expires_at=datetime.fromisoformat(str(row["expires_at"])),
            summary_json=json.loads(str(row["summary_json"])),
        )

    def consume_confirmation_challenge(
        self,
        *,
        challenge_id: str,
        confirmation_token_hash: str,
        operation_hash: str,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        company_party_id: int,
    ) -> bool:
        """Atomically consume a pending challenge with all invariants checked."""

        with self._connect() as connection:
            result = connection.execute(
                """
                update local_confirmation_challenges
                   set status = 'consumed', consumed_at = ?
                 where challenge_id = ?
                   and status = 'pending'
                   and confirmation_token_hash = ?
                   and operation_hash = ?
                   and operation_type = ?
                   and resource_type = ?
                   and resource_id = ?
                   and company_party_id = ?
                   and expires_at > ?
                """,
                (
                    _now_iso(),
                    challenge_id,
                    confirmation_token_hash,
                    operation_hash,
                    operation_type,
                    resource_type,
                    resource_id,
                    company_party_id,
                    _now_iso(),
                ),
            )
            return result.rowcount == 1

    def record_idempotency_started(
        self,
        *,
        idempotency_id: str,
        company_party_id: int,
        operation_type: str,
        idempotency_key_hash: str,
        operation_hash: str,
    ) -> LocalIdempotencyStart:
        """Create or return a local idempotency record."""

        with self._connect() as connection:
            existing = self._get_idempotency_record(
                connection=connection,
                company_party_id=company_party_id,
                operation_type=operation_type,
                idempotency_key_hash=idempotency_key_hash,
            )
            if existing is not None:
                return LocalIdempotencyStart(record=existing, created=False)
            connection.execute(
                """
                insert into local_idempotency_records (
                    idempotency_id, created_at, updated_at, company_party_id,
                    operation_type, idempotency_key_hash, operation_hash, status
                )
                values (?, ?, ?, ?, ?, ?, ?, 'started')
                """,
                (
                    idempotency_id,
                    _now_iso(),
                    _now_iso(),
                    company_party_id,
                    operation_type,
                    idempotency_key_hash,
                    operation_hash,
                ),
            )
            created = self._get_idempotency_record(
                connection=connection,
                company_party_id=company_party_id,
                operation_type=operation_type,
                idempotency_key_hash=idempotency_key_hash,
            )
        if created is None:  # pragma: no cover - SQLite insert succeeded but row disappeared.
            raise RuntimeError("Local idempotency record was not created")
        return LocalIdempotencyStart(record=created, created=True)

    def record_idempotency_outcome(
        self,
        *,
        idempotency_id: str,
        status: str,
        billit_resource_type: str | None = None,
        billit_resource_id: str | None = None,
        billit_error_code: str | None = None,
    ) -> bool:
        """Update the final outcome of a local idempotent operation."""

        with self._connect() as connection:
            result = connection.execute(
                """
                update local_idempotency_records
                   set status = ?,
                       billit_resource_type = ?,
                       billit_resource_id = ?,
                       billit_error_code = ?,
                       updated_at = ?
                 where idempotency_id = ?
                """,
                (
                    status,
                    billit_resource_type,
                    billit_resource_id,
                    billit_error_code,
                    _now_iso(),
                    idempotency_id,
                ),
            )
            return result.rowcount == 1

    def audit_events(self) -> list[dict[str, Any]]:
        """Return audit events for focused local tests."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                select event_type, operation_class, tool_name, outcome, error_code,
                       correlation_id, environment, company_party_id, resource_type,
                       resource_id, summary_json, latency_ms
                  from local_audit_events
                 order by created_at, audit_id
                """
            ).fetchall()
        events: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["summary_json"] = json.loads(str(item["summary_json"]))
            events.append(item)
        return events

    def _get_idempotency_record(
        self,
        *,
        connection: sqlite3.Connection,
        company_party_id: int,
        operation_type: str,
        idempotency_key_hash: str,
    ) -> LocalIdempotencyRecord | None:
        row = connection.execute(
            """
            select idempotency_id, status, operation_hash, billit_resource_type,
                   billit_resource_id, billit_error_code
              from local_idempotency_records
             where company_party_id = ?
               and operation_type = ?
               and idempotency_key_hash = ?
            """,
            (company_party_id, operation_type, idempotency_key_hash),
        ).fetchone()
        if row is None:
            return None
        return LocalIdempotencyRecord(
            idempotency_id=str(row["idempotency_id"]),
            status=str(row["status"]),
            operation_hash=str(row["operation_hash"]),
            billit_resource_type=row["billit_resource_type"],
            billit_resource_id=row["billit_resource_id"],
            billit_error_code=row["billit_error_code"],
        )

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        if not self._schema_ready:
            self._ensure_schema(connection)
            self._schema_ready = True
        return connection

    @staticmethod
    def _ensure_schema(connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            create table if not exists local_audit_events (
                audit_id text primary key,
                created_at text not null,
                event_type text not null,
                operation_class text not null,
                tool_name text,
                outcome text not null,
                error_code text,
                correlation_id text not null,
                environment text,
                company_party_id integer,
                resource_type text,
                resource_id text,
                summary_json text not null,
                latency_ms integer
            );

            create table if not exists local_confirmation_challenges (
                challenge_id text primary key,
                created_at text not null,
                expires_at text not null,
                consumed_at text,
                status text not null,
                operation_type text not null,
                resource_type text not null,
                resource_id text not null,
                company_party_id integer not null,
                operation_hash text not null,
                confirmation_token_hash text not null,
                summary_json text not null
            );

            create table if not exists local_idempotency_records (
                idempotency_id text primary key,
                created_at text not null,
                updated_at text not null,
                company_party_id integer not null,
                operation_type text not null,
                idempotency_key_hash text not null,
                operation_hash text not null,
                status text not null,
                billit_resource_type text,
                billit_resource_id text,
                billit_error_code text,
                unique(company_party_id, operation_type, idempotency_key_hash)
            );
            """
        )


def _json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()

"""Local confirmation and idempotency services over LocalStateStore."""

from __future__ import annotations

import uuid
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Protocol, cast

from billit_mcp.local_api_key.common import LocalToolError, hash_payload, hash_text, token
from billit_mcp.services.invoice_workflow import (
    IdempotencyState,
    PendingSendChallenge,
    SendChallenge,
)

if TYPE_CHECKING:
    from billit_mcp.local_api_key.state import LocalConfirmationChallenge, LocalIdempotencyRecord


class StateRuntime(Protocol):
    """Runtime hooks needed by local state services."""

    state: Any

    @property
    def configured_party_id(self) -> int:
        """Configured numeric company PartyID."""
        ...

    def audit_sync(
        self,
        *,
        event_type: str,
        operation_class: str,
        outcome: str,
        correlation_id: str,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        """Record an audit event from sync state code."""
        ...


class LocalWorkflowState:
    """Local state helpers for invoice idempotency and confirmation challenges."""

    def __init__(self, runtime: StateRuntime) -> None:
        self.runtime = runtime

    def create_confirmation_challenge(
        self,
        *,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        summary: dict[str, Any],
    ) -> SendChallenge:
        """Create a server-owned local confirmation challenge."""

        challenge_id = str(uuid.uuid4())
        confirmation_token = token()
        operation_hash = hash_payload(summary)
        expires_at = datetime.now(UTC) + timedelta(minutes=10)
        self.runtime.state.create_confirmation_challenge(
            challenge_id=challenge_id,
            confirmation_token_hash=hash_text(confirmation_token),
            expires_at=expires_at,
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            company_party_id=self.runtime.configured_party_id,
            operation_hash=operation_hash,
            summary=summary,
        )
        self.runtime.audit_sync(
            event_type="confirmation_challenge_created",
            operation_class="confirmation",
            outcome="challenge_created",
            correlation_id=token(),
            company_party_id=self.runtime.configured_party_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary={"operation_type": operation_type, "resource_type": resource_type},
        )
        return SendChallenge(
            challenge_id=challenge_id,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
            expires_at=expires_at.isoformat(),
            summary=summary,
        )

    def get_pending_confirmation_challenge(self, challenge_id: str) -> LocalConfirmationChallenge:
        """Load a pending challenge without consuming it."""

        challenge = cast(
            "LocalConfirmationChallenge | None",
            self.runtime.state.get_confirmation_challenge(challenge_id),
        )
        if challenge is None:
            raise LocalToolError("challenge_not_found", "Confirmation challenge not found")
        if challenge.status != "pending" or challenge.expires_at <= datetime.now(UTC):
            raise LocalToolError("challenge_expired", "Confirmation challenge is not pending")
        if challenge.company_party_id != self.runtime.configured_party_id:
            raise LocalToolError("challenge_mismatch", "Challenge company does not match")
        return challenge

    def get_pending_send_challenge(self, challenge_id: str) -> PendingSendChallenge:
        """Load a pending invoice-send challenge."""

        challenge = self.get_pending_confirmation_challenge(challenge_id)
        if challenge.operation_type != "invoice_send" or challenge.resource_type != "order":
            raise LocalToolError("challenge_mismatch", "Challenge operation does not match")
        return PendingSendChallenge(
            challenge_id=challenge.challenge_id,
            operation_hash=challenge.operation_hash,
            resource_id=challenge.resource_id,
            summary=challenge.summary_json,
        )

    def consume_confirmation_challenge(
        self,
        *,
        challenge: LocalConfirmationChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a pending confirmation challenge."""

        if challenge.confirmation_token_hash != hash_text(confirmation_token):
            raise LocalToolError("challenge_token_invalid", "Confirmation token is invalid")
        consumed = self.runtime.state.consume_confirmation_challenge(
            challenge_id=challenge.challenge_id,
            confirmation_token_hash=hash_text(confirmation_token),
            operation_hash=operation_hash,
            operation_type=challenge.operation_type,
            resource_type=challenge.resource_type,
            resource_id=challenge.resource_id,
            company_party_id=self.runtime.configured_party_id,
        )
        if not consumed:
            raise LocalToolError("challenge_mismatch", "Confirmation was not consumed")
        self.runtime.audit_sync(
            event_type="confirmation_challenge_consumed",
            operation_class="confirmation",
            outcome="challenge_consumed",
            correlation_id=token(),
            company_party_id=self.runtime.configured_party_id,
            resource_type=challenge.resource_type,
            resource_id=challenge.resource_id,
            summary={"operation_type": challenge.operation_type},
        )

    def consume_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a pending invoice-send challenge."""

        local_challenge = self.get_pending_confirmation_challenge(challenge.challenge_id)
        self.consume_confirmation_challenge(
            challenge=local_challenge,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

    def record_idempotency_started(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> LocalIdempotencyRecord | None:
        """Create or return a local idempotency record."""

        if not idempotency_key:
            return None
        record = cast(
            "LocalIdempotencyRecord",
            self.runtime.state.record_idempotency_started(
                idempotency_id=str(uuid.uuid4()),
                company_party_id=self.runtime.configured_party_id,
                operation_type=operation_type,
                idempotency_key_hash=hash_text(idempotency_key),
                operation_hash=operation_hash,
            ),
        )
        if record.operation_hash != operation_hash:
            raise LocalToolError(
                "idempotency_conflict",
                "Idempotency key was already used for a different operation",
                error_code="IDEMPOTENCY_CONFLICT",
            )
        return record

    async def idempotency_state(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyState | None:
        """Return workflow idempotency state."""

        record = self.record_idempotency_started(
            operation_type=operation_type,
            idempotency_key=idempotency_key,
            operation_hash=operation_hash,
        )
        if record is None:
            return None
        return IdempotencyState(
            idempotency_id=record.idempotency_id,
            status=record.status,
            operation_hash=record.operation_hash,
            billit_resource_id=record.billit_resource_id,
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
        """Persist a workflow idempotency outcome."""

        with suppress(Exception):
            self.runtime.state.record_idempotency_outcome(
                idempotency_id=idempotency_id,
                status=status,
                billit_resource_type=billit_resource_type,
                billit_resource_id=billit_resource_id,
                billit_error_code=billit_error_code,
            )

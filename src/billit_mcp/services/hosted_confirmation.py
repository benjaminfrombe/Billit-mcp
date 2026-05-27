"""Hosted confirmation challenge service."""

from __future__ import annotations

from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from sqlalchemy import update

from billit_mcp.auth.security import ensure_aware_utc, random_token_urlsafe, sha256_text
from billit_mcp.persistence.models import ConfirmationChallenge
from billit_mcp.services.hosted_errors import HostedToolError
from billit_mcp.services.invoice_workflow import hash_payload

if TYPE_CHECKING:
    from billit_mcp.persistence.database import HostedDatabase
    from billit_mcp.services.hosted_audit import HostedAuditService


class HostedConfirmationService:
    """Create, inspect, and atomically consume hosted confirmations."""

    def __init__(self, *, database: HostedDatabase, audit: HostedAuditService) -> None:
        self._database = database
        self._audit = audit

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
        async with self._database.session() as session:
            session.add(challenge)
        await self._audit.audit(
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

        async with self._database.session() as session:
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
            await self._audit.audit(
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

        async with self._database.session() as session:
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

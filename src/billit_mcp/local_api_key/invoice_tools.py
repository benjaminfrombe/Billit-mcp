"""Local API-key invoice tool handlers backed by the shared workflow."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Protocol

from billit_mcp.local_api_key.common import LocalToolError, ToolResult, success
from billit_mcp.services.invoice import build_invoice_preflight
from billit_mcp.services.invoice_workflow import (
    ConfirmSendRequest,
    DraftInvoiceRequest,
    IdempotencyStart,
    PendingSendChallenge,
    PrepareSendRequest,
    SendChallenge,
    confirm_invoice_send,
    create_invoice_draft,
    prepare_invoice_send,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from billit_mcp.local_api_key.client import LocalAuditedBillitClient


class LocalInvoiceRuntime(Protocol):
    """Runtime hooks required by local invoice tools."""

    @property
    def configured_party_id(self) -> int:
        """Configured numeric PartyID."""
        ...

    @property
    def local_writes_enabled(self) -> bool:
        """Whether local draft writes are enabled."""
        ...

    async def audited_client(self, *, tool_name: str) -> LocalAuditedBillitClient:
        """Return an audited Billit client."""
        ...

    async def execute_tool(
        self,
        *,
        tool_name: str,
        operation_class: str,
        handler: Any,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> ToolResult:
        """Execute a local tool with central audit/error handling."""
        ...

    def configured_party_id_or_none(self) -> int | None:
        """Return configured numeric PartyID when available."""
        ...

    def local_warnings(self) -> list[str]:
        """Return local warnings."""
        ...

    def settings_party_id(self) -> str:
        """Return configured PartyID without coercion."""
        ...

    def require_writes_enabled(self) -> None:
        """Fail unless draft writes are enabled."""
        ...

    def require_sends_enabled(self) -> None:
        """Fail unless sending is enabled."""
        ...

    async def validate_company_for_write(self, *, tool_name: str) -> None:
        """Validate company entitlement for writes/sends."""
        ...

    async def local_idempotency_state(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyStart | None:
        """Create or load local idempotency state."""
        ...

    async def record_local_idempotency_outcome(
        self,
        *,
        idempotency_id: str,
        status: str,
        billit_resource_type: str | None = None,
        billit_resource_id: str | None = None,
        billit_error_code: str | None = None,
    ) -> None:
        """Persist local idempotency outcome."""
        ...

    def create_local_send_challenge(
        self,
        *,
        resource_id: str,
        summary: dict[str, Any],
    ) -> SendChallenge:
        """Create a local send confirmation challenge."""
        ...

    def get_pending_local_send_challenge(self, *, challenge_id: str) -> PendingSendChallenge:
        """Load a pending local send challenge."""
        ...

    def consume_local_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Consume a local send challenge."""
        ...


class LocalInvoiceTools:
    """Local invoice tool methods exposed through LocalAPIKeyRuntime."""

    def __init__(self, runtime: LocalInvoiceRuntime) -> None:
        self.runtime = runtime

    async def invoice_prepare(
        self,
        *,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> ToolResult:
        """Run a read-only invoice preflight."""

        async def handler() -> ToolResult:
            preflight = build_invoice_preflight(
                customer=customer,
                lines=lines,
                order_date=order_date,
                expiry_date=expiry_date,
                desired_transport=desired_transport,
            )
            preflight["company_party_id"] = self.runtime.settings_party_id()
            preflight["writes_enabled"] = self.runtime.local_writes_enabled
            preflight["warnings"] = list(preflight.get("warnings") or []) + (
                self.runtime.local_warnings()
            )
            return success(preflight)

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.prepare",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def invoice_create_draft(
        self,
        *,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        external_provider_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> ToolResult:
        """Create a Billit sales invoice draft without sending it."""

        async def handler() -> ToolResult:
            return await create_invoice_draft(
                LocalInvoiceWorkflowAdapter(self.runtime),
                DraftInvoiceRequest(
                    customer=customer,
                    lines=lines,
                    order_date=order_date,
                    expiry_date=expiry_date,
                    external_provider_id=external_provider_id,
                    idempotency_key=idempotency_key,
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.create_draft",
            operation_class="write",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def invoice_prepare_send(
        self,
        *,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> ToolResult:
        """Prepare a local confirmation challenge before sending an invoice."""

        async def handler() -> ToolResult:
            return await prepare_invoice_send(
                LocalInvoiceWorkflowAdapter(self.runtime),
                PrepareSendRequest(
                    order_id=order_id,
                    transport_type=transport_type,
                    strict_transport=strict_transport,
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.prepare_send",
            operation_class="external_send",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def invoice_confirm_send(
        self,
        *,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> ToolResult:
        """Consume a confirmation challenge and send the invoice."""

        async def handler() -> ToolResult:
            return await confirm_invoice_send(
                LocalInvoiceWorkflowAdapter(self.runtime),
                ConfirmSendRequest(
                    challenge_id=challenge_id,
                    confirmation_token=confirmation_token,
                    operation_hash=operation_hash,
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.confirm_send",
            operation_class="external_send",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
            resource_type="confirmation_challenge",
            resource_id=challenge_id,
        )


class LocalInvoiceWorkflowAdapter:
    """Local adapter for the shared invoice workflow."""

    def __init__(self, runtime: LocalInvoiceRuntime) -> None:
        self.runtime = runtime

    @property
    def company_party_id(self) -> int:
        return self.runtime.configured_party_id

    async def ensure_create_draft_allowed(self, *, tool_name: str) -> None:
        self.runtime.require_writes_enabled()
        await self.runtime.validate_company_for_write(tool_name=tool_name)

    async def ensure_send_allowed(self, *, tool_name: str) -> None:
        self.runtime.require_sends_enabled()
        await self.runtime.validate_company_for_write(tool_name=tool_name)

    @asynccontextmanager
    async def billit_client(self, *, tool_name: str) -> AsyncIterator[LocalAuditedBillitClient]:
        yield await self.runtime.audited_client(tool_name=tool_name)

    async def record_idempotency_started(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyStart | None:
        return await self.runtime.local_idempotency_state(
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
        await self.runtime.record_local_idempotency_outcome(
            idempotency_id=idempotency_id,
            status=status,
            billit_resource_type=billit_resource_type,
            billit_resource_id=billit_resource_id,
            billit_error_code=billit_error_code,
        )

    async def create_send_challenge(
        self,
        *,
        resource_id: str,
        summary: dict[str, Any],
    ) -> SendChallenge:
        return self.runtime.create_local_send_challenge(resource_id=resource_id, summary=summary)

    async def get_pending_send_challenge(self, *, challenge_id: str) -> PendingSendChallenge:
        return self.runtime.get_pending_local_send_challenge(challenge_id=challenge_id)

    async def consume_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        self.runtime.consume_local_send_challenge(
            challenge=challenge,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

    def workflow_error(
        self,
        error_type: str,
        message: str,
        *,
        error_code: str | None = None,
    ) -> Exception:
        return LocalToolError(error_type, message, error_code=error_code)

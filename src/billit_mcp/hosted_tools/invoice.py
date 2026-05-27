"""Hosted OAuth invoice MCP tools backed by the shared workflow."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from billit_mcp.services.hosted_runtime import (
    AuditedBillitClient,
    HostedClaims,
    HostedToolError,
    HostedToolRuntime,
    success,
)
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

    from mcp.server.fastmcp import FastMCP

    from billit_mcp.persistence.models import BillitConnection


def register_invoice_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register hosted invoice tools."""

    @mcp.tool(name="billit.invoice.prepare")
    async def invoice_prepare(
        environment: str,
        company_party_id: int,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> dict[str, Any]:
        """Read-only invoice preflight."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            connection = await runtime.resolve_connection(
                actor_id=typed.actor_id,
                environment=environment,
            )
            await runtime.validate_company(
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
            )
            return success(
                build_invoice_preflight(
                    customer=customer,
                    lines=lines,
                    order_date=order_date,
                    expiry_date=expiry_date,
                    desired_transport=desired_transport,
                )
            )

        return await runtime.execute_tool(
            tool_name="billit.invoice.prepare",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.create_draft")
    async def invoice_create_draft(
        environment: str,
        company_party_id: int,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        external_provider_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a Billit sales invoice draft without sending it."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            return await create_invoice_draft(
                HostedInvoiceWorkflowAdapter(
                    runtime=runtime,
                    claims=runtime.typed_claims(claims),
                    environment=environment,
                    company_party_id=company_party_id,
                ),
                DraftInvoiceRequest(
                    customer=customer,
                    lines=lines,
                    order_date=order_date,
                    expiry_date=expiry_date,
                    external_provider_id=external_provider_id,
                    idempotency_key=idempotency_key,
                ),
            )

        return await runtime.execute_tool(
            tool_name="billit.invoice.create_draft",
            required_scope="billit:invoice.create",
            operation_class="write",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.prepare_send")
    async def invoice_prepare_send(
        environment: str,
        company_party_id: int,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> dict[str, Any]:
        """Prepare a server-owned confirmation challenge before sending an invoice."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            return await prepare_invoice_send(
                HostedInvoiceWorkflowAdapter(
                    runtime=runtime,
                    claims=runtime.typed_claims(claims),
                    environment=environment,
                    company_party_id=company_party_id,
                ),
                PrepareSendRequest(
                    order_id=order_id,
                    transport_type=transport_type,
                    strict_transport=strict_transport,
                ),
            )

        return await runtime.execute_tool(
            tool_name="billit.invoice.prepare_send",
            required_scope="billit:invoice.send",
            operation_class="external_send",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.confirm_send")
    async def invoice_confirm_send(
        environment: str,
        company_party_id: int,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> dict[str, Any]:
        """Consume a confirmation challenge and send the invoice."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            return await confirm_invoice_send(
                HostedInvoiceWorkflowAdapter(
                    runtime=runtime,
                    claims=runtime.typed_claims(claims),
                    environment=environment,
                    company_party_id=company_party_id,
                ),
                ConfirmSendRequest(
                    challenge_id=challenge_id,
                    confirmation_token=confirmation_token,
                    operation_hash=operation_hash,
                ),
            )

        return await runtime.execute_tool(
            tool_name="billit.invoice.confirm_send",
            required_scope="billit:invoice.send",
            operation_class="external_send",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.get_delivery_status")
    async def invoice_get_delivery_status(
        environment: str,
        company_party_id: int,
        order_id: int,
    ) -> dict[str, Any]:
        """Return a concise fresh-read delivery status."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            async with runtime.authorized_billit_client(
                claims=typed,
                environment=environment,
                company_party_id=company_party_id,
                tool_name="billit.invoice.get_delivery_status",
            ) as (_, client):
                order = await client.request("GET", f"/orders/{order_id}")
            if not order.get("success"):
                return order
            data = order.get("data") or {}
            return success(
                {
                    "order_id": order_id,
                    "is_sent": bool(data.get("IsSent")),
                    "paid": bool(data.get("Paid")),
                    "delivery_status": data.get("DeliveryStatus")
                    or data.get("OrderStatus")
                    or "unknown",
                    "messages": data.get("Messages") or [],
                    "source": "fresh_billit_read",
                }
            )

        return await runtime.execute_tool(
            tool_name="billit.invoice.get_delivery_status",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )


class HostedInvoiceWorkflowAdapter:
    """Hosted adapter for the shared invoice workflow."""

    def __init__(
        self,
        *,
        runtime: HostedToolRuntime,
        claims: HostedClaims,
        environment: str,
        company_party_id: int,
    ) -> None:
        self.runtime = runtime
        self.claims = claims
        self.environment = environment
        self._company_party_id = company_party_id
        self._connection: BillitConnection | None = None

    @property
    def company_party_id(self) -> int:
        return self._company_party_id

    async def ensure_create_draft_allowed(self, *, tool_name: str) -> None:
        await self._authorized_connection()

    async def ensure_send_allowed(self, *, tool_name: str) -> None:
        await self._authorized_connection()

    @asynccontextmanager
    async def billit_client(self, *, tool_name: str) -> AsyncIterator[AuditedBillitClient]:
        async with self.runtime.authorized_billit_client(
            claims=self.claims,
            environment=self.environment,
            company_party_id=self.company_party_id,
            tool_name=tool_name,
        ) as (connection, client):
            self._connection = connection
            yield client

    async def record_idempotency_started(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyStart | None:
        if not idempotency_key:
            return None
        connection = await self._authorized_connection()
        return await self.runtime.record_idempotency_started(
            connection_id=connection.connection_id,
            company_party_id=self.company_party_id,
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
        await self.runtime.record_idempotency_outcome(
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
        connection = await self._authorized_connection()
        payload = await self.runtime.create_confirmation_challenge(
            actor_id=self.claims.actor_id,
            client_id=self.claims.client_id,
            connection_id=connection.connection_id,
            environment=self.environment,
            company_party_id=self.company_party_id,
            operation_type="invoice_send",
            resource_type="order",
            resource_id=resource_id,
            required_scope="billit:invoice.send",
            summary=summary,
        )
        return SendChallenge(
            challenge_id=str(payload["challenge_id"]),
            confirmation_token=str(payload["confirmation_token"]),
            operation_hash=str(payload["operation_hash"]),
            expires_at=str(payload["expires_at"]),
            summary=dict(payload["summary"]),
        )

    async def get_pending_send_challenge(self, *, challenge_id: str) -> PendingSendChallenge:
        challenge = await self.runtime.get_pending_confirmation_challenge(
            challenge_id=challenge_id,
            actor_id=self.claims.actor_id,
            client_id=self.claims.client_id,
            environment=self.environment,
            company_party_id=self.company_party_id,
            operation_type="invoice_send",
            resource_type="order",
            required_scope="billit:invoice.send",
        )
        return PendingSendChallenge(
            challenge_id=challenge.challenge_id,
            operation_hash=challenge.operation_hash,
            resource_id=str(challenge.resource_id),
            summary=challenge.summary_json,
        )

    async def consume_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        connection = await self._authorized_connection()
        await self.runtime.consume_confirmation_challenge(
            challenge_id=challenge.challenge_id,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
            actor_id=self.claims.actor_id,
            client_id=self.claims.client_id,
            connection_id=connection.connection_id,
            environment=self.environment,
            company_party_id=self.company_party_id,
            operation_type="invoice_send",
            resource_type="order",
            resource_id=challenge.resource_id,
            required_scope="billit:invoice.send",
        )

    def workflow_error(
        self,
        error_type: str,
        message: str,
        *,
        error_code: str | None = None,
    ) -> Exception:
        return HostedToolError(error_type, message, error_code=error_code)

    async def _authorized_connection(self) -> BillitConnection:
        if self._connection is None:
            self._connection = await self.runtime.resolve_connection(
                actor_id=self.claims.actor_id,
                environment=self.environment,
            )
        await self.runtime.validate_company(
            connection_id=self._connection.connection_id,
            environment=self.environment,
            company_party_id=self.company_party_id,
        )
        return self._connection

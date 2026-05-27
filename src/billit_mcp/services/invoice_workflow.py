"""Shared guarded invoice workflows for Billit MCP runtimes."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Protocol, cast

from billit_mcp.services.invoice import build_invoice_payload, build_invoice_preflight

ToolResult = dict[str, Any]


class InvoiceBillitClient(Protocol):
    """Minimal Billit client protocol used by invoice workflows."""

    async def request(self, method: str, path: str, **kwargs: Any) -> ToolResult:
        """Perform a Billit API request."""
        ...


@dataclass(frozen=True)
class DraftInvoiceRequest:
    """Typed internal request for invoice draft creation."""

    customer: dict[str, Any]
    lines: list[dict[str, Any]]
    order_date: str
    expiry_date: str
    external_provider_id: str | None = None
    idempotency_key: str | None = None


@dataclass(frozen=True)
class PrepareSendRequest:
    """Typed internal request for invoice send preparation."""

    order_id: int
    transport_type: str
    strict_transport: bool = True


@dataclass(frozen=True)
class ConfirmSendRequest:
    """Typed internal request for invoice send confirmation."""

    challenge_id: str
    confirmation_token: str
    operation_hash: str


@dataclass(frozen=True)
class IdempotencyState:
    """Stored idempotency state returned by runtime adapters."""

    idempotency_id: str
    status: str
    operation_hash: str
    billit_resource_id: str | None


@dataclass(frozen=True)
class IdempotencyStart:
    """Result of starting an idempotent workflow operation."""

    record: IdempotencyState
    created: bool


@dataclass(frozen=True)
class SendChallenge:
    """Challenge created by a runtime adapter."""

    challenge_id: str
    confirmation_token: str
    operation_hash: str
    expires_at: str
    summary: dict[str, Any]

    def to_result(self) -> dict[str, Any]:
        """Return the public challenge payload."""

        return {
            "challenge_id": self.challenge_id,
            "confirmation_token": self.confirmation_token,
            "operation_hash": self.operation_hash,
            "expires_at": self.expires_at,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class PendingSendChallenge:
    """Pending send challenge loaded for confirmation."""

    challenge_id: str
    operation_hash: str
    resource_id: str
    summary: dict[str, Any]


class InvoiceWorkflowAdapter(Protocol):
    """Runtime-specific policy and persistence hooks for invoice workflows."""

    @property
    def company_party_id(self) -> int:
        """Billit company PartyID for this workflow."""
        ...

    async def ensure_create_draft_allowed(self, *, tool_name: str) -> None:
        """Fail unless invoice draft creation is allowed."""
        ...

    async def ensure_send_allowed(self, *, tool_name: str) -> None:
        """Fail unless external invoice sending is allowed."""
        ...

    def billit_client(self, *, tool_name: str) -> Any:
        """Return an audited Billit client context."""
        ...

    async def record_idempotency_started(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyStart | None:
        """Create or load an idempotency record."""
        ...

    async def record_idempotency_outcome(
        self,
        *,
        idempotency_id: str,
        status: str,
        billit_resource_type: str | None = None,
        billit_resource_id: str | None = None,
        billit_error_code: str | None = None,
    ) -> None:
        """Persist an idempotency outcome."""
        ...

    async def create_send_challenge(
        self,
        *,
        resource_id: str,
        summary: dict[str, Any],
    ) -> SendChallenge:
        """Create a pending send confirmation challenge."""
        ...

    async def get_pending_send_challenge(self, *, challenge_id: str) -> PendingSendChallenge:
        """Load a pending send challenge without consuming it."""
        ...

    async def consume_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a pending send challenge."""
        ...

    def workflow_error(
        self,
        error_type: str,
        message: str,
        *,
        error_code: str | None = None,
    ) -> Exception:
        """Build a runtime-specific structured exception."""
        ...


async def create_invoice_draft(
    adapter: InvoiceWorkflowAdapter,
    request: DraftInvoiceRequest,
) -> ToolResult:
    """Create a Billit invoice draft through a guarded runtime adapter."""

    await adapter.ensure_create_draft_allowed(tool_name="billit.invoice.create_draft")
    preflight = build_invoice_preflight(
        customer=request.customer,
        lines=request.lines,
        order_date=request.order_date,
        expiry_date=request.expiry_date,
    )
    if preflight["blockers"]:
        raise adapter.workflow_error(
            "invoice_preflight_blocked",
            "Invoice draft request has blocking validation issues",
            error_code="INVOICE_PREFLIGHT_BLOCKED",
        )

    payload = build_invoice_payload(
        customer=request.customer,
        lines=request.lines,
        order_date=request.order_date,
        expiry_date=request.expiry_date,
        external_provider_id=request.external_provider_id,
    )
    operation_hash = hash_payload(payload)
    idempotency = await adapter.record_idempotency_started(
        operation_type="invoice_create_draft",
        idempotency_key=request.idempotency_key,
        operation_hash=operation_hash,
    )
    record = idempotency.record if idempotency is not None else None
    if record is not None:
        if record.operation_hash != operation_hash:
            raise adapter.workflow_error(
                "idempotency_conflict",
                "Idempotency key was already used for a different invoice draft",
                error_code="IDEMPOTENCY_CONFLICT",
            )
        if record.status == "succeeded" and record.billit_resource_id:
            return success(
                {
                    "idempotent_replay": True,
                    "order_id": record.billit_resource_id,
                }
            )
        if idempotency is not None and not idempotency.created:
            raise adapter.workflow_error(
                "idempotency_replay_blocked",
                f"Prior idempotent draft outcome is {record.status}",
                error_code="IDEMPOTENCY_REPLAY_BLOCKED",
            )

    idempotency_id = record.idempotency_id if record is not None else None
    headers = {"Idempotency-Key": request.idempotency_key} if request.idempotency_key else None
    async with adapter.billit_client(tool_name="billit.invoice.create_draft") as client:
        try:
            response = cast(
                "ToolResult",
                await client.request("POST", "/orders", json=payload, headers=headers),
            )
        except Exception:
            if idempotency_id is not None:
                await adapter.record_idempotency_outcome(
                    idempotency_id=idempotency_id,
                    status="unknown_side_effect",
                    billit_error_code="BILLIT_REQUEST_EXCEPTION",
                )
            raise

        order_id = order_id_from_response(response.get("data"))
        if response.get("success") and order_id:
            if idempotency_id is not None:
                await adapter.record_idempotency_outcome(
                    idempotency_id=idempotency_id,
                    status="succeeded",
                    billit_resource_type="order",
                    billit_resource_id=str(order_id),
                )
            try:
                detail = cast("ToolResult", await client.request("GET", f"/orders/{order_id}"))
            except Exception:
                return response
            return detail if detail.get("success") else response

        if idempotency_id is not None:
            await adapter.record_idempotency_outcome(
                idempotency_id=idempotency_id,
                status="failed",
                billit_error_code=str(response.get("error_code") or "BILLIT_ERROR"),
            )
        return response


async def prepare_invoice_send(
    adapter: InvoiceWorkflowAdapter,
    request: PrepareSendRequest,
) -> ToolResult:
    """Refetch an invoice and create a guarded send confirmation challenge."""

    await adapter.ensure_send_allowed(tool_name="billit.invoice.prepare_send")
    async with adapter.billit_client(tool_name="billit.invoice.prepare_send") as client:
        order = cast("ToolResult", await client.request("GET", f"/orders/{request.order_id}"))
    if not order.get("success"):
        return order

    summary = redacted_send_summary(
        order.get("data"),
        company_party_id=adapter.company_party_id,
        transport_type=normalize_transport_type(request.transport_type),
        strict_transport=request.strict_transport,
    )
    raise_if_send_ineligible(adapter, summary)
    challenge = await adapter.create_send_challenge(
        resource_id=str(request.order_id),
        summary=summary,
    )
    return success(challenge.to_result())


async def confirm_invoice_send(
    adapter: InvoiceWorkflowAdapter,
    request: ConfirmSendRequest,
) -> ToolResult:
    """Refetch, revalidate, atomically consume, then send an invoice."""

    await adapter.ensure_send_allowed(tool_name="billit.invoice.confirm_send")
    challenge = await adapter.get_pending_send_challenge(challenge_id=request.challenge_id)
    order_id = challenge.resource_id
    async with adapter.billit_client(tool_name="billit.invoice.confirm_send") as client:
        order = cast("ToolResult", await client.request("GET", f"/orders/{order_id}"))
        if not order.get("success"):
            return order
        current_summary = redacted_send_summary(
            order.get("data"),
            company_party_id=adapter.company_party_id,
            transport_type=str(challenge.summary["transport_type"]),
            strict_transport=bool(challenge.summary["strict_transport"]),
        )
        raise_if_send_ineligible(adapter, current_summary)
        current_hash = hash_payload(current_summary)
        if current_hash != challenge.operation_hash or current_hash != request.operation_hash:
            raise adapter.workflow_error(
                "challenge_changed",
                "Invoice state changed after the confirmation challenge was created",
            )
        await adapter.consume_send_challenge(
            challenge=challenge,
            confirmation_token=request.confirmation_token,
            operation_hash=current_hash,
        )
        headers = {"StrictTransportType": "true"} if current_summary["strict_transport"] else None
        return cast(
            "ToolResult",
            await client.request(
                "POST",
                "/orders/commands/send",
                json={
                    "Transporttype": current_summary["transport_type"],
                    "OrderIDs": [int(order_id)],
                },
                headers=headers,
            ),
        )


def success(data: Any) -> ToolResult:
    """Return a successful tool result envelope."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def hash_payload(payload: dict[str, Any]) -> str:
    """Return a stable hash for a JSON-compatible operation payload."""

    return hash_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def hash_text(value: str) -> str:
    """Return a SHA-256 hex digest."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def redacted_send_summary(
    order: Any,
    *,
    company_party_id: int,
    transport_type: str,
    strict_transport: bool,
) -> dict[str, Any]:
    """Build the canonical redacted send summary used in confirmation challenges."""

    data = order if isinstance(order, dict) else {}
    raw_customer = data.get("Customer")
    customer: dict[str, Any] = raw_customer if isinstance(raw_customer, dict) else {}
    return {
        "company_party_id": company_party_id,
        "order_id": data.get("OrderID") or data.get("ID"),
        "invoice_number": data.get("OrderNumber"),
        "customer_name_hash": hash_text(str(customer.get("Name") or "")),
        "customer_vat_hash": hash_text(str(customer.get("VATNumber") or "")),
        "amount_including_vat": data.get("TotalIncl") or data.get("TotalInclVAT"),
        "currency": data.get("Currency") or "EUR",
        "is_sent": bool(data.get("IsSent")),
        "order_status": data.get("OrderStatus"),
        "transport_type": transport_type,
        "strict_transport": strict_transport,
        "fallback_allowed": not strict_transport,
    }


def raise_if_send_ineligible(
    adapter: InvoiceWorkflowAdapter,
    summary: dict[str, Any],
) -> None:
    """Fail if a redacted send summary cannot be sent."""

    if not summary.get("order_id"):
        raise adapter.workflow_error(
            "invoice_send_ineligible",
            "Order ID is missing from Billit order",
        )
    if summary.get("is_sent"):
        raise adapter.workflow_error(
            "invoice_already_sent",
            "Invoice is already marked as sent",
        )


def normalize_transport_type(value: str) -> str:
    """Normalize public transport aliases to Billit transport values."""

    return "SMTP" if value == "Email" else value


def order_id_from_response(data: Any) -> Any:
    """Extract a Billit order id from a create response."""

    if isinstance(data, dict):
        return data.get("OrderID") or data.get("ID")
    return data

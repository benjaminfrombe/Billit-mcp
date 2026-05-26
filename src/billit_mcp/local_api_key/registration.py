"""Registration for curated local API-key Billit MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from billit_mcp.local_api_key.runtime import LocalAPIKeyRuntime


def register_local_api_key_tools(mcp: FastMCP, runtime: LocalAPIKeyRuntime) -> None:
    """Register exactly the local/private API-key stdio tool surface."""

    @mcp.tool(name="billit.connection_status")
    async def connection_status() -> dict[str, Any]:
        """Check local API-key auth, Billit account access, and safety gates."""

        return await runtime.connection_status()

    @mcp.tool(name="billit.list_companies")
    async def list_companies() -> dict[str, Any]:
        """List companies visible in Billit accountInformation."""

        return await runtime.list_companies()

    @mcp.tool(name="billit.search_orders")
    async def search_orders(
        direction: str | None = None,
        order_type: str | None = None,
        customer_name: str | None = None,
        vat_number: str | None = None,
        paid: bool | None = None,
        modified_since: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search orders with structured allowlisted filters only."""

        return await runtime.search_orders(
            direction=direction,
            order_type=order_type,
            customer_name=customer_name,
            vat_number=vat_number,
            paid=paid,
            modified_since=modified_since,
            limit=limit,
        )

    @mcp.tool(name="billit.get_order")
    async def get_order(order_id: int) -> dict[str, Any]:
        """Fetch one Billit order by ID."""

        return await runtime.get_order(order_id=order_id)

    @mcp.tool(name="billit.resolve_party")
    async def resolve_party(
        role: str,
        name: str | None = None,
        vat_number: str | None = None,
        email: str | None = None,
        external_provider_id: str | None = None,
    ) -> dict[str, Any]:
        """Resolve a customer or supplier without guessing on ambiguity."""

        return await runtime.resolve_party(
            role=role,
            name=name,
            vat_number=vat_number,
            email=email,
            external_provider_id=external_provider_id,
        )

    @mcp.tool(name="billit.lookup_peppol_receiver")
    async def lookup_peppol_receiver(identifier: str) -> dict[str, Any]:
        """Check whether a receiver identifier is visible on Peppol."""

        return await runtime.lookup_peppol_receiver(identifier=identifier)

    @mcp.tool(name="billit.list_financial_transactions")
    async def list_financial_transactions(limit: int = 20) -> dict[str, Any]:
        """List financial transactions without arbitrary OData."""

        return await runtime.list_financial_transactions(limit=limit)

    @mcp.tool(name="billit.list_reports")
    async def list_reports() -> dict[str, Any]:
        """List available Billit reports."""

        return await runtime.list_reports()

    @mcp.tool(name="billit.get_report")
    async def get_report(
        report_id: str,
        parameters: dict[str, str | int | float | bool] | None = None,
    ) -> dict[str, Any]:
        """Get a Billit report by id with bounded scalar parameters."""

        return await runtime.get_report(report_id=report_id, parameters=parameters)

    @mcp.tool(name="billit.invoice.prepare")
    async def invoice_prepare(
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> dict[str, Any]:
        """Validate an invoice draft request without writing."""

        return await runtime.invoice_prepare(
            customer=customer,
            lines=lines,
            order_date=order_date,
            expiry_date=expiry_date,
            desired_transport=desired_transport,
        )

    @mcp.tool(name="billit.invoice.create_draft")
    async def invoice_create_draft(
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        external_provider_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a local-gated Billit sales invoice draft without sending."""

        return await runtime.invoice_create_draft(
            customer=customer,
            lines=lines,
            order_date=order_date,
            expiry_date=expiry_date,
            external_provider_id=external_provider_id,
            idempotency_key=idempotency_key,
        )

    @mcp.tool(name="billit.invoice.prepare_send")
    async def invoice_prepare_send(
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> dict[str, Any]:
        """Create a server-owned confirmation challenge before sending."""

        return await runtime.invoice_prepare_send(
            order_id=order_id,
            transport_type=transport_type,
            strict_transport=strict_transport,
        )

    @mcp.tool(name="billit.invoice.confirm_send")
    async def invoice_confirm_send(
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> dict[str, Any]:
        """Consume a confirmation challenge and send after revalidation."""

        return await runtime.invoice_confirm_send(
            challenge_id=challenge_id,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

    @mcp.tool(name="billit.invoice.get_delivery_status")
    async def invoice_get_delivery_status(order_id: int) -> dict[str, Any]:
        """Return fresh Billit delivery status for one invoice/order."""

        return await runtime.invoice_get_delivery_status(order_id=order_id)

    @mcp.tool(name="billit.invoice.summary")
    async def invoice_summary(start_date: str, end_date: str) -> dict[str, Any]:
        """Summarize sales invoices through the shared read-only helper."""

        return await runtime.invoice_summary(start_date=start_date, end_date=end_date)

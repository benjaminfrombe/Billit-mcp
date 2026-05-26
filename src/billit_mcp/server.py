#!/usr/bin/env python3
"""Billit MCP Server - Model Context Protocol server for Billit API integration."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP

from billit.client import BillitAPIClient
from billit.dependencies import build_client
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.services import ai_composite
from billit.smart_search import run_smart_search

_mcp_client: BillitAPIClient | None = None


@asynccontextmanager
async def mcp_lifespan(server: FastMCP) -> AsyncIterator[dict[str, object]]:
    """Close the shared MCP Billit client when the stdio server shuts down."""

    try:
        yield {}
    finally:
        await close_mcp_client()


# Initialize the MCP server
mcp = FastMCP(
    "billit-mcp",
    dependencies=["httpx", "pydantic", "python-dotenv"],
    lifespan=mcp_lifespan,
)


async def get_client() -> BillitAPIClient:
    """Get the process-scoped MCP Billit API client."""

    global _mcp_client
    if _mcp_client is None or getattr(_mcp_client.client, "is_closed", False):
        _mcp_client = build_client()
    return _mcp_client


async def close_mcp_client() -> None:
    """Close and clear the process-scoped MCP Billit API client."""

    global _mcp_client
    if _mcp_client is not None:
        await _mcp_client.close()
        _mcp_client = None


# Party Management Tools
@mcp.tool()
async def list_parties(
    party_type: str, odata_filter: str | None = None, skip: int = 0, top: int = 120
) -> dict[str, Any]:
    """List parties (customers or suppliers).

    Args:
        party_type: Type of party - 'Customer' or 'Supplier'
        odata_filter: Optional OData filter expression
        skip: Number of records to skip for pagination
        top: Maximum number of records to return (max 120)
    """
    client = await get_client()
    params = list_params(
        skip=skip,
        top=top,
        odata_filter=odata_filter,
        extra={"PartyType": party_type},
    )

    return await client.request("GET", "/parties", params=params)


@mcp.tool()
async def create_party(party_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new party (customer or supplier).

    Args:
        party_data: Party data including Name, PartyType, VAT number, etc.
    """
    client = await get_client()
    return await client.request("POST", "/parties", json=party_data)


@mcp.tool()
async def get_party(party_id: int) -> dict[str, Any]:
    """Get details of a specific party.

    Args:
        party_id: The ID of the party to retrieve
    """
    client = await get_client()
    return await client.request("GET", f"/parties/{party_id}")


@mcp.tool()
async def update_party(party_id: int, party_updates: dict[str, Any]) -> dict[str, Any]:
    """Update an existing party.

    Args:
        party_id: The ID of the party to update
        party_updates: Fields to update
    """
    client = await get_client()
    return await client.request("PATCH", f"/parties/{party_id}", json=party_updates)


# Product Management Tools
@mcp.tool()
async def list_products(
    odata_filter: str | None = None, skip: int = 0, top: int = 120
) -> dict[str, Any]:
    """List products.

    Args:
        odata_filter: Optional OData filter expression
        skip: Number of records to skip for pagination
        top: Maximum number of records to return (max 120)
    """
    client = await get_client()
    params = list_params(skip=skip, top=top, odata_filter=odata_filter)

    return await client.request("GET", "/products", params=params)


@mcp.tool()
async def get_product(product_id: int) -> dict[str, Any]:
    """Get details of a specific product.

    Args:
        product_id: The ID of the product to retrieve
    """
    client = await get_client()
    return await client.request("GET", f"/products/{product_id}")


@mcp.tool()
async def upsert_product(product_data: dict[str, Any]) -> dict[str, Any]:
    """Create or update a product.

    Args:
        product_data: Product data including Description, UnitPrice, VAT rate, etc.
    """
    client = await get_client()
    return await client.request("POST", "/products", json=product_data)


# Order Management Tools
@mcp.tool()
async def list_orders(
    odata_filter: str | None = None, skip: int = 0, top: int = 120
) -> dict[str, Any]:
    """List orders (invoices, credit notes, etc.).

    Args:
        odata_filter: Optional OData filter expression
        skip: Number of records to skip for pagination
        top: Maximum number of records to return (max 120)
    """
    client = await get_client()
    params = list_params(skip=skip, top=top, odata_filter=odata_filter)

    return await client.request("GET", "/orders", params=params)


@mcp.tool()
async def create_order(order_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new order (invoice, credit note, etc.).

    Args:
        order_data: Order data including Customer, OrderLines, etc.
    """
    client = await get_client()
    return await client.request("POST", "/orders", json=order_data)


@mcp.tool()
async def get_order(order_id: int) -> dict[str, Any]:
    """Get details of a specific order.

    Args:
        order_id: The ID of the order to retrieve
    """
    client = await get_client()
    return await client.request("GET", f"/orders/{order_id}")


@mcp.tool()
async def update_order(order_id: int, order_updates: dict[str, Any]) -> dict[str, Any]:
    """Update an existing order.

    Args:
        order_id: The ID of the order to update
        order_updates: Fields to update (Paid, PaidDate, IsSent, etc.)
    """
    client = await get_client()
    return await client.request("PATCH", f"/orders/{order_id}", json=order_updates)


@mcp.tool()
async def delete_order(order_id: int) -> dict[str, Any]:
    """Delete a draft order.

    Args:
        order_id: The ID of the order to delete
    """
    client = await get_client()
    return await client.request("DELETE", f"/orders/{order_id}")


@mcp.tool()
async def record_payment(order_id: int, payment_info: dict[str, Any]) -> dict[str, Any]:
    """Record a payment for an order.

    Args:
        order_id: The ID of the order
        payment_info: Payment details including amount, date, etc.
    """
    client = await get_client()
    return await client.request("POST", f"/orders/{order_id}/payment", json=payment_info)


@mcp.tool()
async def send_order(
    order_ids: list[int], transport_type: str, strict_transport: bool = False
) -> dict[str, Any]:
    """Send one or more orders via specified transport.

    Args:
        order_ids: List of order IDs to send
        transport_type: Transport method ('Peppol', 'SMTP', 'Email', etc.)
        strict_transport: If True, prevent fallback to alternative transport methods

    Valid transport types:
    - SMTP: Email delivery (requires valid customer email)
    - Peppol: Peppol e-invoicing network
    - Letter: Physical mail
    - SDI: Italian network
    - KSeF: Polish network
    - OSA: Hungarian network
    - ANAF: Romanian network
    - SAT: Mexican network

    Important behaviors:
    - Peppol is tried first if customer is registered on network
    - If Peppol fails, fallback to email (unless strict_transport=True)
    - Email fallback requires valid customer email address
    - Set strict_transport=True to prevent fallbacks and enforce exact transport

    Common errors:
    - "TheCustomer_0_DoesNotHaveAValidEmailAddress": Update customer email first
    - Order must be in correct status (ToSend, not already Sent)

    Note: 'Email' auto-corrected to 'SMTP'
    """
    client = await get_client()

    # Auto-correct Email → SMTP
    if transport_type == "Email":
        transport_type = "SMTP"

    # Prepare data for Billit API
    data = {
        "Transporttype": transport_type,
        "OrderIDs": order_ids,
    }

    # Add headers if strict transport is requested
    headers = {}
    if strict_transport:
        headers["StrictTransportType"] = "true"

    # Call Billit API directly
    return await client.request("POST", "/orders/commands/send", json=data, headers=headers)


@mcp.tool()
async def add_booking_entries(order_id: int, entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Add booking entries to an order.

    Args:
        order_id: The ID of the order
        entries: List of booking entries
    """
    client = await get_client()
    return await client.request("POST", f"/orders/{order_id}/booking", json=entries)


@mcp.tool()
async def list_deleted_orders() -> dict[str, Any]:
    """List recently deleted orders."""
    client = await get_client()
    return await client.request("GET", "/orders/deleted")


# Financial Transaction Tools
@mcp.tool()
async def list_financial_transactions(
    odata_filter: str | None = None, skip: int = 0, top: int = 120
) -> dict[str, Any]:
    """List financial transactions.

    Args:
        odata_filter: Optional OData filter expression
        skip: Number of records to skip for pagination
        top: Maximum number of records to return (max 120)
    """
    client = await get_client()
    params = list_params(skip=skip, top=top, odata_filter=odata_filter)

    return await client.request("GET", FINANCIAL_TRANSACTIONS_ENDPOINT, params=params)


@mcp.tool()
async def import_transactions_file(file_path: str) -> dict[str, Any]:
    """Import a bank statement file.

    Args:
        file_path: Path to the file to import (CODA, CSV, etc.)
    """
    client = await get_client()
    return await client.request(
        "POST", f"{FINANCIAL_TRANSACTIONS_ENDPOINT}/importFile", json={"file_path": file_path}
    )


@mcp.tool()
async def confirm_transaction_import(import_id: str) -> dict[str, Any]:
    """Confirm a transaction import.

    Args:
        import_id: The ID of the import to confirm
    """
    client = await get_client()
    return await client.request(
        "POST", f"{FINANCIAL_TRANSACTIONS_ENDPOINT}/commands/import", json={"import_id": import_id}
    )


# Account Management Tools
@mcp.tool()
async def get_account_information() -> dict[str, Any]:
    """Get information about the authenticated account."""
    client = await get_client()
    return await client.request("GET", "/account/accountInformation")


@mcp.tool()
async def get_sso_token() -> dict[str, Any]:
    """Get a Single Sign-On token for the Billit web UI."""
    client = await get_client()
    return await client.request("GET", "/account/ssoToken")


@mcp.tool()
async def get_next_sequence_number(sequence_type: str, consume: bool = False) -> dict[str, Any]:
    """Get the next sequence number.

    Args:
        sequence_type: Type of sequence (e.g., 'Income-Invoice')
        consume: If True, consume the number
    """
    client = await get_client()
    data = {"sequence_type": sequence_type, "consume": consume}
    return await client.request("POST", "/account/sequences", json=data)


@mcp.tool()
async def register_company(company_data: dict[str, Any]) -> dict[str, Any]:
    """Register a new company (for accountants).

    Args:
        company_data: Company registration data
    """
    client = await get_client()
    return await client.request("POST", "/account/registercompany", json=company_data)


# Document Management Tools
@mcp.tool()
async def list_documents(
    odata_filter: str | None = None, skip: int = 0, top: int = 120
) -> dict[str, Any]:
    """List documents.

    Args:
        odata_filter: Optional OData filter expression
        skip: Number of records to skip for pagination
        top: Maximum number of records to return (max 120)
    """
    client = await get_client()
    params = list_params(skip=skip, top=top, odata_filter=odata_filter)

    return await client.request("GET", "/documents", params=params)


@mcp.tool()
async def upload_document(file_path: str, metadata: dict[str, Any]) -> dict[str, Any]:
    """Upload a document.

    Args:
        file_path: Path to the file to upload
        metadata: Document metadata
    """
    client = await get_client()
    data = {"file_path": file_path, "metadata": metadata}
    return await client.request("POST", "/documents", json=data)


@mcp.tool()
async def get_document(document_id: int) -> dict[str, Any]:
    """Get details of a specific document.

    Args:
        document_id: The ID of the document to retrieve
    """
    client = await get_client()
    return await client.request("GET", f"/documents/{document_id}")


@mcp.tool()
async def download_file(file_id: str) -> dict[str, Any]:
    """Download a file.

    Args:
        file_id: The ID of the file to download
    """
    client = await get_client()
    return await client.request("GET", f"/files/{file_id}")


# Webhook Management Tools
@mcp.tool()
async def create_webhook(url: str, entity_type: str, update_type: str) -> dict[str, Any]:
    """Create a webhook subscription.

    Args:
        url: The webhook URL
        entity_type: Type of entity to subscribe to
        update_type: Type of updates to receive
    """
    client = await get_client()
    data = {"url": url, "entity_type": entity_type, "update_type": update_type}
    return await client.request("POST", "/webhook", json=data)


@mcp.tool()
async def list_webhooks() -> dict[str, Any]:
    """List all configured webhooks."""
    client = await get_client()
    return await client.request("GET", "/webhook")


@mcp.tool()
async def delete_webhook(webhook_id: str) -> dict[str, Any]:
    """Delete a webhook subscription.

    Args:
        webhook_id: The ID of the webhook to delete
    """
    client = await get_client()
    return await client.request("DELETE", f"/webhook/{webhook_id}")


@mcp.tool()
async def refresh_webhook_secret(webhook_id: str) -> dict[str, Any]:
    """Refresh the signing secret for a webhook.

    Args:
        webhook_id: The ID of the webhook
    """
    client = await get_client()
    return await client.request("POST", f"/webhook/{webhook_id}/refresh")


# Peppol E-invoicing Tools
@mcp.tool()
async def check_peppol_participant(identifier: str) -> dict[str, Any]:
    """Check if a company is a Peppol participant.

    Args:
        identifier: Company identifier (VAT, CBE, GLN, etc.)
    """
    client = await get_client()
    return await client.request("GET", f"/peppol/participantInformation/{identifier}")


@mcp.tool()
async def register_peppol_participant(registration_data: dict[str, Any]) -> dict[str, Any]:
    """Register as a Peppol participant.

    Args:
        registration_data: Registration information
    """
    client = await get_client()
    return await client.request("POST", "/peppol/participants", json=registration_data)


@mcp.tool()
async def send_peppol_invoice(order_id: int) -> dict[str, Any]:
    """Send an invoice via Peppol.

    Args:
        order_id: The ID of the order to send
    """
    client = await get_client()
    return await client.request("POST", "/peppol/sendOrder", json={"order_id": order_id})


# AI Composite Tools
@mcp.tool()
async def suggest_payment_reconciliation() -> dict[str, Any]:
    """Get AI-powered payment reconciliation suggestions."""
    client = await get_client()
    return await ai_composite.suggest_payment_reconciliation(client)


@mcp.tool()
async def generate_invoice_summary(start_date: str, end_date: str) -> dict[str, Any]:
    """Generate an AI-powered invoice summary.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    client = await get_client()
    return await ai_composite.generate_invoice_summary(client, start_date, end_date)


@mcp.tool()
async def list_overdue_invoices() -> dict[str, Any]:
    """List all overdue invoices."""
    client = await get_client()
    return await ai_composite.list_overdue_invoices(client)


@mcp.tool()
async def get_cashflow_overview(period: str) -> dict[str, Any]:
    """Get a cashflow overview for a period.

    Args:
        period: Period specification (e.g., '2024-Q1', '2024-01')
    """
    client = await get_client()
    return await ai_composite.get_cashflow_overview(client, period)


@mcp.tool()
async def smart_search(
    query: str, entity_type: str = "all", max_results: int = 10
) -> dict[str, Any]:
    """Search orders, parties, and products with semantic-ish matching."""

    client = await get_client()
    return await run_smart_search(client, query, entity_type, max_results)


@mcp.tool()
async def debug_smart_search(
    query: str, entity_type: str = "orders", max_results: int = 3
) -> dict[str, Any]:
    """Debug smart search by returning the shared search result with parsed terms."""

    client = await get_client()
    result = await run_smart_search(client, query, entity_type, max_results)
    if result["success"]:
        result["data"]["debug_info"] = {
            "entity_type": entity_type,
            "max_results": max_results,
        }
    return result


# Utility Tools
@mcp.tool()
async def search_company(keywords: str) -> dict[str, Any]:
    """Search for a company by name or number.

    Args:
        keywords: Search keywords
    """
    client = await get_client()
    return await client.request("GET", f"/misc/companysearch/{keywords}")


@mcp.tool()
async def get_type_codes(code_type: str) -> dict[str, Any]:
    """Get available codes for a type.

    Args:
        code_type: Type of codes (e.g., 'VATRate', 'Currency', 'OrderStatus')
    """
    client = await get_client()
    return await client.request("GET", f"/misc/typecodes/{code_type}")


@mcp.tool()
async def list_available_reports() -> dict[str, Any]:
    """List all available report types."""
    client = await get_client()
    return await client.request("GET", report_endpoint())


@mcp.tool()
async def get_report(report_id: str, **params: Any) -> dict[str, Any]:
    """Generate and download a report.

    Args:
        report_id: The ID of the report type
        **params: Additional report parameters (depends on report type)
    """
    client = await get_client()
    return await client.request("GET", report_endpoint(report_id), params=params)

"""AI-enhanced composite tools."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from ..client import BillitAPIClient
from ..dependencies import get_client
from ..services import ai_composite
from ..smart_search import run_smart_search

router = APIRouter()


@router.get("/ai/suggest-payment-reconciliation")
async def suggest_payment_reconciliation(
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Match outstanding invoices with bank transactions by reference and amount."""

    return await ai_composite.suggest_payment_reconciliation(client)


@router.get("/ai/invoice-summary")
async def generate_invoice_summary(
    start_date: str,
    end_date: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return the number and total of sales invoices between two dates."""

    return await ai_composite.generate_invoice_summary(client, start_date, end_date)


@router.get("/ai/expense-summary")
async def generate_expense_summary(
    start_date: str,
    end_date: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return the number and total of purchase invoices between two dates."""

    return await ai_composite.generate_expense_summary(client, start_date, end_date)


@router.get("/ai/cashflow")
async def get_cashflow_overview(
    period: str, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Summarize cash inflow and outflow for the given YYYY-MM period."""

    return await ai_composite.get_cashflow_overview(client, period)


@router.post("/ai/categorize-expense/{invoice_id}")
async def categorize_expense_invoice(
    invoice_id: int, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Suggest a simple category for an expense invoice based on keywords."""

    return await ai_composite.categorize_expense_invoice(client, invoice_id)


@router.get("/ai/overdue-invoices")
async def list_overdue_invoices(
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return all overdue sales invoices."""

    return await ai_composite.list_overdue_invoices(client)


@router.get("/ai/supplier-spend/{supplier_id}")
async def get_supplier_spend_summary(
    supplier_id: int,
    period: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return total spend with a supplier for the given period."""

    return await ai_composite.get_supplier_spend_summary(client, supplier_id, period)


@router.get("/ai/customer-revenue/{customer_id}")
async def get_customer_revenue_summary(
    customer_id: int,
    period: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return total revenue from a customer for the given period."""

    return await ai_composite.get_customer_revenue_summary(client, customer_id, period)


@router.get("/ai/duplicate-contacts")
async def find_duplicate_contacts(
    similarity_threshold: float = 0.9,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Find contacts with similar names using a naive ratio check."""

    return await ai_composite.find_duplicate_contacts(client, similarity_threshold)


@router.post("/ai/normalize-address/{party_id}")
async def normalize_contact_address(
    party_id: int, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Normalize address fields of a contact in a very naive way."""

    return await ai_composite.normalize_contact_address(client, party_id)


@router.post("/ai/create-invoice-from-text")
async def create_invoice_from_text(
    data: dict[str, Any], client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Create a very simple sales invoice using provided free text."""

    return await ai_composite.create_invoice_from_text(client, data)


@router.get("/ai/smart-search")
async def smart_search(
    query: str,
    entity_type: str = "all",
    max_results: int = 10,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Search orders, parties, and products with semantic-ish matching."""

    return await run_smart_search(client, query, entity_type, max_results)

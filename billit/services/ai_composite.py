"""Shared AI-style composite operations for Billit data."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, MAX_PAGE_SIZE
from billit.smart_search import normalize_items, similarity

if TYPE_CHECKING:
    from billit.protocols import BillitRequester


def period_bounds(period: str) -> tuple[str, str]:
    """Return inclusive start and exclusive end dates for YYYY or YYYY-MM periods."""

    parts = period.split("-")
    if len(parts) == 1:
        year = int(parts[0])
        return f"{year}-01-01", f"{year + 1}-01-01"
    year, month = [int(part) for part in parts]
    start = f"{year}-{month:02d}-01"
    if month == 12:
        return start, f"{year + 1}-01-01"
    return start, f"{year}-{month + 1:02d}-01"


def odata_date(value: str) -> str:
    """Return a Billit OData date literal."""

    return f"datetime'{value}'"


async def suggest_payment_reconciliation(client: BillitRequester) -> dict[str, Any]:
    """Match outstanding invoices with bank transactions by reference and amount."""

    invoices_resp = await client.request(
        "GET",
        "/orders",
        params={"$filter": "ToPay gt 0", "$top": MAX_PAGE_SIZE},
    )
    tx_resp = await client.request(
        "GET",
        FINANCIAL_TRANSACTIONS_ENDPOINT,
        params={"$top": MAX_PAGE_SIZE},
    )
    if not invoices_resp.get("success"):
        return invoices_resp
    if not tx_resp.get("success"):
        return tx_resp
    invoices = normalize_items(invoices_resp.get("data"))
    transactions = normalize_items(tx_resp.get("data"))
    matches: list[dict[str, Any]] = []
    for inv in invoices:
        ref = inv.get("PaymentReference") or inv.get("StructuredCommunication")
        amount = float(inv.get("ToPay", 0))
        for tx in transactions:
            tx_ref = tx.get("PaymentReference") or tx.get("Communication")
            if ref and ref == tx_ref:
                matches.append(
                    {
                        "order_id": inv.get("OrderID"),
                        "transaction_id": tx.get("FinancialTransactionID"),
                        "amount": amount,
                    }
                )
                break
            tx_amount = float(tx.get("Amount", 0))
            if amount and abs(amount - tx_amount) < 0.01:
                matches.append(
                    {
                        "order_id": inv.get("OrderID"),
                        "transaction_id": tx.get("FinancialTransactionID"),
                        "amount": amount,
                    }
                )
                break
    return {"success": True, "data": matches, "error": None, "error_code": None}


async def generate_invoice_summary(
    client: BillitRequester,
    start_date: str,
    end_date: str,
) -> dict[str, Any]:
    """Return the number and total of sales invoices between two dates."""

    params = {
        "$filter": (
            f"OrderDirection eq 'Income' and OrderDate ge {odata_date(start_date)} "
            f"and OrderDate le {odata_date(end_date)}"
        ),
        "$top": MAX_PAGE_SIZE,
    }
    resp = await client.request("GET", "/orders", params=params)
    if not resp.get("success"):
        return resp
    invoices = normalize_items(resp.get("data"))
    total = sum(float(i.get("TotalIncl", 0)) for i in invoices)
    return {
        "success": True,
        "data": {"count": len(invoices), "total_incl": total},
        "error": None,
        "error_code": None,
    }


async def generate_expense_summary(
    client: BillitRequester,
    start_date: str,
    end_date: str,
) -> dict[str, Any]:
    """Return the number and total of purchase invoices between two dates."""

    params = {
        "$filter": (
            f"OrderDirection eq 'Cost' and OrderDate ge {odata_date(start_date)} "
            f"and OrderDate le {odata_date(end_date)}"
        ),
        "$top": MAX_PAGE_SIZE,
    }
    resp = await client.request("GET", "/orders", params=params)
    if not resp.get("success"):
        return resp
    invoices = normalize_items(resp.get("data"))
    total = sum(float(i.get("TotalIncl", 0)) for i in invoices)
    return {
        "success": True,
        "data": {"count": len(invoices), "total_incl": total},
        "error": None,
        "error_code": None,
    }


async def get_cashflow_overview(client: BillitRequester, period: str) -> dict[str, Any]:
    """Summarize cash inflow and outflow for the given YYYY-MM period."""

    start, end_date = period_bounds(period)

    income_resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": (
                f"OrderDirection eq 'Income' and OrderDate ge {odata_date(start)} "
                f"and OrderDate lt {odata_date(end_date)}"
            ),
            "$top": MAX_PAGE_SIZE,
        },
    )
    if not income_resp.get("success"):
        return income_resp
    cost_resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": (
                f"OrderDirection eq 'Cost' and OrderDate ge {odata_date(start)} "
                f"and OrderDate lt {odata_date(end_date)}"
            ),
            "$top": MAX_PAGE_SIZE,
        },
    )
    if not cost_resp.get("success"):
        return cost_resp
    income_orders = normalize_items(income_resp.get("data"))
    cost_orders = normalize_items(cost_resp.get("data"))
    income_total = sum(float(o.get("TotalIncl", 0)) for o in income_orders)
    cost_total = sum(float(o.get("TotalIncl", 0)) for o in cost_orders)
    return {
        "success": True,
        "data": {
            "income": income_total,
            "cost": cost_total,
            "net": income_total - cost_total,
        },
        "error": None,
        "error_code": None,
    }


async def categorize_expense_invoice(client: BillitRequester, invoice_id: int) -> dict[str, Any]:
    """Suggest a simple category for an expense invoice based on keywords."""

    resp = await client.request("GET", f"/orders/{invoice_id}")
    if not resp.get("success"):
        return resp
    order = resp.get("data", {}) or {}
    lines = order.get("OrderLines", []) or []
    text = " ".join(line.get("Description", "") for line in lines).lower()
    if any(k in text for k in ["fuel", "gas", "petrol", "diesel"]):
        category = "Transport"
    elif any(k in text for k in ["office", "paper", "stationery"]):
        category = "Office"
    else:
        category = "General"
    return {
        "success": True,
        "data": {"invoice_id": invoice_id, "category": category},
        "error": None,
        "error_code": None,
    }


async def list_overdue_invoices(client: BillitRequester) -> dict[str, Any]:
    """Return all overdue sales invoices."""

    resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": "Overdue eq true and OrderDirection eq 'Income'",
            "$top": MAX_PAGE_SIZE,
        },
    )
    if not resp.get("success"):
        return resp
    data = normalize_items(resp.get("data"))
    overdue_ids = [o.get("OrderID") for o in data]
    return {
        "success": True,
        "data": overdue_ids,
        "error": None,
        "error_code": None,
    }


async def get_supplier_spend_summary(
    client: BillitRequester,
    supplier_id: int,
    period: str,
) -> dict[str, Any]:
    """Return total spend with a supplier for the given period."""

    start, end_date = period_bounds(period)
    params = {
        "$filter": (
            f"OrderDirection eq 'Cost' and Party/PartyID eq {supplier_id} "
            f"and OrderDate ge {odata_date(start)} and OrderDate lt {odata_date(end_date)}"
        ),
        "$top": MAX_PAGE_SIZE,
    }
    resp = await client.request("GET", "/orders", params=params)
    if not resp.get("success"):
        return resp
    orders = normalize_items(resp.get("data"))
    total = sum(float(o.get("TotalIncl", 0)) for o in orders)
    return {
        "success": True,
        "data": {"supplier_id": supplier_id, "total_incl": total},
        "error": None,
        "error_code": None,
    }


async def get_customer_revenue_summary(
    client: BillitRequester,
    customer_id: int,
    period: str,
) -> dict[str, Any]:
    """Return total revenue from a customer for the given period."""

    start, end_date = period_bounds(period)
    params = {
        "$filter": (
            f"OrderDirection eq 'Income' and Party/PartyID eq {customer_id} "
            f"and OrderDate ge {odata_date(start)} and OrderDate lt {odata_date(end_date)}"
        ),
        "$top": MAX_PAGE_SIZE,
    }
    resp = await client.request("GET", "/orders", params=params)
    if not resp.get("success"):
        return resp
    orders = normalize_items(resp.get("data"))
    total = sum(float(o.get("TotalIncl", 0)) for o in orders)
    return {
        "success": True,
        "data": {"customer_id": customer_id, "total_incl": total},
        "error": None,
        "error_code": None,
    }


async def find_duplicate_contacts(
    client: BillitRequester,
    similarity_threshold: float = 0.9,
) -> dict[str, Any]:
    """Find contacts with similar names using a naive ratio check."""

    resp = await client.request("GET", "/parties", params={"$top": MAX_PAGE_SIZE})
    if not resp.get("success"):
        return resp
    parties = normalize_items(resp.get("data"))
    duplicates: list[dict[str, Any]] = []
    names = [(p.get("PartyID"), p.get("Name", "")) for p in parties]
    for i, (id_a, name_a) in enumerate(names):
        for id_b, name_b in names[i + 1 :]:
            if not name_a or not name_b:
                continue
            ratio = similarity(name_a, name_b)
            if ratio >= similarity_threshold:
                duplicates.append({"party_a": id_a, "party_b": id_b, "similarity": ratio})
    return {"success": True, "data": duplicates, "error": None, "error_code": None}


async def normalize_contact_address(client: BillitRequester, party_id: int) -> dict[str, Any]:
    """Normalize address fields of a contact in a simple deterministic way."""

    resp = await client.request("GET", f"/parties/{party_id}")
    if not resp.get("success"):
        return resp
    party = resp.get("data", {}) or {}
    addresses = party.get("Addresses", []) or []
    normalized = []
    for addr in addresses:
        normalized.append({k: str(v).title() if isinstance(v, str) else v for k, v in addr.items()})
    await client.request(
        "PATCH",
        f"/parties/{party_id}",
        json={"Addresses": normalized},
    )
    return {
        "success": True,
        "data": {"party_id": party_id, "normalized": True},
        "error": None,
        "error_code": None,
    }


async def create_invoice_from_text(
    client: BillitRequester,
    data: dict[str, Any],
) -> dict[str, Any]:
    """Create a simple sales invoice using provided free text."""

    text_description = data.get("text_description", "")
    invoice = {
        "OrderDirection": "Income",
        "OrderType": "Invoice",
        "Customer": {"Name": "Text Import"},
        "OrderLines": [
            {
                "Description": text_description,
                "Quantity": 1,
                "UnitPriceExcl": 0.0,
            }
        ],
    }
    return await client.request("POST", "/orders", json=invoice)

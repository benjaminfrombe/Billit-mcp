"""Shared AI-style composite operations for Billit data."""

from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING, Any

from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, MAX_PAGE_SIZE, list_params
from billit.smart_search import normalize_items, similarity

if TYPE_CHECKING:
    from billit.protocols import BillitRequester

Envelope = dict[str, Any]
_PERIOD_PATTERN = re.compile(r"^(?P<year>\d{4})(?:-(?P<month>0[1-9]|1[0-2]))?$")


def success(data: Any) -> Envelope:
    """Return the standard Billit MCP success envelope."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def failure(error: str, error_code: str) -> Envelope:
    """Return the standard Billit MCP failure envelope."""

    return {"success": False, "data": None, "error": error, "error_code": error_code}


def period_bounds(period: str) -> tuple[str, str] | None:
    """Return inclusive start and exclusive end dates for YYYY or YYYY-MM periods."""

    match = _PERIOD_PATTERN.fullmatch(period)
    if match is None:
        return None
    year = int(match.group("year"))
    month_value = match.group("month")
    if month_value is None:
        return f"{year}-01-01", f"{year + 1}-01-01"
    month = int(month_value)
    start = f"{year}-{month:02d}-01"
    if month == 12:
        return start, f"{year + 1}-01-01"
    return start, f"{year}-{month + 1:02d}-01"


def invalid_period(period: str) -> Envelope:
    """Return a typed error for unsupported composite periods."""

    return failure(
        f"Unsupported period '{period}'. Use YYYY or YYYY-MM.",
        "INVALID_PERIOD",
    )


def odata_date(value: str) -> str:
    """Return a Billit OData date literal."""

    return f"datetime'{value}'"


def money(value: Any) -> float:
    """Coerce Billit numeric values to floats for summaries."""

    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def order_filter(
    direction: str,
    start_date: str,
    end_date: str,
    *,
    inclusive_end: bool = False,
    party_id: int | None = None,
) -> str:
    """Build a Billit order direction/date OData filter."""

    end_operator = "le" if inclusive_end else "lt"
    filters = [
        f"OrderDirection eq '{direction}'",
        f"OrderDate ge {odata_date(start_date)}",
        f"OrderDate {end_operator} {odata_date(end_date)}",
    ]
    if party_id is not None:
        filters.insert(1, f"Party/PartyID eq {party_id}")
    return " and ".join(filters)


async def list_orders(client: BillitRequester, odata_filter: str) -> Envelope:
    """Fetch orders through the shared capped list-query path."""

    return await client.request(
        "GET",
        "/orders",
        params=list_params(skip=None, top=MAX_PAGE_SIZE, odata_filter=odata_filter),
    )


def total_incl(items: list[dict[str, Any]]) -> float:
    """Return the sum of Billit TotalIncl values."""

    return sum(money(item.get("TotalIncl")) for item in items)


async def order_summary(
    client: BillitRequester,
    direction: str,
    start_date: str,
    end_date: str,
    *,
    party_id: int | None = None,
    include_count: bool = False,
) -> Envelope:
    """Return a total, and optionally count, for an order filter."""

    response = await list_orders(
        client,
        order_filter(direction, start_date, end_date, inclusive_end=True, party_id=party_id),
    )
    if not response.get("success"):
        return response
    items = normalize_items(response.get("data"))
    data: dict[str, Any] = {"total_incl": total_incl(items)}
    if include_count:
        data["count"] = len(items)
    return success(data)


async def period_order_total(
    client: BillitRequester,
    direction: str,
    period: str,
    *,
    party_id: int | None = None,
) -> Envelope:
    """Return a total for a YYYY or YYYY-MM period."""

    bounds = period_bounds(period)
    if bounds is None:
        return invalid_period(period)
    start_date, end_date = bounds
    response = await list_orders(
        client,
        order_filter(direction, start_date, end_date, party_id=party_id),
    )
    if not response.get("success"):
        return response
    return success({"total_incl": total_incl(normalize_items(response.get("data")))})


async def suggest_payment_reconciliation(client: BillitRequester) -> Envelope:
    """Match outstanding invoices with bank transactions by reference and amount."""

    invoices_resp, tx_resp = await asyncio.gather(
        client.request(
            "GET",
            "/orders",
            params=list_params(skip=None, top=MAX_PAGE_SIZE, odata_filter="ToPay gt 0"),
        ),
        client.request(
            "GET",
            FINANCIAL_TRANSACTIONS_ENDPOINT,
            params=list_params(skip=None, top=MAX_PAGE_SIZE),
        ),
    )
    if not invoices_resp.get("success"):
        return invoices_resp
    if not tx_resp.get("success"):
        return tx_resp

    transactions = normalize_items(tx_resp.get("data"))
    matches: list[dict[str, Any]] = []
    for invoice in normalize_items(invoices_resp.get("data")):
        reference = invoice.get("PaymentReference") or invoice.get("StructuredCommunication")
        amount = money(invoice.get("ToPay"))
        for transaction in transactions:
            tx_reference = transaction.get("PaymentReference") or transaction.get("Communication")
            tx_amount = money(transaction.get("Amount"))
            if (reference and reference == tx_reference) or (
                amount and abs(amount - tx_amount) < 0.01
            ):
                matches.append(
                    {
                        "order_id": invoice.get("OrderID"),
                        "transaction_id": transaction.get("FinancialTransactionID"),
                        "amount": amount,
                    }
                )
                break
    return success(matches)


async def generate_invoice_summary(
    client: BillitRequester,
    start_date: str,
    end_date: str,
) -> Envelope:
    """Return the number and total of sales invoices between two dates."""

    return await order_summary(
        client,
        "Income",
        start_date,
        end_date,
        include_count=True,
    )


async def generate_expense_summary(
    client: BillitRequester,
    start_date: str,
    end_date: str,
) -> Envelope:
    """Return the number and total of purchase invoices between two dates."""

    return await order_summary(
        client,
        "Cost",
        start_date,
        end_date,
        include_count=True,
    )


async def get_cashflow_overview(client: BillitRequester, period: str) -> Envelope:
    """Summarize cash inflow and outflow for the given YYYY or YYYY-MM period."""

    bounds = period_bounds(period)
    if bounds is None:
        return invalid_period(period)
    start_date, end_date = bounds
    income_resp, cost_resp = await asyncio.gather(
        list_orders(client, order_filter("Income", start_date, end_date)),
        list_orders(client, order_filter("Cost", start_date, end_date)),
    )
    if not income_resp.get("success"):
        return income_resp
    if not cost_resp.get("success"):
        return cost_resp
    income_total = total_incl(normalize_items(income_resp.get("data")))
    cost_total = total_incl(normalize_items(cost_resp.get("data")))
    return success({"income": income_total, "cost": cost_total, "net": income_total - cost_total})


async def categorize_expense_invoice(client: BillitRequester, invoice_id: int) -> Envelope:
    """Suggest a simple category for an expense invoice based on keywords."""

    resp = await client.request("GET", f"/orders/{invoice_id}")
    if not resp.get("success"):
        return resp
    order = resp.get("data", {}) or {}
    lines = order.get("OrderLines", []) or []
    text = " ".join(str(line.get("Description", "")) for line in lines).lower()
    if any(keyword in text for keyword in ["fuel", "gas", "petrol", "diesel"]):
        category = "Transport"
    elif any(keyword in text for keyword in ["office", "paper", "stationery"]):
        category = "Office"
    else:
        category = "General"
    return success({"invoice_id": invoice_id, "category": category})


async def list_overdue_invoices(client: BillitRequester) -> Envelope:
    """Return all overdue sales invoices."""

    resp = await list_orders(client, "Overdue eq true and OrderDirection eq 'Income'")
    if not resp.get("success"):
        return resp
    return success([order.get("OrderID") for order in normalize_items(resp.get("data"))])


async def get_supplier_spend_summary(
    client: BillitRequester,
    supplier_id: int,
    period: str,
) -> Envelope:
    """Return total spend with a supplier for the given period."""

    response = await period_order_total(client, "Cost", period, party_id=supplier_id)
    if not response.get("success"):
        return response
    return success({"supplier_id": supplier_id, **response["data"]})


async def get_customer_revenue_summary(
    client: BillitRequester,
    customer_id: int,
    period: str,
) -> Envelope:
    """Return total revenue from a customer for the given period."""

    response = await period_order_total(client, "Income", period, party_id=customer_id)
    if not response.get("success"):
        return response
    return success({"customer_id": customer_id, **response["data"]})


async def find_duplicate_contacts(
    client: BillitRequester,
    similarity_threshold: float = 0.9,
) -> Envelope:
    """Find contacts with similar names using a naive ratio check."""

    resp = await client.request(
        "GET",
        "/parties",
        params=list_params(skip=None, top=MAX_PAGE_SIZE),
    )
    if not resp.get("success"):
        return resp
    duplicates: list[dict[str, Any]] = []
    names = [
        (party.get("PartyID"), party.get("Name", "")) for party in normalize_items(resp.get("data"))
    ]
    for index, (id_a, name_a) in enumerate(names):
        for id_b, name_b in names[index + 1 :]:
            if not name_a or not name_b:
                continue
            ratio = similarity(str(name_a), str(name_b))
            if ratio >= similarity_threshold:
                duplicates.append({"party_a": id_a, "party_b": id_b, "similarity": ratio})
    return success(duplicates)


async def normalize_contact_address(client: BillitRequester, party_id: int) -> Envelope:
    """Normalize address fields of a contact in a simple deterministic way."""

    resp = await client.request("GET", f"/parties/{party_id}")
    if not resp.get("success"):
        return resp
    party = resp.get("data", {}) or {}
    addresses = party.get("Addresses", []) or []
    normalized = [
        {
            key: str(value).title() if isinstance(value, str) else value
            for key, value in address.items()
        }
        for address in addresses
    ]
    patch_resp = await client.request(
        "PATCH",
        f"/parties/{party_id}",
        json={"Addresses": normalized},
    )
    if not patch_resp.get("success"):
        return patch_resp
    return success({"party_id": party_id, "normalized": True})


async def create_invoice_from_text(
    client: BillitRequester,
    data: dict[str, Any],
) -> Envelope:
    """Create a simple sales invoice using provided free text."""

    invoice = {
        "OrderDirection": "Income",
        "OrderType": "Invoice",
        "Customer": {"Name": "Text Import"},
        "OrderLines": [
            {
                "Description": data.get("text_description", ""),
                "Quantity": 1,
                "UnitPriceExcl": 0.0,
            }
        ],
    }
    return await client.request("POST", "/orders", json=invoice)

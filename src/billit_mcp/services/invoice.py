"""Shared invoice workflow helpers for hosted Billit MCP mode."""

from __future__ import annotations

from typing import Any


def build_invoice_preflight(
    *,
    customer: dict[str, Any],
    lines: list[dict[str, Any]],
    order_date: str,
    expiry_date: str,
    desired_transport: str | None = None,
) -> dict[str, Any]:
    """Build the read-only invoice preflight response used by hosted tools."""

    blockers = invoice_blockers(customer, lines, order_date, expiry_date)
    return {
        "ready": not blockers,
        "blockers": blockers,
        "warnings": [],
        "customer_resolution": {
            "mode": "provided_party"
            if customer.get("party_id") or customer.get("PartyID")
            else "needs_resolution"
        },
        "transport": {
            "desired": desired_transport,
            "recommended": desired_transport or "Peppol",
            "fallback": "SMTP",
        },
        "next_action": {"tool": "billit.invoice.create_draft" if not blockers else None},
    }


def invoice_blockers(
    customer: dict[str, Any], lines: list[dict[str, Any]], order_date: str, expiry_date: str
) -> list[str]:
    """Return deterministic invoice-preflight blockers."""

    blockers: list[str] = []
    if not customer.get("party_id") and not customer.get("PartyID") and not customer.get("name"):
        blockers.append("Customer party_id, PartyID, or name is required.")
    if not lines:
        blockers.append("At least one invoice line is required.")
    for index, line in enumerate(lines):
        if not line.get("description"):
            blockers.append(f"Line {index + 1} is missing description.")
        if line.get("quantity") is None:
            blockers.append(f"Line {index + 1} is missing quantity.")
        if line.get("unit_price") is None:
            blockers.append(f"Line {index + 1} is missing unit_price.")
    if not order_date:
        blockers.append("order_date is required.")
    if not expiry_date:
        blockers.append("expiry_date is required.")
    return blockers


def build_invoice_payload(
    *,
    customer: dict[str, Any],
    lines: list[dict[str, Any]],
    order_date: str,
    expiry_date: str,
    external_provider_id: str | None = None,
) -> dict[str, Any]:
    """Build the Billit order payload for a draft sales invoice."""

    billit_customer: dict[str, Any]
    if customer.get("party_id") or customer.get("PartyID"):
        billit_customer = {"PartyID": customer.get("party_id") or customer.get("PartyID")}
    else:
        billit_customer = {
            "Name": customer.get("name") or customer.get("Name"),
            "VATNumber": customer.get("vat_number") or customer.get("VATNumber"),
            "Email": customer.get("email") or customer.get("Email"),
            "PartyType": "Customer",
        }
    payload: dict[str, Any] = {
        "OrderType": "Invoice",
        "OrderDirection": "Income",
        "OrderDate": order_date,
        "ExpiryDate": expiry_date,
        "Customer": billit_customer,
        "OrderLines": [
            {
                "Description": line.get("description"),
                "Quantity": line.get("quantity"),
                "UnitPriceExcl": line.get("unit_price"),
                "VATPercentage": line.get("vat_percentage", 21),
            }
            for line in lines
        ],
    }
    if external_provider_id:
        payload["ExternalProviderID"] = external_provider_id
    return payload


def build_send_summary(
    order: Any,
    *,
    company_party_id: int,
    transport_type: str,
    strict_transport: bool,
) -> dict[str, Any]:
    """Build the canonical confirmation challenge summary for invoice sending."""

    data = order if isinstance(order, dict) else {}
    raw_customer = data.get("Customer")
    customer: dict[str, Any] = raw_customer if isinstance(raw_customer, dict) else {}
    return {
        "company_party_id": company_party_id,
        "order_id": data.get("OrderID") or data.get("ID"),
        "invoice_number": data.get("OrderNumber"),
        "customer_name": customer.get("Name"),
        "customer_vat": customer.get("VATNumber"),
        "amount_including_vat": data.get("TotalIncl") or data.get("TotalInclVAT"),
        "currency": data.get("Currency") or "EUR",
        "is_sent": bool(data.get("IsSent")),
        "order_status": data.get("OrderStatus"),
        "transport_type": transport_type,
        "strict_transport": strict_transport,
        "fallback_allowed": not strict_transport,
    }

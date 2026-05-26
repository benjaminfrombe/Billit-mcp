"""Structured Billit filter compilation for hosted tools."""

from __future__ import annotations

from datetime import date

from billit.endpoints import list_params

ORDER_TYPE_MAP = {
    "invoice": "Invoice",
    "credit_note": "CreditNote",
    "offer": "Offer",
    "delivery_note": "DeliveryNote",
    "order_form": "OrderForm",
}

DIRECTION_MAP = {
    "income": "Income",
    "cost": "Cost",
}

PARTY_ROLE_MAP = {
    "customer": "Customer",
    "supplier": "Supplier",
}


def compile_order_params(
    *,
    direction: str | None = None,
    order_type: str | None = None,
    customer_name: str | None = None,
    vat_number: str | None = None,
    paid: bool | None = None,
    modified_since: str | None = None,
    limit: int = 20,
) -> dict[str, object]:
    """Compile safe hosted order search parameters."""

    filters: list[str] = []
    if direction:
        resolved_direction = DIRECTION_MAP.get(direction.lower())
        if resolved_direction is None:
            raise ValueError(f"Unsupported direction: {direction}")
        filters.append(f"OrderDirection eq '{resolved_direction}'")
    if order_type:
        resolved_type = ORDER_TYPE_MAP.get(order_type.lower())
        if resolved_type is None:
            raise ValueError(f"Unsupported order_type: {order_type}")
        filters.append(f"OrderType eq '{resolved_type}'")
    if customer_name:
        filters.append(f"contains(Customer/Name,'{_odata_string(customer_name)}')")
    if vat_number:
        filters.append(f"Customer/VATNumber eq '{_odata_string(vat_number)}'")
    if paid is not None:
        filters.append(f"Paid eq {str(paid).lower()}")
    if modified_since:
        date.fromisoformat(modified_since)
        filters.append(f"LastModifiedDate ge {modified_since}")
    top = max(1, min(limit, 120))
    return list_params(skip=0, top=top, odata_filter=" and ".join(filters) if filters else None)


def compile_party_params(
    *,
    role: str,
    name: str | None = None,
    vat_number: str | None = None,
    email: str | None = None,
    external_provider_id: str | None = None,
    limit: int = 5,
) -> dict[str, object]:
    """Compile safe hosted party-resolution parameters."""

    resolved_role = PARTY_ROLE_MAP.get(role)
    if resolved_role is None:
        raise ValueError("Unsupported role: expected customer or supplier")
    filters = [f"PartyType eq '{resolved_role}'"]
    if external_provider_id:
        filters.append(f"ExternalProviderID eq '{_odata_string(external_provider_id)}'")
    elif vat_number:
        filters.append(f"VATNumber eq '{_odata_string(vat_number)}'")
    elif email:
        filters.append(f"Email eq '{_odata_string(email)}'")
    elif name:
        filters.append(f"contains(Name,'{_odata_string(name)}')")
    top = max(1, min(limit, 20))
    return list_params(skip=0, top=top, odata_filter=" and ".join(filters))


def _odata_string(value: str) -> str:
    """Escape a user-provided OData string literal."""

    lowered = value.lower()
    if "$" in value or ";" in value or " and " in lowered or " or " in lowered:
        raise ValueError("Unsupported characters in filter value")
    return value.replace("'", "''")

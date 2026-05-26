"""Shared smart-search implementation for Billit orders, parties, and products."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import TYPE_CHECKING, Any

from billit.endpoints import MAX_PAGE_SIZE, list_params

if TYPE_CHECKING:
    from billit.protocols import BillitRequester

ENTITY_TYPES = {"orders", "parties", "products", "all"}
STOP_WORDS = {"the", "and", "for", "with", "from", "in", "on", "at", "to", "of", "a", "an"}
DATE_PATTERNS = (
    r"(\d{4})",
    r"(january|february|march|april|may|june|july|august|september|october|november|december)",
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
    r"(winter|spring|summer|fall|autumn)",
    r"(split)",
)


@dataclass(frozen=True)
class SearchTerms:
    """Parsed search query terms."""

    query: str
    amounts: list[float]
    dates: list[str]
    keywords: list[str]


def parse_search_terms(query: str) -> SearchTerms:
    """Extract reusable scoring terms from a search query."""

    query_lower = query.lower()
    amount_matches = re.findall(r"[€$£]\s*(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)", query)
    amounts = [float(amount.replace(",", "")) for amount in amount_matches]
    dates: list[str] = []
    for pattern in DATE_PATTERNS:
        dates.extend(re.findall(pattern, query_lower))
    keywords = [
        word
        for word in re.findall(r"[a-z0-9]+", query_lower)
        if len(word) > 2 and word not in STOP_WORDS
    ]
    return SearchTerms(query=query, amounts=amounts, dates=dates, keywords=keywords)


def normalize_items(data: Any) -> list[dict[str, Any]]:
    """Return Billit list payloads as a list of dictionaries."""

    items = data.get("Items", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def similarity(left: str, right: str) -> float:
    """Compute a case-insensitive similarity ratio."""

    return SequenceMatcher(None, left.lower(), right.lower()).ratio()


def score_order(order: dict[str, Any], terms: SearchTerms) -> tuple[float, list[str]]:
    """Score an order against search terms."""

    score = 0.0
    matches: list[str] = []
    customer_name = (order.get("CounterParty") or {}).get("DisplayName", "") or ""
    order_number = str(order.get("OrderNumber", "") or "")
    description = str(order.get("Description", "") or "")
    order_lines = normalize_items(order.get("OrderLines", []))
    line_text = " ".join(str(line.get("Description", "") or "") for line in order_lines)
    search_text = f"{customer_name} {order_number} {description} {line_text}".lower()

    for keyword in terms.keywords:
        if keyword in search_text:
            score += 1.0
            matches.append(keyword)

    if customer_name:
        score += similarity(terms.query, customer_name) * 3.0

    total_amount = float(order.get("TotalIncl", 0) or 0)
    for amount in terms.amounts:
        if abs(total_amount - amount) < 0.01:
            score += 4.0
            matches.append(str(amount))
        elif amount and abs(total_amount - amount) < amount * 0.1:
            score += 2.0
            matches.append(str(amount))

    date_text = f"{order_number} {description} {order.get('OrderDate', '')}".lower()
    for date_term in terms.dates:
        if date_term in date_text:
            score += 1.5
            matches.append(date_term)

    return score, matches


def score_party(party: dict[str, Any], terms: SearchTerms) -> tuple[float, list[str]]:
    """Score a party against search terms."""

    name = str(party.get("Name", "") or "")
    display_name = str(party.get("DisplayName", "") or "")
    search_text = f"{name} {display_name}".lower()
    score = 0.0
    matches: list[str] = []
    for keyword in terms.keywords:
        if keyword in search_text:
            score += 1.5
            matches.append(keyword)
    if name or display_name:
        score += max(similarity(terms.query, name), similarity(terms.query, display_name)) * 3.0
    return score, matches


def score_product(product: dict[str, Any], terms: SearchTerms) -> tuple[float, list[str]]:
    """Score a product against search terms."""

    description = str(product.get("Description", "") or "")
    description_lower = description.lower()
    score = similarity(terms.query, description) * 3.0 if description else 0.0
    matches: list[str] = []
    for keyword in terms.keywords:
        if keyword in description_lower:
            score += 1.0
            matches.append(keyword)
    return score, matches


async def run_smart_search(
    client: BillitRequester,
    query: str,
    entity_type: str = "all",
    max_results: int = 10,
) -> dict[str, Any]:
    """Search orders, parties, and products using one shared scoring path."""

    if entity_type not in ENTITY_TYPES:
        return {
            "success": False,
            "data": None,
            "error": f"entity_type must be one of: {', '.join(sorted(ENTITY_TYPES))}",
            "error_code": "INVALID_ENTITY_TYPE",
        }

    terms = parse_search_terms(query)
    results: list[dict[str, Any]] = []

    if entity_type in {"orders", "all"}:
        orders_resp = await client.request(
            "GET", "/orders", params=list_params(skip=None, top=MAX_PAGE_SIZE)
        )
        if not orders_resp.get("success"):
            return orders_resp
        for order in normalize_items(orders_resp.get("data")):
            score, matches = score_order(order, terms)
            if score > 0.1:
                results.append(
                    {"entity_type": "order", "score": score, "matches": matches, "data": order}
                )

    if entity_type in {"parties", "all"}:
        parties_resp = await client.request(
            "GET", "/parties", params=list_params(skip=None, top=MAX_PAGE_SIZE)
        )
        if not parties_resp.get("success"):
            return parties_resp
        for party in normalize_items(parties_resp.get("data")):
            score, matches = score_party(party, terms)
            if score > 0.1:
                results.append(
                    {"entity_type": "party", "score": score, "matches": matches, "data": party}
                )

    if entity_type in {"products", "all"}:
        products_resp = await client.request(
            "GET", "/products", params=list_params(skip=None, top=MAX_PAGE_SIZE)
        )
        if not products_resp.get("success"):
            return products_resp
        for product in normalize_items(products_resp.get("data")):
            score, matches = score_product(product, terms)
            if score > 0.1:
                results.append(
                    {"entity_type": "product", "score": score, "matches": matches, "data": product}
                )

    results.sort(key=lambda result: result["score"], reverse=True)
    results = results[:max_results]
    return {
        "success": True,
        "data": {
            "query": query,
            "total_results": len(results),
            "results": results,
            "parsed_keywords": {
                "amounts": terms.amounts,
                "dates": terms.dates,
                "content": terms.keywords,
            },
        },
        "error": None,
        "error_code": None,
    }

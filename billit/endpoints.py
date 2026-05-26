"""Canonical Billit REST endpoint paths used by adapters and canaries."""

from __future__ import annotations

from typing import Any

FINANCIAL_TRANSACTIONS_ENDPOINT = "/financialTransactions"
MAX_PAGE_SIZE = 120
REPORTS_ENDPOINT = "/reports"


def clamp_page_size(top: int, maximum: int = MAX_PAGE_SIZE) -> int:
    """Clamp a Billit list page size to the supported range."""

    return min(max(0, top), maximum)


def list_params(
    *,
    skip: int | None = 0,
    top: int = MAX_PAGE_SIZE,
    odata_filter: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build canonical OData list parameters with safe pagination limits."""

    params: dict[str, Any] = dict(extra or {})
    if skip is not None:
        params["$skip"] = max(0, skip)
    params["$top"] = clamp_page_size(top)
    if odata_filter:
        params["$filter"] = odata_filter
    return params


def report_endpoint(report_id: str | None = None) -> str:
    """Return the canonical report endpoint path."""

    if report_id:
        return f"{REPORTS_ENDPOINT}/{report_id}"
    return REPORTS_ENDPOINT

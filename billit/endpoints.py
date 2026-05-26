"""Canonical Billit REST endpoint paths used by adapters and canaries."""

from __future__ import annotations

FINANCIAL_TRANSACTIONS_ENDPOINT = "/financialTransactions"
MAX_PAGE_SIZE = 120
REPORTS_ENDPOINT = "/reports"


def report_endpoint(report_id: str | None = None) -> str:
    """Return the canonical report endpoint path."""

    if report_id:
        return f"{REPORTS_ENDPOINT}/{report_id}"
    return REPORTS_ENDPOINT

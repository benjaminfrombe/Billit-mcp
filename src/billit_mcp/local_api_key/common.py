"""Shared local API-key runtime types and result helpers."""

from __future__ import annotations

import secrets
from typing import Any, Protocol

from billit_mcp.services.invoice_workflow import hash_payload, hash_text

ToolResult = dict[str, Any]

LOCAL_API_KEY_TOOL_NAMES = {
    "billit.connection_status",
    "billit.list_companies",
    "billit.search_orders",
    "billit.get_order",
    "billit.resolve_party",
    "billit.lookup_peppol_receiver",
    "billit.list_financial_transactions",
    "billit.list_reports",
    "billit.get_report",
    "billit.invoice.prepare",
    "billit.invoice.create_draft",
    "billit.invoice.prepare_send",
    "billit.invoice.confirm_send",
    "billit.invoice.get_delivery_status",
    "billit.invoice.summary",
}

SECURITY_DENIALS = {
    "configuration_error",
    "local_writes_disabled",
    "local_sends_disabled",
    "company_entitlement_unverified",
    "unauthorized_company",
    "context_party_id_disabled",
    "challenge_not_found",
    "challenge_expired",
    "challenge_mismatch",
    "challenge_token_invalid",
    "challenge_changed",
    "idempotency_conflict",
}


class LocalBillitClient(Protocol):
    """Minimal client protocol used by the local API-key runtime."""

    client: Any

    async def request(self, method: str, url: str, **kwargs: Any) -> ToolResult:
        """Perform a Billit request."""
        ...

    async def close(self) -> None:
        """Close the client."""
        ...


class LocalToolError(RuntimeError):
    """Structured local API-key tool error."""

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        severity: str = "blocking",
        retryable: bool = False,
        user_action_required: bool = True,
        error_code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.retryable = retryable
        self.user_action_required = user_action_required
        self.error_code = error_code or error_type.upper()

    def to_result(self) -> ToolResult:
        """Return the stable Billit MCP envelope."""

        return failure(
            {
                "type": self.error_type,
                "severity": self.severity,
                "retryable": self.retryable,
                "user_action_required": self.user_action_required,
                "message": self.message,
            },
            self.error_code,
        )


def success(data: Any) -> ToolResult:
    """Return a successful local tool result."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def failure(error: Any, error_code: str) -> ToolResult:
    """Return a failed local tool result."""

    return {"success": False, "data": None, "error": error, "error_code": error_code}


def error_result(exc: Exception) -> ToolResult:
    """Convert an exception into the stable MCP envelope."""

    if isinstance(exc, LocalToolError):
        return exc.to_result()
    return failure(
        {
            "type": "local_tool_error",
            "severity": "blocking",
            "retryable": False,
            "user_action_required": True,
            "message": str(exc),
        },
        "LOCAL_TOOL_ERROR",
    )


def item_list(data: Any) -> list[dict[str, Any]]:
    """Return Billit list items from a list response shape."""

    if isinstance(data, dict):
        items = data.get("Items") or data.get("items") or data.get("value")
        return items if isinstance(items, list) else []
    return data if isinstance(data, list) else []


def token() -> str:
    """Return a short URL-safe correlation token."""

    return secrets.token_urlsafe(18)


__all__ = [
    "LOCAL_API_KEY_TOOL_NAMES",
    "SECURITY_DENIALS",
    "LocalBillitClient",
    "LocalToolError",
    "ToolResult",
    "error_result",
    "failure",
    "hash_payload",
    "hash_text",
    "item_list",
    "success",
    "token",
]

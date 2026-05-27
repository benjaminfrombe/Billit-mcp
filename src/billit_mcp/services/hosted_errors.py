"""Hosted tool result and error helpers."""

from __future__ import annotations

from typing import Any

SECURITY_DENIALS = {
    "unauthenticated",
    "insufficient_scope",
    "billit_not_connected",
    "billit_reauthorization_required",
    "unauthorized_company",
}


class HostedToolError(RuntimeError):
    """Structured hosted tool error."""

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
        """Create a structured tool error."""

        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.retryable = retryable
        self.user_action_required = user_action_required
        self.error_code = error_code or error_type.upper()

    def to_result(self) -> dict[str, Any]:
        """Return the stable Billit MCP envelope."""

        return {
            "success": False,
            "data": None,
            "error": {
                "type": self.error_type,
                "severity": self.severity,
                "retryable": self.retryable,
                "user_action_required": self.user_action_required,
                "message": self.message,
            },
            "error_code": self.error_code,
        }


def success(data: Any) -> dict[str, Any]:
    """Return a successful tool result."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def error_result(exc: Exception) -> dict[str, Any]:
    """Convert an exception into the stable MCP envelope."""

    if isinstance(exc, HostedToolError):
        return exc.to_result()
    return {
        "success": False,
        "data": None,
        "error": {
            "type": "hosted_tool_error",
            "severity": "blocking",
            "retryable": False,
            "user_action_required": True,
            "message": str(exc),
        },
        "error_code": "HOSTED_TOOL_ERROR",
    }

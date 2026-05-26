"""Local API-key Billit client lifecycle and audit wrapper."""

from __future__ import annotations

from contextlib import suppress
from time import perf_counter
from typing import Any, Protocol

from billit_mcp.local_api_key.common import LocalBillitClient, ToolResult, token


class AuditRuntime(Protocol):
    """Runtime hooks required by the audited local Billit client."""

    async def audit(
        self,
        *,
        event_type: str,
        operation_class: str,
        outcome: str,
        correlation_id: str,
        tool_name: str | None = None,
        environment: str | None = None,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
        latency_ms: int | None = None,
    ) -> None:
        """Record a redacted local audit event."""
        ...


class LocalAuditedBillitClient:
    """Local Billit API client wrapper that records redacted outbound audit."""

    def __init__(
        self,
        *,
        client: LocalBillitClient,
        runtime: AuditRuntime,
        tool_name: str,
        environment: str,
        company_party_id: int | None,
    ) -> None:
        self._client = client
        self._runtime = runtime
        self._tool_name = tool_name
        self._environment = environment
        self._company_party_id = company_party_id

    async def request(self, method: str, url: str, **kwargs: Any) -> ToolResult:
        """Proxy a Billit request and audit only method/path/outcome metadata."""

        started = perf_counter()
        outcome = "success"
        error_code: str | None = None
        try:
            response = await self._client.request(method, url, **kwargs)
            if not response.get("success", False):
                outcome = "failure"
                error_code = str(response.get("error_code") or "BILLIT_API_ERROR")
            return response
        except Exception:
            outcome = "failure"
            error_code = "BILLIT_API_EXCEPTION"
            raise
        finally:
            with suppress(Exception):
                await self._runtime.audit(
                    event_type="billit_api_call",
                    operation_class="external_api",
                    outcome=outcome,
                    correlation_id=token(),
                    tool_name=self._tool_name,
                    environment=self._environment,
                    company_party_id=self._company_party_id,
                    summary={"method": method.upper(), "path": url},
                    error_code=error_code,
                    latency_ms=int((perf_counter() - started) * 1000),
                )

    async def close(self) -> None:
        """No-op close for compatibility with shared workflow contexts."""

        return None


def client_is_closed(client: LocalBillitClient) -> bool:
    """Return whether the wrapped httpx client is closed."""

    inner = getattr(client, "client", None)
    return bool(getattr(inner, "is_closed", False))

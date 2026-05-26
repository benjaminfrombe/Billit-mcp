"""Curated read-only local API-key MCP tool handlers."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Protocol, cast
from urllib.parse import quote

from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.services.ai_composite import generate_invoice_summary
from billit_mcp.local_api_key.common import LocalToolError, ToolResult, item_list, success
from billit_mcp.local_api_key.settings import (
    base_url_host,
    environment_name,
    missing_local_settings,
)
from billit_mcp.services.filters import compile_order_params, compile_party_params

if TYPE_CHECKING:
    from billit_mcp.local_api_key.companies import CompanyStatus


class LocalReadRuntime(Protocol):
    """Runtime hooks required by local read tools."""

    state: Any

    def settings_party_id(self) -> str:
        """Return configured PartyID without coercion."""
        ...

    def settings_base_url(self) -> str:
        """Return configured Billit base URL."""
        ...

    async def audited_client(self, *, tool_name: str) -> Any:
        """Return an audited Billit client."""
        ...

    async def execute_tool(
        self,
        *,
        tool_name: str,
        operation_class: str,
        handler: Any,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> ToolResult:
        """Execute a local tool with central audit/error handling."""
        ...

    async def company_status(self, *, tool_name: str) -> CompanyStatus:
        """Return accountInformation company status."""
        ...

    def local_warnings(self) -> list[str]:
        """Return local warnings."""
        ...

    def configured_party_id_or_none(self) -> int | None:
        """Return configured numeric PartyID when available."""
        ...

    @property
    def local_writes_enabled(self) -> bool:
        """Whether local writes are enabled."""
        ...

    @property
    def local_sends_enabled(self) -> bool:
        """Whether local sends are enabled."""
        ...


class LocalReadTools:
    """Read and read-like local API-key tool implementations."""

    def __init__(self, runtime: LocalReadRuntime) -> None:
        self.runtime = runtime

    async def connection_status(self) -> ToolResult:
        """Check local API-key configuration, auth, and company entitlement."""

        async def handler() -> ToolResult:
            missing = missing_local_settings()
            if missing:
                return success(
                    {
                        "connected": False,
                        "configuration_complete": False,
                        "missing_settings": missing,
                        "environment": environment_name(os.getenv("BILLIT_BASE_URL", "")),
                        "base_url_host": base_url_host(os.getenv("BILLIT_BASE_URL", "")),
                        "configured_party_id": os.getenv("BILLIT_PARTY_ID"),
                        "company_authorization": "not_checked",
                        "company_count": 0,
                        "writes_enabled": self.runtime.local_writes_enabled,
                        "sends_enabled": self.runtime.local_sends_enabled,
                        "context_party_id_enabled": False,
                        "warnings": [
                            "Missing required local API-key settings: " + ", ".join(missing)
                        ],
                        "state_path": str(self.runtime.state.path),
                    }
                )
            company = await self.runtime.company_status(tool_name="billit.connection_status")
            if not company.account_response.get("success"):
                return company.account_response
            return success(
                {
                    "connected": True,
                    "configuration_complete": True,
                    "environment": environment_name(self.runtime.settings_base_url()),
                    "base_url_host": base_url_host(self.runtime.settings_base_url()),
                    "configured_party_id": company.configured_party_id,
                    "company_authorization": company.state,
                    "company_count": len(company.companies),
                    "writes_enabled": self.runtime.local_writes_enabled,
                    "sends_enabled": self.runtime.local_sends_enabled,
                    "context_party_id_enabled": False,
                    "warnings": self.runtime.local_warnings() + company.warnings,
                    "state_path": str(self.runtime.state.path),
                }
            )

        return await self.runtime.execute_tool(
            tool_name="billit.connection_status",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def list_companies(self) -> ToolResult:
        """List companies from accountInformation without storing raw payloads."""

        async def handler() -> ToolResult:
            company = await self.runtime.company_status(tool_name="billit.list_companies")
            if not company.account_response.get("success"):
                return company.account_response
            return success(
                {
                    "configured_party_id": company.configured_party_id,
                    "company_authorization": company.state,
                    "companies": company.companies,
                    "warnings": self.runtime.local_warnings() + company.warnings,
                }
            )

        return await self.runtime.execute_tool(
            tool_name="billit.list_companies",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def search_orders(
        self,
        *,
        direction: str | None = None,
        order_type: str | None = None,
        customer_name: str | None = None,
        vat_number: str | None = None,
        paid: bool | None = None,
        modified_since: str | None = None,
        limit: int = 20,
    ) -> ToolResult:
        """Search orders using structured allowlisted filters only."""

        async def handler() -> ToolResult:
            params = compile_order_params(
                direction=direction,
                order_type=order_type,
                customer_name=customer_name,
                vat_number=vat_number,
                paid=paid,
                modified_since=modified_since,
                limit=limit,
            )
            client = await self.runtime.audited_client(tool_name="billit.search_orders")
            return cast("ToolResult", await client.request("GET", "/orders", params=params))

        return await self.runtime.execute_tool(
            tool_name="billit.search_orders",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def get_order(self, *, order_id: int) -> ToolResult:
        """Get one Billit order by ID."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(tool_name="billit.get_order")
            return cast("ToolResult", await client.request("GET", f"/orders/{order_id}"))

        return await self.runtime.execute_tool(
            tool_name="billit.get_order",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def resolve_party(
        self,
        *,
        role: str,
        name: str | None = None,
        vat_number: str | None = None,
        email: str | None = None,
        external_provider_id: str | None = None,
    ) -> ToolResult:
        """Resolve a customer or supplier without guessing on ambiguity."""

        async def handler() -> ToolResult:
            params = compile_party_params(
                role=role.lower(),
                name=name,
                vat_number=vat_number,
                email=email,
                external_provider_id=external_provider_id,
            )
            client = await self.runtime.audited_client(tool_name="billit.resolve_party")
            response = cast(
                "ToolResult",
                await client.request("GET", "/parties", params=params),
            )
            if not response.get("success"):
                return response
            items = item_list(response.get("data"))
            if len(items) == 1:
                return success(
                    {
                        "resolution": "single_match",
                        "party": items[0],
                        "confidence": 1.0,
                        "safe_to_use": True,
                    }
                )
            if len(items) > 1:
                return success(
                    {
                        "resolution": "ambiguous",
                        "candidates": items,
                        "confidence": 0.0,
                        "safe_to_use": False,
                    }
                )
            return success(
                {
                    "resolution": "no_match",
                    "party": None,
                    "confidence": 0.0,
                    "safe_to_use": False,
                }
            )

        return await self.runtime.execute_tool(
            tool_name="billit.resolve_party",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def lookup_peppol_receiver(self, *, identifier: str) -> ToolResult:
        """Check whether a receiver identifier is visible on Peppol."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(tool_name="billit.lookup_peppol_receiver")
            return cast(
                "ToolResult",
                await client.request(
                    "GET",
                    f"/peppol/participantInformation/{quote(identifier, safe='')}",
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.lookup_peppol_receiver",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def list_financial_transactions(self, *, limit: int = 20) -> ToolResult:
        """List financial transactions without raw OData passthrough."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(
                tool_name="billit.list_financial_transactions"
            )
            return cast(
                "ToolResult",
                await client.request(
                    "GET",
                    FINANCIAL_TRANSACTIONS_ENDPOINT,
                    params=list_params(skip=0, top=limit),
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.list_financial_transactions",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def list_reports(self) -> ToolResult:
        """List available reports."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(tool_name="billit.list_reports")
            return cast("ToolResult", await client.request("GET", report_endpoint()))

        return await self.runtime.execute_tool(
            tool_name="billit.list_reports",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )

    async def get_report(
        self,
        *,
        report_id: str,
        parameters: dict[str, str | int | float | bool] | None = None,
    ) -> ToolResult:
        """Get a report with bounded scalar parameters."""

        async def handler() -> ToolResult:
            validate_report_request(report_id, parameters or {})
            client = await self.runtime.audited_client(tool_name="billit.get_report")
            return cast(
                "ToolResult",
                await client.request(
                    "GET",
                    report_endpoint(report_id),
                    params=parameters or {},
                ),
            )

        return await self.runtime.execute_tool(
            tool_name="billit.get_report",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
            resource_type="report",
            resource_id=report_id,
        )

    async def invoice_get_delivery_status(self, *, order_id: int) -> ToolResult:
        """Return a concise fresh-read delivery status."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(
                tool_name="billit.invoice.get_delivery_status"
            )
            order = cast("ToolResult", await client.request("GET", f"/orders/{order_id}"))
            if not order.get("success"):
                return order
            data = order.get("data") or {}
            return success(
                {
                    "order_id": order_id,
                    "is_sent": bool(data.get("IsSent")),
                    "paid": bool(data.get("Paid")),
                    "delivery_status": data.get("DeliveryStatus")
                    or data.get("OrderStatus")
                    or "unknown",
                    "messages": data.get("Messages") or [],
                    "source": "fresh_billit_read",
                }
            )

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.get_delivery_status",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def invoice_summary(self, *, start_date: str, end_date: str) -> ToolResult:
        """Summarize sales invoices through the shared read-only helper."""

        async def handler() -> ToolResult:
            client = await self.runtime.audited_client(tool_name="billit.invoice.summary")
            return await generate_invoice_summary(client, start_date, end_date)

        return await self.runtime.execute_tool(
            tool_name="billit.invoice.summary",
            operation_class="read",
            handler=handler,
            company_party_id=self.runtime.configured_party_id_or_none(),
        )


def validate_report_request(
    report_id: str,
    parameters: dict[str, str | int | float | bool],
) -> None:
    """Reject arbitrary OData-style report parameters."""

    if not report_id or "/" in report_id or "\\" in report_id or "$" in report_id:
        raise LocalToolError("invalid_report_id", "report_id must be a simple Billit report id")
    for key, value in parameters.items():
        if key.startswith("$") or "filter" in key.lower():
            raise LocalToolError(
                "unsupported_report_parameter", "Raw OData parameters are rejected"
            )
        if not isinstance(value, str | int | float | bool):
            raise LocalToolError(
                "unsupported_report_parameter",
                "Report parameters must be scalar values",
            )

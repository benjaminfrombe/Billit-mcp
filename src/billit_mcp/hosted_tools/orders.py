"""Hosted OAuth order MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit_mcp.services.filters import compile_order_params

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from billit_mcp.services.hosted_runtime import HostedToolRuntime


def register_order_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register hosted order tools."""

    @mcp.tool(name="billit.search_orders")
    async def search_orders(
        environment: str,
        company_party_id: int,
        direction: str | None = None,
        order_type: str | None = None,
        customer_name: str | None = None,
        vat_number: str | None = None,
        paid: bool | None = None,
        modified_since: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search orders using structured allowlisted filters."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            params = compile_order_params(
                direction=direction,
                order_type=order_type,
                customer_name=customer_name,
                vat_number=vat_number,
                paid=paid,
                modified_since=modified_since,
                limit=limit,
            )
            async with runtime.authorized_billit_client(
                claims=typed,
                environment=environment,
                company_party_id=company_party_id,
                tool_name="billit.search_orders",
            ) as (_, client):
                return await client.request("GET", "/orders", params=params)

        return await runtime.execute_tool(
            tool_name="billit.search_orders",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.get_order")
    async def get_order(environment: str, company_party_id: int, order_id: int) -> dict[str, Any]:
        """Get one Billit order by ID."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            async with runtime.authorized_billit_client(
                claims=typed,
                environment=environment,
                company_party_id=company_party_id,
                tool_name="billit.get_order",
            ) as (_, client):
                return await client.request("GET", f"/orders/{order_id}")

        return await runtime.execute_tool(
            tool_name="billit.get_order",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

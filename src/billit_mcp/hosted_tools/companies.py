"""Hosted OAuth company and connection MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit_mcp.services.hosted_runtime import HostedToolRuntime, success

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_company_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register hosted connection and company tools."""

    @mcp.tool(name="billit.connection_status")
    async def connection_status(environment: str = "sandbox") -> dict[str, Any]:
        """Return the current hosted Billit connection status."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            connection = await runtime.resolve_connection(
                actor_id=typed.actor_id,
                environment=environment,
            )
            return success(
                {
                    "connected": True,
                    "environment": environment,
                    "token_status": connection.status,
                    "connection_id": connection.connection_id,
                }
            )

        return await runtime.execute_tool(
            tool_name="billit.connection_status",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
        )

    @mcp.tool(name="billit.list_companies")
    async def list_companies(environment: str = "sandbox") -> dict[str, Any]:
        """List companies authorized for the current Billit connection."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            connection = await runtime.resolve_connection(
                actor_id=typed.actor_id,
                environment=environment,
            )
            return success(
                {
                    "companies": await runtime.list_authorized_companies(
                        connection_id=connection.connection_id,
                        environment=environment,
                    )
                }
            )

        return await runtime.execute_tool(
            tool_name="billit.list_companies",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
        )

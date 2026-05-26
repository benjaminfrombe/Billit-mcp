"""Registration for curated hosted Billit MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from billit_mcp.hosted_tools.companies import register_company_tools
from billit_mcp.hosted_tools.invoice import register_invoice_tools
from billit_mcp.hosted_tools.orders import register_order_tools
from billit_mcp.hosted_tools.parties import register_party_tools

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from billit_mcp.services.hosted_runtime import HostedToolRuntime


def register_hosted_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register only the public hosted MVP tool surface."""

    register_company_tools(mcp, runtime)
    register_order_tools(mcp, runtime)
    register_party_tools(mcp, runtime)
    register_invoice_tools(mcp, runtime)

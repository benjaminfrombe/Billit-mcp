"""MCP app factories for local and hosted runtimes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

from billit_mcp.hosted_tools.registration import register_hosted_tools

if TYPE_CHECKING:
    from billit_mcp.auth.oauth_service import MCPJWTVerifier
    from billit_mcp.services.hosted_runtime import HostedToolRuntime


def create_hosted_mcp(runtime: HostedToolRuntime, verifier: MCPJWTVerifier) -> FastMCP:
    """Create the hosted Streamable HTTP MCP server with curated tools only."""

    mcp = FastMCP(
        "billit-mcp-hosted",
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        token_verifier=verifier,
        auth=AuthSettings(
            issuer_url=runtime.settings.issuer_url,
            resource_server_url=runtime.settings.resource_url,
        ),
    )
    register_hosted_tools(mcp, runtime)
    return mcp

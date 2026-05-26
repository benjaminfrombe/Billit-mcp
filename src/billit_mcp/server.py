"""Curated local/private API-key MCP stdio server for Billit."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

from billit_mcp.local_api_key.registration import register_local_api_key_tools
from billit_mcp.local_api_key.runtime import LocalAPIKeyRuntime

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_runtime = LocalAPIKeyRuntime()


@asynccontextmanager
async def mcp_lifespan(server: FastMCP) -> AsyncIterator[dict[str, object]]:
    """Close the shared local Billit client when stdio handling shuts down."""

    try:
        yield {}
    finally:
        await close_mcp_client()


mcp = FastMCP(
    "billit-mcp",
    dependencies=["httpx", "pydantic", "python-dotenv"],
    lifespan=mcp_lifespan,
)
register_local_api_key_tools(mcp, _runtime)


def get_runtime() -> LocalAPIKeyRuntime:
    """Return the process-scoped local API-key runtime."""

    return _runtime


async def get_client() -> object:
    """Return the process-scoped local Billit API client."""

    return await _runtime.get_client()


async def close_mcp_client() -> None:
    """Close and clear the process-scoped local Billit API client."""

    await _runtime.close()

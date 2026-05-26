"""Billit MCP Server - Model Context Protocol server for Billit API integration."""

from .server import mcp
from .stdio import run_stdio


def main() -> None:
    """Main entry point for the billit-mcp script."""
    run_stdio()


__all__ = ["main", "mcp"]

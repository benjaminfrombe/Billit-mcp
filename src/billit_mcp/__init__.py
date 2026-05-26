"""Billit MCP Server - Model Context Protocol server for Billit API integration."""

from .server import mcp


def main() -> None:
    """Main entry point for the billit-mcp script."""
    mcp.run()


__all__ = ["main", "mcp"]

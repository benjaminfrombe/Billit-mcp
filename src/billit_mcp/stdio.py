"""Local stdio runtime for the packaged Billit MCP server."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

from .server import mcp


def get_log_level() -> int:
    """Return a configured Python logging level with a safe fallback."""

    log_level_str = os.getenv("LOG_LEVEL", "INFO")
    if log_level_str.startswith("${") and log_level_str.endswith("}"):
        if ":-" in log_level_str:
            log_level_str = log_level_str.split(":-", 1)[1].rstrip("}")
        else:
            log_level_str = "INFO"
    try:
        return int(getattr(logging, log_level_str.upper()))
    except AttributeError:
        return logging.INFO


def configure_logging() -> None:
    """Configure runtime logging for local stdio execution."""

    logging.basicConfig(
        level=get_log_level(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def run_stdio() -> None:
    """Run the local/private stdio MCP server."""

    load_dotenv()
    configure_logging()
    mcp.run("stdio")

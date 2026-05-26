---
title: "Billit MCP - Auto Update Configuration for MCP Clients"
updated: 2026-05-26
---

# Billit MCP Auto Update Configuration

This document explains how to run Billit MCP from the latest published package
without manually upgrading a local virtual environment. Use this for MCP
clients such as Claude Desktop, Claude Code, Cursor, or any client that accepts
a command plus arguments.

## Billit MCP Auto Update with pipx

`pipx run --no-cache --spec billit-mcp python -m billit_mcp` creates an
isolated environment and fetches the package again for each run. This is the
most predictable option when you want the latest PyPI release and do not want a
long-lived package install.

```json
{
  "mcpServers": {
    "billit": {
      "command": "pipx",
      "args": [
        "run",
        "--no-cache",
        "--spec",
        "billit-mcp",
        "python",
        "-m",
        "billit_mcp"
      ],
      "env": {
        "BILLIT_API_KEY": "your-billit-api-key",
        "BILLIT_BASE_URL": "https://api.billit.be/v1",
        "BILLIT_PARTY_ID": "your-company-party-id"
      }
    }
  }
}
```

## Billit MCP Auto Update with uvx

`uvx` is faster than `pipx` in many environments. Use this when your machine
already has `uv` installed and your MCP client can execute shell commands.

```bash
uvx --no-cache billit-mcp
```

Equivalent MCP client command:

```json
{
  "mcpServers": {
    "billit": {
      "command": "uvx",
      "args": ["--no-cache", "billit-mcp"],
      "env": {
        "BILLIT_API_KEY": "your-billit-api-key",
        "BILLIT_BASE_URL": "https://api.billit.be/v1",
        "BILLIT_PARTY_ID": "your-company-party-id"
      }
    }
  }
}
```

## Billit MCP Auto Update Verification

After changing an MCP client config, restart the client process. MCP clients
usually read server configuration only on startup.

Verify the package can start:

```bash
BILLIT_API_KEY=dummy \
BILLIT_BASE_URL=https://api.billit.be/v1 \
BILLIT_PARTY_ID=dummy \
pipx run --no-cache --spec billit-mcp python -m billit_mcp
```

That command starts an MCP stdio process and waits for client protocol input.
Use `Ctrl-C` to stop it during manual checks.

## Billit MCP Auto Update Troubleshooting

If your MCP client still runs an old package, remove any cached or installed
copy before restarting the client:

```bash
pipx uninstall billit-mcp 2>/dev/null || true
rm -rf ~/.local/pipx/.cache
```

If startup fails before any tool call, check that all required environment
variables are present in the MCP client configuration. The server needs
`BILLIT_API_KEY`, `BILLIT_BASE_URL`, and `BILLIT_PARTY_ID` to create a Billit
client.

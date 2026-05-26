---
title: "Billit MCP - Development and Testing Guide"
updated: 2026-05-26
---

# Billit MCP Development and Testing Guide

This guide explains how to work on the repository safely and how to validate
changes before release.

## Billit MCP Development Setup

Install dependencies with Poetry:

```bash
poetry install
```

Run the MCP server:

```bash
poetry run python -m billit_mcp
```

Run the legacy FastAPI adapter:

```bash
poetry run uvicorn server:app --reload
```

## Billit MCP Source Layout for Contributors

`src/billit_mcp/server.py` is the packaged MCP tool registration file. Add MCP
tools here only when they should be available to AI clients.

`billit/tools/` contains FastAPI route modules. Add routes here when local HTTP
testing or the legacy adapter needs coverage, but remember that this does not
automatically add an MCP tool.

`billit/client.py` contains the shared REST client. Changes here affect both
MCP tools and the FastAPI adapter.

`billit/smart_search.py` contains reusable local search scoring. Keep this
logic independent from FastAPI so MCP and HTTP routes can share it.

## Billit MCP Quality Gates

Run:

```bash
poetry run ruff check .
poetry run pytest -q
```

Ruff is configured in `pyproject.toml` with `E` and `F` rules and a 100
character line length. Do not introduce broad lint exclusions without a clear
reason.

## Billit MCP Test Types

Unit and route tests are the default. They monkeypatch `BillitAPIClient.request`
or use `respx` so they do not need credentials.

Live tests are skipped unless `--live` is passed. They require real Billit
credentials and should normally use sandbox.

```bash
poetry run pytest tests/test_live_integration.py -q --live
```

## Billit MCP Documentation Updates

When behavior changes, update the nearest doc:

- MCP tool changes: [MCP Tool Reference](mcp-tools.md)
- FastAPI route changes: [FastAPI Adapter Routes](fastapi-adapter.md)
- Environment changes: [Configuration Reference](configuration.md)
- Deployment or release changes: [Operations Runbook](operations.md)
- Upstream Billit reference mapping: [Billit API Source Reference](billit-api-reference.md)

Every maintained Markdown file should have:

```yaml
---
title: "Billit MCP - Specific Topic"
updated: YYYY-MM-DD
---
```

Use descriptive H2/H3 headings. Avoid generic headings such as `Overview`,
`Setup`, `Usage`, and `Notes` because they weaken QMD retrieval.

## Billit MCP Pull Request Expectations

Keep changes scoped to one behavior or documentation area. Include tests for
behavior changes and include docs when a user-facing command, route, tool, or
configuration variable changes.

Before opening a pull request, verify that no local credentials or customer
data are staged:

```bash
git diff --cached --name-only
git diff --cached --check
```

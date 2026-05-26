---
title: "Billit MCP - Development and Testing Guide"
updated: 2026-05-26
---

# Billit MCP Development and Testing Guide

This guide explains how to work on the repository safely and how to validate
changes before release.

## Billit MCP Development Setup

Install dependencies with uv:

```bash
uv sync --locked
```

Run the MCP server:

```bash
uv run python -m billit_mcp
```

Run the hosted Streamable HTTP MCP server:

```bash
uv run uvicorn billit_mcp.http_app:create_app --factory --host 127.0.0.1 --port 8000
```

Run the legacy FastAPI adapter:

```bash
uv run uvicorn server:app --reload
```

## Billit MCP Source Layout for Contributors

`src/billit_mcp/server.py` is the packaged MCP tool registration file. Add MCP
tools here only when they should be available to AI clients.

`src/billit_mcp/http_app.py`, `src/billit_mcp/registry.py`, and
`src/billit_mcp/hosted_tools/` are the hosted OAuth runtime. Hosted tools are
curated separately and must not import `billit/tools/` or local API-key
settings.

`billit/tools/` contains FastAPI route modules. Add routes here when local HTTP
testing or the legacy adapter needs coverage, but remember that this does not
automatically add an MCP tool.

`billit/client.py` contains the shared REST client. Changes here affect both
MCP tools and the FastAPI adapter.

`billit/services/` contains adapter-neutral composite helpers shared by MCP
tools, canaries, and FastAPI routes.

`billit/smart_search.py` contains reusable local search scoring. Keep this
logic independent from FastAPI so MCP and HTTP routes can share it.

## Billit MCP Quality Gates

Run:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy billit src tests
uv run lint-imports
uv run pytest -q
uv run diff-cover coverage.xml --compare-branch=origin/master --diff-range-notation=... --fail-under=80
uv build
```

Ruff, mypy, import-linter, pytest, coverage, and diff-cover are configured in
`pyproject.toml`. Do not introduce broad exclusions without a clear reason.

## Billit MCP Test Types

Unit and route tests are the default. Normal pytest sets fake Billit env vars
and fails any unmocked `BillitAPIClient.request` call. Tests must monkeypatch
the client request method, use `respx`, or be marked live.

Live tests are skipped unless `--live` is passed. The live pytest path now wraps
the same read-only sandbox canary used for local endpoint drift evidence.

```bash
uv run pytest tests/test_live_integration.py -q --live
```

The local live-data canary is separate from CI. It defaults to sandbox, reads
the sandbox key from env or macOS Keychain, performs read-only probes, and
writes sanitized evidence under `.local/`:

```bash
BILLIT_SANDBOX_API_KEY_K4K="$(security find-generic-password -w -s BILLIT_SANDBOX_API_KEY_K4K)" \
BILLIT_PARTY_ID="$BILLIT_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only
```

Hosted OAuth read-only canary mode uses the local hosted database and requires
a pre-seeded sandbox Billit OAuth grant. It forces the hosted refresh-token path
and still performs only Billit reads:

```bash
BILLIT_SANDBOX_PARTY_ID="$BILLIT_SANDBOX_PARTY_ID" \
BILLIT_MCP_DATABASE_URL="sqlite+aiosqlite:///.local/billit-mcp-hosted.db" \
uv run python scripts/local/live_billit_canary.py --read-only --mode hosted-oauth-readonly
```

For sandbox runs, credential precedence is
`BILLIT_SANDBOX_API_KEY_K4K`, `BILLIT_SANDBOX_API_KEY`, macOS Keychain service
`BILLIT_SANDBOX_API_KEY_K4K`, then `BILLIT_API_KEY` as a compatibility fallback.
Hosted canary mode does not automate Billit login and does not persist tokens,
API keys, raw customer payloads, raw invoice payloads, file contents, or webhook
bodies into the evidence report.

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

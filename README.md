---
title: "Billit MCP - Project Overview and Quickstart"
updated: 2026-05-26
---

# Billit MCP

Billit MCP is a Python 3.12 Model Context Protocol server for the Billit REST
API. The packaged stdio runtime is a curated local/private API-key connector
for developers and power users. It exposes a narrow set of read tools plus the
confirmation-gated sales-invoice draft/send workflow through a standard
response envelope.

The packaged runtime is the MCP stdio server in `src/billit_mcp/server.py`.
The hosted OAuth runtime is the Streamable HTTP ASGI app in
`src/billit_mcp/http_app.py`. The FastAPI app in `server.py` is a legacy local
adapter used for HTTP smoke tests and route-level development; its raw route
names are not registered as MCP tools.

## Billit MCP Runtime Quickstart

Install from PyPI and run the MCP server:

```bash
pip install billit-mcp
python -m billit_mcp
```

For local development:

```bash
git clone https://github.com/olivier-motium/Billit-mcp.git
cd Billit-mcp
uv sync --locked
uv run python -m billit_mcp
```

The server reads credentials from environment variables. A `.env` file is
loaded automatically for local runs and is ignored by git.

```env
BILLIT_API_KEY=your-billit-api-key
BILLIT_BASE_URL=https://api.billit.be/v1
BILLIT_PARTY_ID=your-company-party-id
RATE_LIMIT_PER_MINUTE=50
BILLIT_MCP_LOCAL_ALLOW_WRITES=0
BILLIT_MCP_LOCAL_ALLOW_SENDS=0
LOG_LEVEL=INFO
```

Use the sandbox by setting `BILLIT_BASE_URL=https://api.sandbox.billit.be/v1`
and using sandbox credentials. Do not mix sandbox and production API keys.
`BILLIT_CONTEXT_PARTY_ID` is ignored in the local MCP runtime; accountant
context is disabled for this MVP.

## Billit MCP Hosted OAuth Runtime

Hosted mode is separate from local API-key stdio mode:

```bash
BILLIT_MCP_DATABASE_URL="sqlite+aiosqlite:///.local/billit-mcp-hosted.db" \
uv run python -m billit_mcp.persistence.migrations

uv run uvicorn billit_mcp.http_app:create_app --factory --host 127.0.0.1 --port 8000
```

It exposes Streamable HTTP MCP at `/mcp`, MCP OAuth metadata and token
endpoints, and Billit OAuth connect/callback endpoints. Hosted mode uses
Billit OAuth grants, encrypted token storage, synced company authorization,
structured filters, and server-owned confirmation challenges for invoice
sending. It does not register raw legacy FastAPI tools and does not read
`BILLIT_API_KEY` or process-scoped `BILLIT_PARTY_ID`.

Hosted startup never runs ORM schema creation. `/readyz` is healthy only after
the configured database is reachable and Alembic is at the hosted head.

## Billit MCP Client Configuration

Most MCP clients can run the package directly:

```json
{
  "mcpServers": {
    "billit": {
      "command": "python",
      "args": ["-m", "billit_mcp"],
      "env": {
        "BILLIT_API_KEY": "your-billit-api-key",
        "BILLIT_BASE_URL": "https://api.billit.be/v1",
        "BILLIT_PARTY_ID": "your-company-party-id"
      }
    }
  }
}
```

For always-latest runs without a persistent install, see
[Auto Update for MCP Clients](AUTO-UPDATE.md).

## Billit MCP Tool Coverage

The packaged API-key stdio server exposes exactly these MCP tools:

`billit.connection_status`, `billit.list_companies`,
`billit.search_orders`, `billit.get_order`, `billit.resolve_party`,
`billit.lookup_peppol_receiver`, `billit.list_financial_transactions`,
`billit.list_reports`, `billit.get_report`, `billit.invoice.prepare`,
`billit.invoice.create_draft`, `billit.invoice.prepare_send`,
`billit.invoice.confirm_send`, `billit.invoice.get_delivery_status`, and
`billit.invoice.summary`.

Raw legacy MCP names such as `create_order`, `send_order`, `delete_order`,
`upload_document`, `download_file`, webhook mutation tools, SSO token tools,
and arbitrary OData passthrough are no longer registered by `python -m
billit_mcp`. The legacy FastAPI adapter still exposes a broader HTTP route
surface for local development. See [FastAPI Adapter Routes](docs/fastapi-adapter.md).

## Billit MCP Response Envelope

All Billit API calls are normalized into this shape:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "error_code": null
}
```

Failed HTTP responses preserve Billit error payloads where possible. Network
failures return `success: false` with `error_code: "REQUEST_ERROR"`.

## Billit MCP Documentation Map

[Documentation Index](docs/index.md) is the main navigation hub. It links to
architecture, configuration, operations, API surface, development workflow,
and the Billit upstream reference folder with short summaries for each reader.

[Architecture and Data Flow](docs/architecture.md) explains the MCP runtime,
legacy FastAPI adapter, shared client, rate limiter, smart search helpers, and
known differences between the two server surfaces.

[Configuration Reference](docs/configuration.md) describes every environment
variable, production versus sandbox selection, local `.env` behavior, macOS
Keychain usage, and secret handling rules.

[MCP Tool Reference](docs/mcp-tools.md) lists the registered MCP tools by
domain, including parameters, Billit endpoint forwarding, and current gotchas.

[Operations Runbook](docs/operations.md) covers local runs, Docker, PyPI
packaging, safe public release checks, troubleshooting, and credential
rotation.

[Development and Testing](docs/development-testing.md) describes repo layout,
quality gates, live-test safety, Ruff/Pytest commands, and contribution
expectations.

[Billit API Source Reference](docs/billit-api-reference.md) explains how to
use the QMD-ready upstream Markdown reference files under
`billit_docs_markdown/` without confusing them with project implementation
docs.

## Billit MCP Development Commands

```bash
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
uv run python -m billit_mcp
uv run uvicorn server:app --reload
```

Run the read-only live canary test only with safe sandbox credentials:

```bash
uv run pytest tests/test_live_integration.py -q --live
```

Run the local read-only live canary against sandbox when validating endpoint
drift or shared composite helpers:

```bash
BILLIT_SANDBOX_API_KEY_K4K="$(security find-generic-password -w -s BILLIT_SANDBOX_API_KEY_K4K)" \
BILLIT_PARTY_ID="$BILLIT_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only --mode api-key-readonly
```

Run the hosted OAuth read-only canary only after seeding a sandbox Billit OAuth
grant in the local hosted database:

```bash
BILLIT_SANDBOX_PARTY_ID="$BILLIT_SANDBOX_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only --mode hosted-oauth-readonly
```

Seed that local grant from an existing sandbox OAuth token pair:

```bash
BILLIT_MCP_CANARY_BILLIT_ACCESS_TOKEN="..." \
BILLIT_MCP_CANARY_BILLIT_REFRESH_TOKEN="..." \
uv run python scripts/local/seed_hosted_oauth_grant.py
```

## Billit MCP Repository Layout

```text
src/billit_mcp/          Packaged MCP stdio server and hosted OAuth runtime.
src/billit_mcp/auth/     MCP OAuth and Billit OAuth bridge services.
src/billit_mcp/hosted_tools/ Curated hosted OAuth-safe MCP tools.
src/billit_mcp/local_api_key/ Curated local API-key stdio runtime services.
src/billit_mcp/persistence/  Hosted SQLAlchemy models and database helpers.
src/billit_mcp/services/ Shared MCP runtime workflow helpers.
billit/client.py         Shared async Billit REST client and response envelope.
billit/dependencies.py   FastAPI dependency factory and request-scoped cleanup.
billit/services/         Shared adapter-neutral business helpers.
billit/smart_search.py   Shared local scoring for orders, parties, and products.
billit/tools/            Legacy FastAPI route modules.
billit/models/           Pydantic request/response models used by route modules.
billit_docs_markdown/    QMD-ready upstream Billit API reference snapshots.
docs/                    Current project documentation.
scripts/local/           Local-only canaries and verification helpers.
tests/                   Unit, route, integration, and live-test suites.
```

## Billit MCP Security Rules

Never commit `.env`, `.pypirc`, API keys, package tokens, customer exports, or
live Billit payloads. The repository was prepared for public use with a
single-root public history; keep future commits equally clean.

Use sandbox credentials for testing unless you are intentionally performing a
production operation. Rotate credentials immediately if they were ever copied
into tracked files, logs, issue text, or public chat.

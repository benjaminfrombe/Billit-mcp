---
title: "Billit MCP - Architecture and Data Flow"
updated: 2026-05-26
---

# Billit MCP Architecture and Data Flow

Billit MCP has three server surfaces. The packaged runtime remains an MCP
stdio server for local/private API-key usage. A hosted Streamable HTTP runtime
is being added for public OAuth usage. The legacy FastAPI adapter is retained
for local HTTP development and route tests.

## Billit MCP Packaged Runtime

`src/billit_mcp/server.py` creates a `FastMCP("billit-mcp")` instance and
registers tool functions with `@mcp.tool()`. Running `python -m billit_mcp`
loads `.env`, configures logging, imports the MCP server, and starts stdio
protocol handling.

MCP tools use a process-scoped `BillitAPIClient` with environment-derived
headers. The server lifespan closes that client when stdio handling shuts down.
The current MCP surface registers 44 tools across parties, products, orders,
financial transactions, account, documents, webhooks, Peppol, reports, utility
lookups, and composite helpers.

## Billit MCP Legacy FastAPI Adapter

`server.py` creates a FastAPI application and includes routers from
`billit/tools/`. These routers expose HTTP routes such as `GET /orders`,
`POST /orders/send`, and `GET /ai/smart-search`.

The FastAPI adapter is useful for route tests, local Swagger inspection, and
experiments with form uploads. It is not what PyPI users get when they run the
MCP package. Keep docs explicit about this split so users do not expect an HTTP
server from `python -m billit_mcp`.

## Billit MCP Hosted OAuth Runtime

`src/billit_mcp/http_app.py` creates the hosted ASGI app. It exposes:

- `POST /mcp` and `GET /mcp` for Streamable HTTP MCP.
- `/.well-known/oauth-protected-resource`
- `/.well-known/oauth-authorization-server`
- `/oauth/authorize`, `/oauth/token`, `/oauth/revoke`, `/oauth/jwks.json`
- `/billit/connect` and `/billit/callback`
- `/healthz`, `/readyz`, `/privacy`, and `/docs`

Hosted mode uses `src/billit_mcp/registry.py` and
`src/billit_mcp/hosted_tools/` instead of importing the legacy raw tool
surface. The hosted registry intentionally exposes only the MVP tools:

- `billit.connection_status`
- `billit.list_companies`
- `billit.search_orders`
- `billit.get_order`
- `billit.resolve_party`
- `billit.lookup_peppol_receiver`
- `billit.invoice.prepare`
- `billit.invoice.create_draft`
- `billit.invoice.prepare_send`
- `billit.invoice.confirm_send`
- `billit.invoice.get_delivery_status`

Hosted mode does not call `BillitSettings.from_env()` and does not read
`BILLIT_API_KEY` or `BILLIT_PARTY_ID`. Billit access is always through a stored
Billit OAuth grant and an explicit, validated `company_party_id`.

## Billit MCP Hosted Auth and Persistence

Hosted auth has two separate layers:

1. MCP-client-to-Billit-MCP OAuth. This is implemented by
   `src/billit_mcp/auth/oauth_service.py` with static clients, PKCE S256
   authorization-code flow, JWT access tokens, revocation, and scope checks.
2. Billit-MCP-to-Billit OAuth. This is implemented by
   `src/billit_mcp/auth/billit_oauth.py`, which exchanges Billit codes, stores
   encrypted grants, refreshes one-time refresh tokens under a row lock, and
   marks connections `reauthorization_required` when refresh fails.

Hosted state lives in Postgres through SQLAlchemy and Alembic:

- OAuth clients, codes, and token revocations.
- Actors and Billit OAuth connections.
- Encrypted Billit token grants.
- Synced Billit companies used to authorize every hosted `company_party_id`.
- Confirmation challenges for invoice sending.
- Local idempotency records and redacted audit events.

Runtime secrets are supplied through environment variables. In AWS, App Runner
maps those variables from Secrets Manager so secret values are not stored in
Terraform.

## Billit MCP Shared Client and Response Envelope

`billit/client.py` owns authentication, rate limiting, timeout behavior, and
response normalization. It loads:

- `BILLIT_API_KEY`
- `BILLIT_BASE_URL`
- `BILLIT_PARTY_ID`
- optional `BILLIT_CONTEXT_PARTY_ID`
- optional `RATE_LIMIT_PER_MINUTE`

Every Billit response is returned as:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "error_code": null
}
```

HTTP 2xx responses become `success: true`. Non-2xx responses preserve Billit
JSON errors where possible. Network failures return `success: false` and
`error_code: "REQUEST_ERROR"`.

## Billit MCP Rate Limiting and Client Lifecycle

The client uses a process-wide token bucket rate limiter. This prevents each
request-scoped FastAPI client from resetting its own bucket and accidentally
overrunning Billit API limits.

`BillitAPIClient` can be configured from environment variables, explicit
`BillitSettings`, or explicit `BillitOAuthSettings`. Local stdio and the
legacy adapter keep the env-derived API-key default. Hosted mode uses only
`BillitOAuthSettings`, so local API-key semantics cannot leak into hosted
requests.

FastAPI routes receive a request-scoped client through `billit/dependencies.py`
and close its underlying `httpx.AsyncClient` after each request. MCP tools use
one process-scoped client from `src/billit_mcp/server.py` and close it through
the FastMCP lifespan hook.

## Billit MCP Smart Search Data Flow

`billit/smart_search.py` implements local search for orders, parties, and
products. It fetches up to 120 records from the selected entity type, parses
amounts, dates, and content keywords from the user query, scores matches with
keyword checks and `SequenceMatcher`, then returns ranked results.

List-style Billit calls build pagination parameters through one shared helper,
which clamps `$top` to 120 before requests reach the Billit API.

The helper is used by both `GET /ai/smart-search` in the FastAPI adapter and
the `smart_search` / `debug_smart_search` MCP tools. Other composite helpers
live under `billit/services/` so MCP and FastAPI call local shared code instead
of forwarding local `/ai/...` routes through the Billit REST client. Upstream
Billit API failures are propagated instead of being converted into empty
successful results.

## Billit MCP Known Architecture Gotchas

MCP and FastAPI tool coverage is not identical. The FastAPI adapter contains
routes for accountant feeds, GL accounts, OCR processing, extra AI composites,
and Peppol inbox operations that are not currently registered as MCP tools.

Report tools use the canonical Billit path `/reports`. Financial transaction
tools use `/financialTransactions`. The local live canary records these
endpoint decisions in sanitized evidence when endpoint drift is being checked.

Billit payloads use PascalCase fields such as `OrderID`, `OrderLines`, and
`PartyID`. FastAPI route parameters often use snake_case for local ergonomics,
but forwarded JSON should match Billit field names unless a Pydantic model
explicitly maps aliases.

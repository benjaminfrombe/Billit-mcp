---
title: "Billit MCP - Architecture and Data Flow"
updated: 2026-05-27
---

# Billit MCP Architecture and Data Flow

Billit MCP has three server surfaces. The packaged runtime is a curated MCP
stdio server for local/private API-key usage. A hosted Streamable HTTP runtime
serves public OAuth usage. The legacy FastAPI adapter is retained for local
HTTP development and route tests.

## Billit MCP Packaged Runtime

`src/billit_mcp/server.py` creates a `FastMCP("billit-mcp")` instance and
registers only the curated local API-key tools from
`src/billit_mcp/local_api_key/`. Running `python -m billit_mcp` loads `.env`,
configures logging, imports the MCP server, and starts stdio protocol handling.
`LocalAPIKeyRuntime` is the compatibility facade; focused local modules own
settings, client audit, company entitlement, local state, read tools, and
invoice tools.

Local MCP tools use a process-scoped `BillitAPIClient` built from explicit
`BILLIT_API_KEY`, `BILLIT_BASE_URL`, and `BILLIT_PARTY_ID`. The local runtime
does not send `ContextPartyID` in the MVP. Redacted audit events, confirmation
challenges, and idempotency records are stored in SQLite under ignored
`.local/`, with no API keys, raw customer payloads, raw invoice payloads,
files, or webhook bodies.

The packaged stdio surface exposes exactly:

- `billit.connection_status`
- `billit.list_companies`
- `billit.search_orders`
- `billit.get_order`
- `billit.resolve_party`
- `billit.lookup_peppol_receiver`
- `billit.list_financial_transactions`
- `billit.list_reports`
- `billit.get_report`
- `billit.invoice.prepare`
- `billit.invoice.create_draft`
- `billit.invoice.prepare_send`
- `billit.invoice.confirm_send`
- `billit.invoice.get_delivery_status`
- `billit.invoice.summary`

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
surface. Hosted registration is grouped by company, order, party, and invoice
tool modules. The hosted registry intentionally exposes only the MVP tools:

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

`src/billit_mcp/services/hosted_runtime.py` remains the facade consumed by
hosted tool modules. Its internals are split into hosted claims, authorization,
Billit client/audit, confirmation, and idempotency services so hosted tool
registration stays thin without changing public tool names, arguments, scopes,
or persistence schema.

Local API-key and hosted OAuth invoice draft/send tools share the guarded
workflow in `src/billit_mcp/services/invoice_workflow.py`. Runtime adapters own
their own gates, scopes, company checks, idempotency state, and confirmation
state, while the workflow owns preflight, refetch/revalidate, operation hashes,
atomic challenge consumption, and the Billit send call ordering.
For draft creation, an existing idempotency record is replayed only when it is
`succeeded` with a stored Billit order id. Existing `started`, `failed`,
`conflict`, or `unknown_side_effect` records are blocked before another
`POST /orders`, and a detail refetch failure after a successful create does not
downgrade the recorded success.

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
response normalization. Legacy API-key callers can load:

- `BILLIT_API_KEY`
- `BILLIT_BASE_URL`
- `BILLIT_PARTY_ID`
- optional `RATE_LIMIT_PER_MINUTE`

The curated local API-key runtime passes explicit settings and forces
`context_party_id=None`, so `ContextPartyID` is disabled even if
`BILLIT_CONTEXT_PARTY_ID` is present in the environment.

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
`BillitSettings`, or explicit `BillitOAuthSettings`. Local stdio builds
explicit API-key settings from the required env vars and strips
`ContextPartyID`; the legacy adapter keeps the env-derived API-key default.
Hosted mode uses only `BillitOAuthSettings`, so local API-key semantics cannot
leak into hosted requests.

FastAPI routes receive a request-scoped client through `billit/dependencies.py`
and close its underlying `httpx.AsyncClient` after each request. Local MCP
tools use one process-scoped client from the local API-key runtime and close it
through the FastMCP lifespan hook.

## Billit MCP Smart Search Data Flow

`billit/smart_search.py` implements local search for orders, parties, and
products. It fetches up to 120 records from the selected entity type, parses
amounts, dates, and content keywords from the user query, scores matches with
keyword checks and `SequenceMatcher`, then returns ranked results.

List-style Billit calls build pagination parameters through one shared helper,
which clamps `$top` to 120 before requests reach the Billit API.

The helper is used by `GET /ai/smart-search` in the FastAPI adapter. The local
stdio MCP surface no longer exposes `smart_search` or `debug_smart_search`;
curated tools use structured allowlisted filters instead. Shared composite
helpers live under `billit/services/` so MCP, canaries, and FastAPI can call
local shared code instead of forwarding local `/ai/...` routes through the
Billit REST client.

## Billit MCP Known Architecture Gotchas

MCP and FastAPI tool coverage is intentionally not identical. The FastAPI
adapter contains raw development routes for accountant feeds, GL accounts, OCR
processing, extra AI composites, and Peppol inbox operations that are not
registered as MCP tools.

Report tools use the canonical Billit path `/reports`. Financial transaction
tools use `/financialTransactions`. The local live canary records these
endpoint decisions in sanitized evidence when endpoint drift is being checked.

Billit payloads use PascalCase fields such as `OrderID`, `OrderLines`, and
`PartyID`. FastAPI route parameters often use snake_case for local ergonomics,
but forwarded JSON should match Billit field names unless a Pydantic model
explicitly maps aliases.

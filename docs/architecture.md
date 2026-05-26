---
title: "Billit MCP - Architecture and Data Flow"
updated: 2026-05-26
---

# Billit MCP Architecture and Data Flow

Billit MCP has two server surfaces that share the same Billit REST client. The
packaged runtime is an MCP stdio server for AI clients. The legacy FastAPI
adapter is retained for local HTTP development and tests.

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

FastAPI routes receive a request-scoped client through `billit/dependencies.py`
and close its underlying `httpx.AsyncClient` after each request. MCP tools use
one process-scoped client from `src/billit_mcp/server.py` and close it through
the FastMCP lifespan hook.

## Billit MCP Smart Search Data Flow

`billit/smart_search.py` implements local search for orders, parties, and
products. It fetches up to 120 records from the selected entity type, parses
amounts, dates, and content keywords from the user query, scores matches with
keyword checks and `SequenceMatcher`, then returns ranked results.

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

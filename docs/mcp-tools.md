---
title: "Billit MCP - MCP Tool Reference"
updated: 2026-05-26
---

# Billit MCP Tool Reference

This page documents the tools registered by MCP runtimes. It does not describe
every legacy FastAPI route. For the HTTP adapter, see
[FastAPI Adapter Routes](fastapi-adapter.md).

## Billit MCP Local API-Key Stdio Tools

`python -m billit_mcp` exposes only this local/private API-key tool surface.
It does not register raw legacy create/update/delete/webhook/admin tools from
`billit/tools/`, and it does not provide an opt-in raw mode.

| Local tool | Billit endpoint or service | Purpose |
| --- | --- | --- |
| `billit.connection_status` | `GET /account/accountInformation` | Check API-key auth, base URL, configured `BILLIT_PARTY_ID`, company entitlement parsing, local write/send gates, and local state path. |
| `billit.list_companies` | `GET /account/accountInformation` | List company Party IDs visible to the API key and mark whether the configured PartyID is authorized. |
| `billit.search_orders` | `GET /orders` | Search orders from structured allowlisted filters only. |
| `billit.get_order` | `GET /orders/{order_id}` | Fetch one order by ID with explicit `PartyID`. |
| `billit.resolve_party` | `GET /parties` | Resolve a customer or supplier without guessing on ambiguity. |
| `billit.lookup_peppol_receiver` | `GET /peppol/participantInformation/{identifier}` | Check Peppol receiver visibility. |
| `billit.list_financial_transactions` | `GET /financialTransactions` | List imported bank transactions without mutation tools. |
| `billit.list_reports` | `GET /reports` | List available reports. |
| `billit.get_report` | `GET /reports/{report_id}` | Fetch a report using bounded scalar parameters. |
| `billit.invoice.prepare` | Shared local preflight | Validate an invoice draft request without writing. |
| `billit.invoice.create_draft` | `POST /orders` | Create a sales invoice draft when `BILLIT_MCP_LOCAL_ALLOW_WRITES=1`; never sends. |
| `billit.invoice.prepare_send` | `GET /orders/{order_id}` plus local confirmation state | Refetch and validate an invoice, then create a local confirmation challenge when `BILLIT_MCP_LOCAL_ALLOW_SENDS=1`. |
| `billit.invoice.confirm_send` | `GET /orders/{order_id}` then `POST /orders/commands/send` | Refetch, revalidate, atomically consume the matching confirmation challenge, then send. |
| `billit.invoice.get_delivery_status` | `GET /orders/{order_id}` | Summarize fresh delivery and payment state. |
| `billit.invoice.summary` | Shared local helper plus `GET /orders` | Summarize sales invoices for a date range. |

Local mode requires `BILLIT_API_KEY`, `BILLIT_BASE_URL`, and
`BILLIT_PARTY_ID`. Every Billit call sends `apiKey` and explicit `PartyID`.
`ContextPartyID` is disabled for this MVP. Reads can continue with warnings
when company-list parsing is inconclusive; draft creation and sending require
the configured PartyID to be verified by `accountInformation`.

Local audit, idempotency, and confirmation state are stored under ignored
`.local/`. They store redacted operational metadata only: no API keys, raw
customer payloads, raw invoice payloads, files, or webhook bodies.

## Billit MCP Hosted OAuth MVP Tools

Hosted mode exposes only this curated tool surface. It uses Billit OAuth grants
and synced `company_party_id` authorization. Hosted mode must not read local
API-key environment variables.

| Hosted tool | Billit endpoint or service | Purpose |
| --- | --- | --- |
| `billit.connection_status` | Local OAuth state | Check MCP auth, Billit connection state, and environment. |
| `billit.list_companies` | Synced account information | List authorized `company_party_id` values. |
| `billit.search_orders` | `GET /orders` | Search orders from structured allowlisted filters only. |
| `billit.get_order` | `GET /orders/{order_id}` | Fetch one order after company authorization. |
| `billit.resolve_party` | `GET /parties` | Resolve a customer or supplier without guessing on ambiguity. |
| `billit.lookup_peppol_receiver` | `GET /peppol/participantInformation/{identifier}` | Check Peppol receiver visibility. |
| `billit.invoice.prepare` | Shared local preflight | Validate an invoice draft request without writing. |
| `billit.invoice.create_draft` | `POST /orders` | Create a sales invoice draft; does not send. |
| `billit.invoice.prepare_send` | `GET /orders/{order_id}` plus confirmation state | Create a server-owned confirmation challenge. |
| `billit.invoice.confirm_send` | `POST /orders/commands/send` | Send only after consuming the matching challenge. |
| `billit.invoice.get_delivery_status` | `GET /orders/{order_id}` | Summarize fresh delivery and payment state. |

Hosted calls must include an explicit `environment` and `company_party_id`, and
the server checks that ID against companies synced from Billit account
information. Invoice sending never accepts a generic `confirmed: true`; the
model must use the `prepare_send` / `confirm_send` challenge flow.

## Billit MCP Raw Tool Migration

The old broad stdio MCP surface is intentionally removed. Use these curated
tools instead:

| Old raw MCP intent | Replacement |
| --- | --- |
| `list_orders` with raw `$filter` | `billit.search_orders` with structured fields. |
| `get_order` | `billit.get_order`. |
| `list_parties` | `billit.resolve_party` with `role`, name, VAT, email, or external provider ID. |
| `check_peppol_participant` | `billit.lookup_peppol_receiver`. |
| `list_financial_transactions` | `billit.list_financial_transactions`. |
| `list_available_reports` | `billit.list_reports`. |
| `get_report` | `billit.get_report`. |
| `generate_invoice_summary` | `billit.invoice.summary`. |
| `create_order` for sales invoices | `billit.invoice.prepare`, then `billit.invoice.create_draft` with local writes enabled. |
| `send_order` | `billit.invoice.prepare_send`, then `billit.invoice.confirm_send` with local sends enabled. |

No MCP replacement exists for raw party/product/order mutation, deletes,
payment marking, booking entries, bank-file import, SSO tokens, company
registration, document upload/download, webhook mutation, Peppol registration,
or arbitrary Billit endpoint passthrough. Keep those in development-only
FastAPI adapter work until a scoped, confirmation-gated workflow is designed.

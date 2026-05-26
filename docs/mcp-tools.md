---
title: "Billit MCP - MCP Tool Reference"
updated: 2026-05-26
---

# Billit MCP Tool Reference

This page documents the tools registered by the packaged MCP server in
`src/billit_mcp/server.py`. It does not describe every legacy FastAPI route.
For the HTTP adapter, see [FastAPI Adapter Routes](fastapi-adapter.md).

## Billit MCP Party Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `list_parties` | `GET /parties` | List customers or suppliers with optional OData filtering. |
| `create_party` | `POST /parties` | Create a customer or supplier from a Billit-style payload. |
| `get_party` | `GET /parties/{party_id}` | Fetch one party by Billit Party ID. |
| `update_party` | `PATCH /parties/{party_id}` | Patch party fields with a Billit-style payload. |

Use PascalCase fields in payloads unless a wrapper explicitly documents a
different shape. Party IDs are Billit IDs, not local database IDs.

## Billit MCP Product Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `list_products` | `GET /products` | List products with optional OData filtering. |
| `get_product` | `GET /products/{product_id}` | Fetch one product by ID. |
| `upsert_product` | `POST /products` | Create or update a product. |

The minimal product model currently maps `ProductID` and `Description`.
Additional Billit fields can still pass through dictionary payloads in the MCP
tool, but route-level validation in the legacy FastAPI adapter is narrower.

## Billit MCP Order Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `list_orders` | `GET /orders` | List invoices, credit notes, and other orders. |
| `create_order` | `POST /orders` | Create an order from a Billit payload. |
| `get_order` | `GET /orders/{order_id}` | Fetch order details by ID. |
| `update_order` | `PATCH /orders/{order_id}` | Patch Billit-supported order fields. |
| `delete_order` | `DELETE /orders/{order_id}` | Delete a draft order. |
| `record_payment` | `POST /orders/{order_id}/payment` | Record payment information. |
| `send_order` | `POST /orders/commands/send` | Send one or more orders by SMTP, Peppol, or another Billit transport. |
| `add_booking_entries` | `POST /orders/{order_id}/booking` | Add accounting booking entries. |
| `list_deleted_orders` | `GET /orders/deleted` | Retrieve deleted order markers for synchronization. |

`send_order` maps `Email` to `SMTP` and can set the `StrictTransportType`
header when `strict_transport` is true. Billit may fall back from Peppol to
email unless strict transport is requested.

## Billit MCP Financial Transaction Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `list_financial_transactions` | `GET /financialTransactions` | List imported bank transactions. |
| `import_transactions_file` | `POST /financialTransactions/importFile` | Upload or reference a bank statement import. |
| `confirm_transaction_import` | `POST /financialTransactions/commands/import` | Confirm a transaction import. |

The MCP implementation sends JSON with file path metadata. The legacy FastAPI
adapter accepts uploaded files for this workflow.

## Billit MCP Account and Document Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `get_account_information` | `GET /account/accountInformation` | Inspect authenticated account details. |
| `get_sso_token` | `GET /account/ssoToken` | Request an SSO token for the Billit web UI. |
| `get_next_sequence_number` | `POST /account/sequences` | Request or consume a sequence number. |
| `register_company` | `POST /account/registercompany` | Register a company under accountant flows. |
| `list_documents` | `GET /documents` | List documents with optional filtering. |
| `upload_document` | `POST /documents` | Upload document metadata and file reference. |
| `get_document` | `GET /documents/{document_id}` | Fetch document metadata. |
| `download_file` | `GET /files/{file_id}` | Download a Billit file by File ID. |

File upload behavior differs between MCP and FastAPI. Validate real upload
flows against sandbox before depending on them operationally.

## Billit MCP Webhook and Peppol Tools

| Tool | Billit endpoint | Purpose |
| --- | --- | --- |
| `create_webhook` | `POST /webhook` | Create a webhook subscription. |
| `list_webhooks` | `GET /webhook` | List webhook subscriptions. |
| `delete_webhook` | `DELETE /webhook/{webhook_id}` | Delete a webhook. |
| `refresh_webhook_secret` | `POST /webhook/{webhook_id}/refresh` | Refresh webhook signing secret. |
| `check_peppol_participant` | `GET /peppol/participantInformation/{identifier}` | Check Peppol registration. |
| `register_peppol_participant` | `POST /peppol/participants` | Register the current company on Peppol. |
| `send_peppol_invoice` | `POST /peppol/sendOrder` | Send an order through Peppol. |

The FastAPI adapter exposes additional Peppol inbox and unregister routes that
are not currently MCP tools.

## Billit MCP Composite, Utility, and Report Tools

| Tool | Billit endpoint or helper | Purpose |
| --- | --- | --- |
| `smart_search` | Local helper plus `/orders`, `/parties`, `/products` | Search Billit records using local scoring. |
| `debug_smart_search` | Local helper plus `/orders`, `/parties`, `/products` | Return search results with parsed debug metadata. |
| `suggest_payment_reconciliation` | `GET /ai/suggest-payment-reconciliation` | Legacy wrapper; currently points at an AI route path, not a known Billit REST path. |
| `generate_invoice_summary` | `GET /ai/invoice-summary` | Legacy wrapper; FastAPI has local implementation. |
| `list_overdue_invoices` | `GET /ai/overdue-invoices` | Legacy wrapper; FastAPI has local implementation. |
| `get_cashflow_overview` | `GET /ai/cashflow` | Legacy wrapper; FastAPI has local implementation. |
| `search_company` | `GET /misc/companysearch/{keywords}` | Search public company data through Billit. |
| `get_type_codes` | `GET /misc/typecodes/{code_type}` | Retrieve Billit system code lists. |
| `list_available_reports` | `GET /reports` | List report types. |
| `get_report` | `GET /reports/{report_id}` | Retrieve a report with optional query parameters. |

Do not assume the legacy AI wrappers work against the public Billit REST API.
Use `smart_search` for the currently shared local composite path, or call the
FastAPI adapter if you intentionally need the local AI route implementations.

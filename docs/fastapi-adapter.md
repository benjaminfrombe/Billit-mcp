---
title: "Billit MCP - Legacy FastAPI Adapter Routes"
updated: 2026-05-26
---

# Billit MCP Legacy FastAPI Adapter Routes

The FastAPI adapter in `server.py` is a local HTTP surface around the same
Billit client and helper modules. It is useful for `httpx.ASGITransport` tests,
manual Swagger checks, and validating route-level request parsing.

Run it locally with:

```bash
uv run uvicorn server:app --reload
```

## Billit MCP FastAPI Route Table

| Method | Route | Handler |
| --- | --- | --- |
| `GET` | `/account` | `get_account_information` |
| `GET` | `/account/sso` | `get_sso_token` |
| `GET` | `/account/sequence/{sequence_type}` | `get_next_sequence_number` |
| `POST` | `/account/register` | `register_company` |
| `POST` | `/feeds` | `register_feed` |
| `GET` | `/feeds` | `list_feeds` |
| `GET` | `/feeds/{feed_name}` | `get_feed_items` |
| `GET` | `/feeds/{feed_name}/{item_id}` | `download_feed_item_content` |
| `POST` | `/feeds/{feed_name}/{item_id}/confirm` | `confirm_feed_item` |
| `DELETE` | `/feeds/{feed_name}` | `delete_feed` |
| `GET` | `/ai/suggest-payment-reconciliation` | `suggest_payment_reconciliation` |
| `GET` | `/ai/invoice-summary` | `generate_invoice_summary` |
| `GET` | `/ai/expense-summary` | `generate_expense_summary` |
| `GET` | `/ai/cashflow` | `get_cashflow_overview` |
| `POST` | `/ai/categorize-expense/{invoice_id}` | `categorize_expense_invoice` |
| `GET` | `/ai/overdue-invoices` | `list_overdue_invoices` |
| `GET` | `/ai/supplier-spend/{supplier_id}` | `get_supplier_spend_summary` |
| `GET` | `/ai/customer-revenue/{customer_id}` | `get_customer_revenue_summary` |
| `GET` | `/ai/duplicate-contacts` | `find_duplicate_contacts` |
| `POST` | `/ai/normalize-address/{party_id}` | `normalize_contact_address` |
| `POST` | `/ai/create-invoice-from-text` | `create_invoice_from_text` |
| `GET` | `/ai/smart-search` | `smart_search` |
| `GET` | `/documents` | `list_documents` |
| `POST` | `/documents` | `upload_document` |
| `GET` | `/documents/{document_id}` | `get_document` |
| `GET` | `/files/{file_id}` | `download_file` |
| `GET` | `/financial-transactions` | `list_financial_transactions` |
| `POST` | `/financial-transactions/import` | `import_transactions_file` |
| `POST` | `/financial-transactions/{import_id}/confirm` | `confirm_transaction_import` |
| `POST` | `/gl-accounts` | `create_gl_account` |
| `POST` | `/gl-accounts/import` | `import_gl_accounts` |
| `POST` | `/journal-entries/import` | `import_journal_entries` |
| `GET` | `/search-company` | `search_company` |
| `GET` | `/type-codes/{code_type}` | `get_type_codes` |
| `GET` | `/type-codes/{code_type}/{code_key}` | `get_code_detail` |
| `GET` | `/orders` | `list_orders` |
| `POST` | `/orders` | `create_order` |
| `GET` | `/orders/deleted` | `list_deleted_orders` |
| `GET` | `/orders/{order_id}` | `get_order` |
| `PATCH` | `/orders/{order_id}` | `update_order` |
| `DELETE` | `/orders/{order_id}` | `delete_order` |
| `POST` | `/orders/{order_id}/payments` | `record_payment` |
| `POST` | `/orders/send` | `send_order` |
| `POST` | `/orders/{order_id}/booking` | `add_booking_entries` |
| `GET` | `/parties` | `list_parties` |
| `POST` | `/parties` | `create_party` |
| `GET` | `/parties/{party_id}` | `get_party` |
| `PATCH` | `/parties/{party_id}` | `update_party` |
| `PATCH` | `/parties/{party_id}/raw` | `update_party_raw` |
| `GET` | `/peppol/participantInformation/{identifier}` | `check_peppol_participant` |
| `POST` | `/peppol/participants` | `register_peppol_participant` |
| `DELETE` | `/peppol/participants` | `unregister_peppol_participant` |
| `POST` | `/peppol/sendOrder` | `send_peppol_invoice` |
| `GET` | `/peppol/inbox` | `list_peppol_inbox` |
| `POST` | `/peppol/inbox/{inbox_item_id}/confirm` | `confirm_peppol_invoice` |
| `POST` | `/peppol/inbox/{inbox_item_id}/refuse` | `refuse_peppol_invoice` |
| `GET` | `/products` | `list_products` |
| `GET` | `/products/{product_id}` | `get_product` |
| `POST` | `/products` | `upsert_product` |
| `GET` | `/reports` | `list_available_reports` |
| `GET` | `/reports/{report_id}` | `get_report` |
| `POST` | `/process` | `submit_document_for_processing` |
| `PATCH` | `/process/{upload_id}` | `update_processing_request` |
| `DELETE` | `/process/{upload_id}` | `cancel_processing_request` |
| `POST` | `/webhooks` | `create_webhook` |
| `GET` | `/webhooks` | `list_webhooks` |
| `DELETE` | `/webhooks/{webhook_id}` | `delete_webhook` |
| `POST` | `/webhooks/{webhook_id}/refresh-secret` | `refresh_webhook_secret` |

## Billit MCP FastAPI Adapter Gotchas

The adapter is not packaged as the main runtime. Do not document FastAPI
routes as MCP tools unless they are also registered in `src/billit_mcp/server.py`.

File upload routes use `UploadFile` and form metadata. MCP tools cannot pass
browser multipart forms directly, so validate file workflows separately for
MCP clients.

The local AI routes in `billit/tools/ai_composite.py` are simple deterministic
helpers. They are useful for workflow assistance, but they are not a machine
learning service and should not be documented as Billit-native endpoints.

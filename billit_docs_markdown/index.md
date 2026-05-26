---
title: "Billit API Source Docs - Reference Index"
updated: 2026-05-26
---

# Billit API Source Docs Reference Index

This directory contains Markdown snapshots of upstream Billit API reference
material. These files are source references for endpoint semantics, payload
fields, transport behavior, OData syntax, Peppol identifiers, and webhook
signatures. They are not implementation plans for this repository.

Use the project docs in `../docs/` first when you need to understand how this
MCP server is wired. Use this folder when you need Billit-specific details such
as order payload examples, identifiers, status codes, Peppol receiver rules, or
webhook verification.

## Billit API Source Docs for Authentication and Environments

[Authentication](authentication.md), [header values](header-values.md),
[sandbox versus production](sandbox-vs-production.md), and
[OAuth setup](how-do-i-get-started-with-oauth.md) explain how Billit expects
API keys, party IDs, environments, and OAuth flows to be supplied. The MCP
server uses API-key authentication through environment variables, while OAuth
material is retained as upstream context for future integrations.

## Billit API Source Docs for Orders and E-Invoicing

[Creating sales invoices](creating-sales-invoices.md),
[sending the first sales invoice](sending-your-first-sales-invoice.md),
[invoice retrieval](retrieve-list-of-invoices.md), and
[invoice status retrieval](retrieve-invoice-info-and-status.md) are the main
references for order payloads and order lifecycle behavior. Related edge cases
cover invoice comments, purchase order numbers, VAT identifiers, empty order
lines, attachments, and email fallback when e-invoicing is unavailable.

## Billit API Source Docs for Contacts, Identifiers, and Products

[Identifiers](identifiers.md),
[company and party ID lookup](where-can-i-find-my-companyid-or-a-partyid.md),
[type codes](types.md), and [OData filtering](odata.md) are the most useful
source docs for party lookup, filtering, and integration-safe identifiers.
These references explain why project code uses PascalCase Billit field names in
payloads while Python route parameters use snake_case.

## Billit API Source Docs for Files, Webhooks, and Processing

[Get files](get-files.md), [include PDFs and attachments](include-own-pdf-and-attachments-in-invoice-to-deliver.md),
[webhooks](webhooks.md), [webhook signatures](verify-signature.md), and
[webhooks for e-invoice statuses](webhooks-for-pushing-e-invoice-statuses.md)
cover file downloads, attachment delivery, callback configuration, and signing
verification. These files are the first place to check when changing document,
file, or webhook behavior.

## Billit API Source Docs for Peppol and Receiving

[Who is an e-invoice receiver](who-is-a-einvoice-receiver.md),
[API for receiving supplier invoices](api-for-receiving-supplier-invoices.md),
[approval process](approval-process.md), and
[network environments](network-environments.md) provide upstream context for
Peppol participant checks, incoming invoice handling, and processing flows.
Project implementation currently exposes a subset of these operations through
MCP and the legacy FastAPI adapter.

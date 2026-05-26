---
title: "Billit MCP - Billit API Source Reference Guide"
updated: 2026-05-26
---

# Billit MCP Billit API Source Reference Guide

The `billit_docs_markdown/` directory contains upstream Billit API reference
snapshots. These documents are not project architecture docs and should not be
treated as an implementation plan. They are retained so contributors can check
Billit-specific payload rules without leaving the repository.

## Billit API Source Docs for Common Implementation Tasks

Use [Authentication](../billit_docs_markdown/authentication.md) and
[Header Values](../billit_docs_markdown/header-values.md) when changing
authentication headers in `billit/client.py`.

Use [OData](../billit_docs_markdown/odata.md) when changing `odata_filter`
pass-through behavior in list tools and routes.

Use [Creating Sales Invoices](../billit_docs_markdown/creating-sales-invoices.md),
[Retrieve List of Invoices](../billit_docs_markdown/retrieve-list-of-invoices.md),
and [Patchable Properties](../billit_docs_markdown/patchable-properties.md)
when changing order creation, order listing, or order patch behavior.

Use [Get Files](../billit_docs_markdown/get-files.md) and
[Include PDFs and Attachments](../billit_docs_markdown/include-own-pdf-and-attachments-in-invoice-to-deliver.md)
when changing document, file, or attachment behavior.

Use [Webhooks](../billit_docs_markdown/webhooks.md) and
[Verify Signature](../billit_docs_markdown/verify-signature.md) when changing
webhook configuration or callback verification docs.

Use [Who is an E-Invoice Receiver](../billit_docs_markdown/who-is-a-einvoice-receiver.md)
and [Send via Email When E-Invoice Delivery Is Not Possible](../billit_docs_markdown/send-via-email-when-delivery-as-einvoice-is-not-possible.md)
when changing Peppol participant checks or transport fallback behavior.

## Billit API Source Docs Maintenance Policy

Do not duplicate large upstream examples into project docs. Link to the source
reference and document only the local interpretation or local gotcha.

Keep source docs focused and searchable. The old monolithic `all_docs.md` file
was removed because it duplicated the split reference files and produced poor
QMD retrieval behavior.

If a new upstream reference page is added, give it `title` and `updated`
frontmatter and link it from
[Billit API Source Docs Reference Index](../billit_docs_markdown/index.md).

---
title: "Invoice Responses to the Sender"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/invoice-responses-to-the-sender"
source_slug: "invoice-responses-to-the-sender"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - invoice
  - responses
  - sender
---

### When Document is Received, do we send response to the Sender ?

When document is received with success at the level of Billit, an Invoice response is back to the sender:

- This will happen when TransferType is Peppol and when the receiver is registered for receiving Invoice Responses
- Information that will be sent back by Billit (automatically) : AB: The document has been successfully received.
- More information about IMR : [IMR](https://www.billit.eu/en-int/help-page/expenditure/invoices/where-can-i-see-imr-messages-from-invoices-sent-via-peppol/)

Updated7 months ago

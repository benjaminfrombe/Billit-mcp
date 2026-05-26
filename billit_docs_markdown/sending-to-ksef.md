---
title: "Sending to KSeF"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sending-to-ksef"
source_slug: "sending-to-ksef"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - sending
---

# Sending to KSeF

Sending the invoices, 2 options:

1. Send via API
2. Use no API, send manually or automatically

### Send via API

Use the commands/send API endpoint for immediate sending

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders/commands/send | POST | OK |

Example Json content:

Send Multiple InvoicesSend 1 Invoice

```json
{
"Transporttype" : "KSeF",
"OrderIDs" :
  [\
	1684998,\
	1684999\
  ]
}
```

```json
{
"Transporttype" : "KSeF",
"OrderIDs" :
  [\
    1684998\
  ]
}
```

## Sending without API

Options are:

1. Manual sending
1. This can can be useful if you want to check the invoices prior to sending or if you want to add attachments.
2. Enabling the automatic sending

More info : [https://docs.billit.be/docs/sending-your-first-invoice](sending-your-first-invoice.md)

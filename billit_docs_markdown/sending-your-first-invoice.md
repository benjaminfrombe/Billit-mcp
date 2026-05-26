---
title: "Sending the Sales Invoice"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sending-your-first-invoice"
source_slug: "sending-your-first-invoice"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - sending
  - first
  - invoice
  - sales
---

## Concept and Methods

Following the creation of your first invoice, the next step is to dispatch it to the recipient. Understanding that invoice delivery methods can vary significantly from one country to another and even among different customers, we've simplified the process to ensure ease and flexibility.

You can explore the various transportTypes available for sending invoices by visiting our documentation page [Transport Types](types.md#transport-types). It's important to note that not all features may be available on the test network within the sandbox environment. Therefore, we recommend regularly checking our network environments documentation for the most recent updates and changes. This proactive approach helps ensure that you're always aligned with the latest capabilities and requirements for invoice delivery.

Sending the invoices, 2 options:

1. Send via API
2. Use no API, send manually or automatically

## Send via API

Use the commands/send API endpoint for immediate sending

1. Content of the Json body : see example below.
1. You can send one or many invoices with one command,
2. All the invoices must be for the same TransportType (e.g. Peppol).
2. Available Transport Types
1. Multiple Transport types are available
      1. Einvoice Networks:
         1. Peppol
         2. Various other Einvoice networks
      2. Other : Send via Email, Letter
2. List of all TransportTypes can be found here -> [Transport Types](types.md#transport-types)

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders/commands/send | POST | OK |

Send Multiple InvoicesSend 1 Invoice

```json
{
"Transporttype" : "Peppol",
"OrderIDs" :
  [\
	1684998,\
	1684999\
  ]
}
```

```text
{
"Transporttype" : "Peppol",
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
1. The automatic sending can be enabled. Every day at 9 am all non-sent invoices will be sent.
2. How to enable it
      1. In MyBillit interface, go to company settings page : Settings/General/Advanced : "Automatically send your invoices to the customer").

![](https://files.readme.io/426bb71e707bbdff4fb1dd3a5159deaf189b1c2f68d671fd41b4aff405e4830f-2025-11-28_07-04-08.png)

Options in different languages:

- English : Automatically send your invoices to the customer
- Dutch : Verstuur je facturen automatisch naar de klant
- French : Envoyez automatiquement vos factures au client

## Validations performed by Billit when the sending is launched

Per transporttype, controls are executed linked to the TransportType (e.g. Peppol, Email, other E-invoice network).

Error types can be:

- The content is not compliant with the validation rules of the network (e.g. Peppol)
- The receiver is not on the network

In case of error, you will have to adjust the invoice before sending again.

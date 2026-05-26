---
title: "Types"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/types"
source_slug: "types"
category: "reference-errors"
topics:
  - reference
  - errors
  - types
---

# Party Types

Party types are mostly used when using the Party Endpoint or when creating an invoice using the Party object instead of a Party ID.

| Type | Definition |
| --- | --- |
| Customer | Used for outgoing invoices |
| Supplier | Used for incoming invoices |

## Address Types

| Type | Definition |
| --- | --- |
| DeliveryAddress | Used to set a delivery address on a invoice |
| InvoiceAddress | Used to set a invoicing address on a invoice |

## Order Types

| Type | Definition |
| --- | --- |
| Invoice | A standard invoice |
| CreditNote | A standard creditnote which can be linked to an invoice |
| Offer | An offer where an invoice can be created from |
| DeliveryNote | Delivery notice |
| OrderForm | Order notice, proof of order |

## Order Direction

| Type | Definition |
| --- | --- |
| Income | These outgoing sales invoices are for your incoming cashflow (AR) |
| Cost | These incoming supplier invoices are for your outgoing cashflow (AP) |

## Order Status

| Status constants |
| --- |
| Draft |
| ToSend |
| ToPay |
| ToInvoice |
| ToDeliver |
| ToDomiciliate |
| Sent |
| Invoiced |
| DeliveryNoteCreated |
| OrderFormCreated |
| Credited |
| Refused |
| Canceled |
| Paid |
| ApprovalNeeded |
| Delivered |
| PaymentFileGenerated |

## Order Approval states

| Status constants |
| --- |
| Pending |
| Approved |
| Rejected |
| ToApproveByMe |

## Transport Types

| Type | Definition |
| --- | --- |
| SMTP | To send an (e)-invoice over SMTP/Email |
| Letter | To send a physical letter of the invoice |
| Peppol | To send an invoice over the Peppol Network (Multiple Countries) |
| SDI | To send an invoice over the SDI network to Italy |
| KSeF | To send an invoice over the Polish network |
| OSA | To Send a notification report to Hungarian government |
| ANAF | To Send an Invoice to Romanian government |
| SAT | To send an invoice to the Mexican network |
| MyInvois | Malaysia MyInvois |
| Chorus | French GOV Chorus Network |
| PDP (Planned) | French E-invoice network (Planned) |

## Integrations

| Type | Definition |
| --- | --- |
| Peppol | Peppol Network |
| SDI | Italian Network |
| OSA | Hungarian Network |
| Chorus | French GOV Chorus Network |
| SAT | Mexican Network |
| KSeF | Polish Network |
| ANAF | To Send an Invoice to Romanian government |
| MyInvois | Malaysia MyInvois |

## Order Payment Types

| Type |
| --- |
| Other |
| Visa |
| Bancontact |
| Contant |
| Wired |
| Online |
| Domiciliation |
| PrivateAccount |

## Webhook Entity Types

| Type | Definition |
| --- | --- |
| Order | Orders, creditnotes, deliverynotes, ... |
| Message | Message contains all digital Transport Types |

## Webhook Update Types

| Type | Definition |
| --- | --- |
| I | A new entity |
| U | Updated entity |
| D | Deleted entity |

## Sequence Types

| Type |
| --- |
| Income-Invoice |
| Income-CreditNote |

## Accounting Cost Types

| Type |
| --- |
| GoodsForReSale |
| ServicesAndMiscellaneousGoods |
| Investments |

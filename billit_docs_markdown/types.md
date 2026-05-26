---
title: "Billit API Source Docs - Types"
updated: 2026-05-26
---

# Types\n\n# Party Types   [Skip link to Party Types](https://docs.billit.be/docs/types\#party-types)

Party types are mostly used when using the Party Endpoint or when creating an invoice using the Party object instead of a Party ID.

| Type | Definition |
| --- | --- |
| Customer | Used for outgoing invoices |
| Supplier | Used for incoming invoices |

## Address Types   [Skip link to Address Types](https://docs.billit.be/docs/types\#address-types)

| Type | Definition |
| --- | --- |
| DeliveryAddress | Used to set a delivery address on a invoice |
| InvoiceAddress | Used to set a invoicing address on a invoice |

## Order Types   [Skip link to Order Types](https://docs.billit.be/docs/types\#order-types)

| Type | Definition |
| --- | --- |
| Invoice | A standard invoice |
| CreditNote | A standard creditnote which can be linked to an invoice |
| Offer | An offer where an invoice can be created from |
| DeliveryNote | Delivery notice |
| OrderForm | Order notice, proof of order |

## Order Direction   [Skip link to Order Direction](https://docs.billit.be/docs/types\#order-direction)

| Type | Definition |
| --- | --- |
| Income | These outgoing sales invoices are for your incoming cashflow (AR) |
| Cost | These incoming supplier invoices are for your outgoing cashflow |

## Order Status   [Skip link to Order Status](https://docs.billit.be/docs/types\#order-status)

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

## Order Approval states   [Skip link to Order Approval states](https://docs.billit.be/docs/types\#order-approval-states)

| Status constants |
| --- |
| Pending |
| Approved |
| Rejected |
| ToApproveByMe |

## Transport Types   [Skip link to Transport Types](https://docs.billit.be/docs/types\#transport-types)

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

## Integrations   [Skip link to Integrations](https://docs.billit.be/docs/types\#integrations)

| Type | Definition |
| --- | --- |
| Peppol | Peppol Network |
| SDI | Italian Network |
| OSA | Hungarian Network |
| Chorus | French GOV Chorus Network |
| SAT | Mexican Network |
| KSeF | Polish Network |
| ANAF | To Send an Invoice to Romanian government |

## Order Payment Types   [Skip link to Order Payment Types](https://docs.billit.be/docs/types\#order-payment-types)

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

## Webhook Entity Types   [Skip link to Webhook Entity Types](https://docs.billit.be/docs/types\#webhook-entity-types)

| Type | Definition |
| --- | --- |
| Order | Orders, creditnotes, deliverynotes, ... |
| Message | Message contains all digital Transport Types |

## Webhook Update Types   [Skip link to Webhook Update Types](https://docs.billit.be/docs/types\#webhook-update-types)

| Type | Definition |
| --- | --- |
| I | A new entity |
| U | Updated entity |
| D | Deleted entity |

## Sequence Types   [Skip link to Sequence Types](https://docs.billit.be/docs/types\#sequence-types)

| Type |
| --- |
| Income-Invoice |
| Income-CreditNote |

## Accounting Cost Types   [Skip link to Accounting Cost Types](https://docs.billit.be/docs/types\#accounting-cost-types)

| Type |
| --- |
| GoodsForReSale |
| ServicesAndMiscellaneousGoods |
| Investments |

Updated30 days ago

* * *

Did this page help you?

Yes

No
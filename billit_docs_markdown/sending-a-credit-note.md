---
title: "Credit Note"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sending-a-credit-note"
source_slug: "sending-a-credit-note"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - sending
  - credit
  - note
---

# Credit Note

The API body for Credit Note is similar to an invoice. Below some specific points of attention.

## How to Define it is a Credit Note

When OrderType is set to CreditNote,

- the document will be defined as a CreditNote.
- The amounts in API-stay **positive** ! Even if amounts are negative on your PDF, in Json they need to be positive.
- As it is related to sales operations, the OrderDirection is Income.
- ExpiryDate remains a mandatory field.
- In the Peppol output UBL does not include bank account number and Payment information.

Example of a Json body of a CreditNote:

Json body CreditNote

```json
{
 "OrderType": "CreditNote",
 "OrderDirection": "Income",
 "OrderNumber": "QS-8596",
 "OrderDate": "2025-06-01",
 "ExpiryDate": "2025-08-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
 ]
}
```

## Reference to an Invoice

When a CreditNote refers to a preceding Invoice, then this reference can be included. "AboutInvoiceNumber" is the tag used for it.

Specific point of attention:

- if there is no link with an invoice, do not include the tag "AboutInvoiceNumber".
- When using "AboutInvoiceNumber"
  - Billit will check that the invoice number exists at Billit. If not, an error will be prompted.
  - When you start with the creation of invoices via an API, the following scenario might occur:
    - Create a credit note via API with AboutInvoiceNumber,
    - The previous invoice was not created via Billit with API (was before the start with Billit)
    - Error will be prompted that invoice could not be found
    - Solution:
      - Send CreditNote via API without the field "AboutInvoiceNumber"
      - Create the Invoice in Billit (without sending, via API or manually), then create the CreditNote (via API or manually.

## CreditNote is Paid / Not Paid

**Standard Behaviour**

Is the CreditNote still to be paid ? Below the parameters that define this.

| Json "AboutInvoiceNumber" used | Json "Paid" field scenario's | UBL Prepaid Amount | UBL Payable Amount |
| --- | --- | --- | --- |
| No | "Paid" Not Used | 0 | Full Amount |
| No | "Paid" : true | Full Amount | 0 |
| No | "Paid": false | 0 | Full Amount |
| Yes | "Paid" Not Used | Full Amount | 0 |
| Yes | "Paid" : true | Full Amount | 0 |
| Yes | "Paid": false | Full Amount | 0 |

**How to combine AboutInvoiceNumber and "To Be Paid"**

This is currently not possible.

## Other Payment Info in CreditNote

What other payment info can be included in the outgoing UBL file via API ?

| Information Type in API-content | Included in outgoing UBL |
| --- | --- |
| PaymentMeansCode | not included |
| PaymentTerms | included |
| IBAN/BIC number | not included |

- [Custom Fields - Credit Note](custom-fields-credit-note.md)
- [Negative Lines on an Invoice](negative-lines.md)

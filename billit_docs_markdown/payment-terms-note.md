---
title: "PaymentTerms Note"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/payment-terms-note"
source_slug: "payment-terms-note"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - payment
  - terms
  - note
  - paymentterms
---

## Payment Terms Note Info

It might be interesting to add additional text info about Payment Terms. It does not contain a reference, just additional descriptions. When using the tag in CustomFields "Payment Terms", then in case of Peppol this text info will appear in tag PaymentTerms/Note.

How it is included in the Json body on header level:

Direct Debit Json body

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-X009a",
 "OrderDate": "2025-07-28",
 "ExpiryDate": "2025-08-30",
 "CustomFields"  : {
    "PaymentTerms": "30 days end of the month" //Add your text info
    },
  "Customer": {
   "Name": "CustomerName",
   "VATNumber": "BE0437295999",

   },
 "OrderLines": [\
  {\
   "Quantity": 1.02,\
   "UnitPriceExcl": 10.03,\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

How it does appear in the Peppol UBL:

![](https://files.readme.io/c5ad445606f14693ddfa1a8bc98ed6453c13e7ed113d0c347f17bc7278fbecfc-PaymentTerms.jpg)

## Display Payment Terms Note info on Billit generated PDF

The PDF that is sent with the einvoice can be your own PDF or a Billit generated PDF. In case of a Billit generated PDF, you might want the specific Payment Note info text on the PDF.

This can be done by using the "Comments" tag in the API Json body text. Here you could copy the same text as in "Payment Terms". Result will be that the text appears on the PDF.

Remark : when using"Comments", you cannot use the CustomField "Invoice.Note".

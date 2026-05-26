---
title: "Negative Lines on an Invoice"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/negative-lines"
source_slug: "negative-lines"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - negative
  - lines
  - invoice
---

# Negative Lines on an Invoice

An invoice related to sales operations has a positive total. But it is allowed that one or more lines of the invoice has a negative Line Total.

How this is done in Billit:

- Quantity is positive
- UnitPriceExcl is negative.

This will be converted in e-invoice networks (e.g. Peppol) in the correct way.

Example of a Json body of an Invoice, where line one has negative total and line 2 has a positive total.

Json body Invoice, line 2 negative

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-484125Neg",
 "OrderDate": "2025-12-29",
 "ExpiryDate": "2026-01-31",
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
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
       {\
   "Quantity": 10,\
   "UnitPriceExcl": 12.0,\
   "Reference": "987965",\
   "Description": "Testproduct",\
   "VATPercentage": 21.0,\
   },\
     {\
   "Quantity": 2,\
   "UnitPriceExcl": -5.00,  //Json : unit price must be negative\
   "Description": "Voucher",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

This is how the negative line will appear in the UBL (line 2 is the negative line):

![](https://files.readme.io/505d5ac104f830ba59cb2f8010eb0582f535b5743d31403ebc3437dd28c9b5c2-2025-12-29_10-57-27.png)

Updated5 months ago

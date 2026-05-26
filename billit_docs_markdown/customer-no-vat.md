---
title: "Company has no VAT number"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/customer-no-vat"
source_slug: "customer-no-vat"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - customer
  - no
  - vat
  - company
  - has
  - number
---

## No VAT Number

When a customer is not VAT registered, and no VAT is mentioned in the API content when posting an invoice, then Billit will overwrite an existing customer with VAT number.

A solution to fix this is to add an additional identifier, e.g.

- company number
- GLN number

Example Json

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-005457",
 "OrderDate": "2025-12-01",
 "ExpiryDate": "2025-12-30",
  "Customer": {
   "Name": "Politie XYZ",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0793249999"  //This information is needed to make sure that a uniwue customer is created in Billit\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Politie XYZ",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1a",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Politie XYZ",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "Zipcode" : "9001",\
        "Box": "b",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 0.1,\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
 ]
}
```

Result is a unique customer in Billit:

![](https://files.readme.io/b594565054f381152b036c1309711ba202ce93886e7ae544a68f3d96abaf8023-2025-12-01_16-42-00.png)

- [Send to Customer with GLN Number](send-to-customer-with-gln-number.md)

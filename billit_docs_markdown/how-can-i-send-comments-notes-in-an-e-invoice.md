---
title: "Billit API Source Docs - How Can I Send Comments Notes In An E Invoice"
updated: 2026-05-26
---

# How can I send Comments/Notes in an e-invoice\n\nSometimes, you may want to include an additional note or comment for the recipient of the invoice. PEPPOL and other networks support sharing comments at the invoice level. With the Billit API, you can achieve this by using the `Invoice.Note` property in custom fields.

For more information on custom fields : [https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support)

Below Json Example with Note in the Custom Fields part:

json

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003",
 "OrderDate": "2025-05-05",
 "ExpiryDate": "2025-06-30",
  "CustomFields"  : {
     "Invoice.Note": "header note description: additional text information",
    },

  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003799999"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}

```

Updated24 days ago

* * *

Did this page help you?

Yes

No
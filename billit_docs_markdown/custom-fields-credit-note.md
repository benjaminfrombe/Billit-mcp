---
title: "Custom Fields - Credit Note"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/custom-fields-credit-note"
source_slug: "custom-fields-credit-note"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - custom
  - fields
  - credit
  - note
---

# Custom Fields - Credit Note

Specific to CreditNotes, the name the be use should contain "CreditNote" and not "Invoice". Below an example with a custom field on the second detail line:

Json body CreditNote

```json
{
 "OrderType": "CreditNote",
 "OrderDirection": "Income",
 "OrderNumber": "QS-9424",
 "OrderDate": "2025-06-15",
 "ExpiryDate": "2025-08-30",
  "AboutInvoiceNumber": "QS-9116",
 "CustomFields"  : {
    "CreditNote.InvoicePeriod.StartDate": "2025-05-01",
    "CreditNote.InvoicePeriod.EndDate": "2025-05-30",
    "CreditNote.Note": "header note 1234 ",
    },
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
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
      "VATPercentage": 21,\
   "CustomFields": {\
   "CreditNoteLine.Note": "Your ref: TW-169944  Our ref: 25001377"\
   }\
   }\
 ]
}
```

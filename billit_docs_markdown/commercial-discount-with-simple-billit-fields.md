---
title: "Commercial Discount with simple Billit Fields"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/commercial-discount-with-simple-billit-fields"
source_slug: "commercial-discount-with-simple-billit-fields"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - commercial
  - discount
  - simple
  - billit
  - fields
---

# Commercial Discount

On the invoice **line**:

- scenario 1 : you can mention a the line net price (no indication of commercial discount)
- scenario 2 : you can include the line discount information as a percentage. (if customer wants to know the discount details)

Input information in the API Json body

| Property | Sample Value | Info |
| --- | --- | --- |
| ReductionPercentage | 25 | Discount percentage |

Example:

API Json body Post

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-50001",
 "OrderDate": "2025-09-15",
 "ExpiryDate": "2025-10-30",
  "Customer": {
   "Name": "Customer Name",
   "VATNumber": "BE0759529999",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Customer Name",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zip": "9000",\
        "CountryCode": "BE"\
        },\
   ]
   },
  "OrderLines": [\
            {\
              "Quantity": 14,\
              "UnitPriceExcl": 2.23,\
              "Description": "my order line1",\
              "ReductionPercentage": 25,  // % commercial discount\
              "VATPercentage": 21.0\
            }\
            ],
}
```

Below an example how it will be included in the UBL when it is sent via Open/Peppol (Allowance on line level) :

![](https://files.readme.io/73d2db60c666d5198f8519c876f03623caf9d9cb611e4b4ce6f55628a8325395-commercial_discount.jpg)

Specific fields in the UBL:

| Property | Sample Value | Info |
| --- | --- | --- |
| 1 | ChargeIndicator | false : it is a discount |
| 2 | AllowanceChargeReason | fixed text set by Billit : allowance |
| 3 | Amount | Total amount of the line discount, calculated by Billit based on ReductionPercentage |

- [Allowances and Charges](allowances-and-charges-advanced.md)
- [Cash Discount with Allowances Charges](cash-discount-with-allowances-charges.md)

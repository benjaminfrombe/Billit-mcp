---
title: "Prepaid Invoice"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/prepaid"
source_slug: "prepaid"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - prepaid
  - invoice
---

## About Prepaid

An invoice might have been prepaid : partially or completely. It is important that this information is included in the einvoice sent to the customer.

| Information Element | Json tag | Example | Extra Info | Corresponding field when UBL |
| --- | --- | --- | --- | --- |
| Partially Paid | "ToPay" | "ToPay": 0.90 | If partially paid, then do not use the element "Paid". This is the amount to be paid, | LegalMonetaryTotal/PayableAmount = Total Amount of Invoice |
| Fully Paid | "Paid" | "Paid": true | If fully paid, then do not use the element "ToPay" | LegalMonetaryTotal/PayableAmount = 0 |
| Prepaid Amount | - | - | So Total Amount - ToPay is the prepaid amount. The prepaid amount is calculated by Billit. | LegalMonetaryTotal/PrepaidAmount |

## Examples Json and Output UBL

Below examples how it is included in the Json body on header level (partially paid and fully paid)

Partially Paid JsonFully Paid Json

```json
{
    "Order" : {
            "OrderNumber": "QS-202565987",
            "OrderType": "Invoice",
            "OrderDirection": "Income",
            "OrderDate": "2025-08-28",
            "ExpiryDate": "2025-08-28",
            "ToPay": 0.90,
            "OrderLines": [\
            {\
              "Quantity": 1,\
              "UnitPriceExcl": 1.0,\
              "Description": "my order line",\
              "VATPercentage": 21.0\
            }\
            ],
            "Customer": {
              "Name": "TestCustomerName",
              "VATNumber": "BE0446725999",
              "PartyType": "Customer",
              "Email" : "testuser@billit.eu"
            }
    }
}
```

```json
{
    "Order" : {
            "OrderNumber": "QS-202565987",
            "OrderType": "Invoice",
            "OrderDirection": "Income",
            "OrderDate": "2025-08-28",
            "ExpiryDate": "2025-08-28",
            "Paid": true,
            "OrderLines": [\
            {\
              "Quantity": 1,\
              "UnitPriceExcl": 1.0,\
              "Description": "my order line",\
              "VATPercentage": 21.0\
            }\
            ],
            "Customer": {
              "Name": "TestCustomerName",
              "VATNumber": "BE0446725999",
              "PartyType": "Customer",
              "Email" : "testuser@billit.eu"
            }
    }
}
```

What will be the result in case of the sending of a Peppol UBL, in the LegalMonetaryTotal segment:

Partially Paid UBL

```xml
  <cac:LegalMonetaryTotal>
    <cbc:LineExtensionAmount currencyID="EUR">1.00</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">1.00</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">1.21</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.31</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">0.90</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
```

The PrepaidAmount and the PayableAmount are adapted (calculated by Billit) accordingly.

## Billit Human Readable when fully paid

When the sender does not include a PDF, then a Billit Human Readable will be generated.

Indication Paid will appear on the Human Readable when:

- the amount is fully prepaid
- date will be based on the Json tag ""PaidDate"

Example:

![](https://files.readme.io/af4f7f0feba449347949abf1d06f96b1d05e1d773fd730830dbd1b4c43bd5768-2025-09-01_12-21-45.jpg)

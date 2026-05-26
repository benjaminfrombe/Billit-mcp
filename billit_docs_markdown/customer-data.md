---
title: "Content Requirements PA"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/customer-data"
source_slug: "customer-data"
category: "partner-france"
topics:
  - partner
  - france
  - customer
  - data
  - content
  - requirements
  - pa
---

## Define Invoice Type

For each invoice, an invoice type must be defined on header level. The basic options are :

| Type | Not (fully) Paid | Already Paid |
| --- | --- | --- |
| Goods Invoice | B1 | B2 |
| Service Invoice | S1 | S2 |
| Mixed Invoice | M1 | M2 |

This data element needs to be delivered to Billit. Specification will follow. In the mean time, Billit sends with the Billit default value S1.

## Define Customer Identifier

Find the identifiers of the customer. Include them in Billit.

More info : [Identifiers PA](identifiers-france-pa.md)

## Accepted Invoice Format of the Receiver - Determined by Billit

Sending the invoices to the receiver must be in a format registered by the receiver. Billit will automatically select a format that is registered by the receiver, you do not have to select the format yourself.

## Example of API content of an Invoice

Invoice

```json
{
    "OrderNumber": "227010068_Simple2",
    "OrderDate": "2026-05-06T00:00:00",
    "ExpiryDate": "2026-06-04T00:00:00",
    "OrderType": "Invoice",
    "OrderDirection": "Income",
    "Customer": {
        "Nr": "0001001999",
        "Name": "FR demo receive",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "FR demo receive",\
                "Street": "place demo receive 987",\
                "Zipcode": "75001",\
                "City": "PARIS",\
                "CountryCode": "FR"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "FR demo receive",\
                "Street": "place demo receive 987",\
                "Zipcode": "75001",\
                "City": "PARIS",\
                "CountryCode": "FR"\
            }\
        ],
        "Street": "place demo receive 987",
        "Zipcode": "75001",
        "City": "PARIS",
        "CountryCode": "FR",
        "Mobile": "+32475366999",
        "Email": "testuser@billit.eu",
        "VATNumber": "FR37127399999",
        "PartyType": "Customer",
        "VATLiable": true,
        "Language": "FR",
        "DisplayName": "FR demo receive",
        "VATDeductable": true,
        "Identifiers": [\
            {\
                "IdentifierType": "CTC",\
                "Identifier": "127369999_DEMO",\
            },\
            {\
                "IdentifierType": "SIRENE",\
                "Identifier": "127362116",\
            }\
        ],
        "SendUBL": true,
        "SendPDF": true
    },

    "OrderLines": [\
        {\
            "Quantity": 1.0,\
            "UnitPriceExcl": 400.0,\
            "Description": "just a single line",\
            "VATPercentage": 20.0,\
            "Unit": "PCE",\
            "DescriptionExtended": "some extended description"\
        }\
    ],
    "OrderTitle": "Simple",
    "Reference": "4512345678",
    "PaymentReference": "365878545",
    "Comments": "additional info",
    "Currency": "EUR",
    "DeliveryDate": "2026-04-27T00:00:00"
}
```

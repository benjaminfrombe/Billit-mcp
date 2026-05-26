---
title: "Payment Reference"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/payment-id"
source_slug: "payment-id"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - payment
  - id
  - reference
---

## Possible scenario's

Possible scenario's:

- the Billit generated Structured Payment Reference is in the einvoice message (default)
- You do not want the Billit generated Structured Payment Reference inthe einvoice message

## How it works

- the Billit generated Structured Payment Reference is in the einvoice message :
  - When Posting an Invoice without Payment Reference in the API Json body, then the Billit generated Structured Payment Reference will be included.
  - Impact : the customer will probably include this reference while paying. This allows to do payment matching in the MyBillit interface.
- You do not want the Billit generated Structured Payment Reference inthe einvoice message:
  - Include the Sender Structured Payment Reference : via the tag "PaymentReference" you can communicate your own structured Payment Reference (See example 1 below).
  - No Structured Payment Reference is needed: You can fill the tag "PaymentReference" with another value, e.g. the Invoice Number (See example 2 below).

Your Own Structured PaymentNo structured Payment Ref

```json
{

    "Order" : {
            "OrderType": "Invoice",
            "OrderDirection": "Income",
            "OrderNumber": "QS-29925", //Invoice Number
            "OrderDate": "2025-07-25",
            "ExpiryDate": "2025-08-30",
            "PaymentReference": "+++090/9337/55493+++", //If we want no OGM then you can insert invoice number
            "OrderLines":
                 {
   "Quantity": 3,
   "UnitPriceExcl": 5.00,
   "Description": "Services",
   "VATPercentage": 0
   }
            ],
            "Customer": {
              "Name": "Customer Company",
              "VATNumber": "BE0446729999",
              "PartyType": "Customer",
              "Contact" : "Jean Dupont",
              "Email" : "user1@billit.eu",
              "Phone" : "015/999999",
            }

}
```

```json
{
    "TransportType" : "Peppol",
    "Order" : {
            "OrderType": "Invoice",
            "OrderDirection": "Income",
            "OrderNumber": "QS-29925", //Invoice Number
            "OrderDate": "2025-07-25",
            "ExpiryDate": "2025-08-30",
            "PaymentReference": "QS-29925", //If we want no OGM then you can insert invoice number
            "OrderLines":
                 {
   "Quantity": 3,
   "UnitPriceExcl": 5.00,
   "Description": "Services",
   "VATPercentage": 0
   }
            ],
            "Customer": {
              "Name": "Customer Company",
              "VATNumber": "BE0446729999",
              "PartyType": "Customer",
              "Contact" : "Jean Dupont",
              "Email" : "user1@billit.eu",
              "Phone" : "015/999999",
            }
    }
}
```

## Billit PDF : Remove barcode for payment

If you are using the Billit generated human readable, but you do not want to have a barcode for payment displayed, you can remove it from the Billit template.

Actions:

- Go to Settings, Corporate Style. Choose document type Invoice (and possibly also CreditNote).
- Remove "$Order.PaymentQR$" from the template
- More information about Corporate Style / Template : [https://docs.billit.be/docs/billit-generated-pdf](billit-generated-pdf.md)

Where to find "$Order.PaymentQR$" (to remove) on the template:

![](https://files.readme.io/13888991d5ec5fe945f9e4c4b930f8111ca80ad6ba9431722043f6750c79bcfe-2026-01-27_15-53-13.png)

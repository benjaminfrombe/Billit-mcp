---
title: "Retrieve Invoice Info and Status"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/retrieve-invoice-information"
source_slug: "retrieve-invoice-information"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - retrieve
  - invoice
  - info
  - status
---

# Retrieve Invoice Info and Status

When an invoice has been created a unique ID is returned. With this ID you can use retrieve all information stored in Billit for this specific invoice. You will be able to retrieve the PDF, E-invoice delivery details, full tax calculations, Original sent E-invoice XML....

Good news! The response you will receive is the same object as you used to create the invoice. Meaning no additional objects need to be created!

> 📘
>
> ### Testable request in Postman: 03 - Retrieve invoice data

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders/{UniqueID} | GET | Order Object |

To test the testable request in Postman you will have to provide the request with the Unique ID returned when creating the invoice.

Because of the response containing al lot of information you will have a brief summary below of the most important fields.

| Property | Value Type | Info |
| --- | --- | --- |
| OrderID | UniqueID | Same ID as in request, the element needed for getting all info. |
| CompanyID | UniqueID | Company Owner ID of the invoice |
| OrderPDF | Object | Contains the PDF generated or provided for the invoice |
| Attachments | List<Object> | Contains the Attachments for the invoice and will always contain the original JSON used to created the invoivce through API. |
| OrderNumber | ID | The Unique invoice ID provided or generated |
| Customer | Object | Contains metadata for the invoice customer |
| Supplier | Object | Contains metadata for the Supplier (Sales invoices== self) |
| LastModified | DateTime | Last datetime when the invoice was modified |
| Created | Datetime | The date when the api processed the invoice |
| Orderlines | List<Object> | Contains the Invoice items in a list with tax calculated on them |
| VatGroups | List<Object> | Contains the different vatgroups calculated for the Invoice |
| Paid | Bool | If the invoice was paid or a payments was received in Billit this will be set to true |
| IsSent | Bool | If the invoice was sent Manually, API, or job it will be set to true |
| PaymentLinks | Object | Contains the EPC QR code for payments |
| CurrentDocumentDeliveryDetails | Object | Contains the information of the delivery of the document |
| Messages | List<object> | Contains all messages for incoming and outgoing traffic for the invoice |

Example output below

JSON

```json
{
    "OrderID": HIDDEN,
    "CompanyID": HIDDEN,
    "OrderPDF": {
        "FileID": "c1cd2bfa-XXXX-XXXX-XXXX-2f6d323bd2fc",
        "FileName": "Invoice_QS-001_Billit.pdf"
    },
    "Attachments": [\
        {\
            "FileID": "af3b583e-XXXX-XXXX-XXXX-2a7d8680a324",\
            "FileName": "QS-001__10_03_2024 15_00_49.json"\
        }\
    ],
    "OrderNumber": "QS-001",
    "Customer": {
        "PartyID": HIDDEN,
        "Name": "Billit",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "Billit",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "301",\
                "City": "Ghent",\
                "CountryCode": "BE"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "Billit",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "301",\
                "City": "Ghent",\
                "CountryCode": "BE"\
            }\
        ],
        "Street": "Oktrooiplein",
        "StreetNumber": "1",
        "Box": "301",
        "City": "Ghent",
        "CountryCode": "BE",
        "Contact": "",
        "ContactLastName": "",
        "VATNumber": "BE0563846944",
        "LastModified": "2024-03-10T15:00:49.487",
        "Created": "2024-03-10T13:55:42.723",
        "PartyType": "Customer",
        "VATLiable": true,
        "Language": "EN",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [],
        "DefaultPaid": false,
        "DisplayName": "Billit",
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "GLN",\
                "Identifier": "5430003732007",\
                "SchemeID": "0088"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR"
    },
    "Supplier": {
        "PartyID": HIDDEN,
        "Name": "Billit Quickstart",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "BILLIT",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "302",\
                "Zipcode": "9000",\
                "City": "Gent",\
                "CountryCode": "BE"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "BILLIT",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "302",\
                "Zipcode": "9000",\
                "City": "Gent",\
                "CountryCode": "BE"\
            }\
        ],
        "Street": "Oktrooiplein",
        "StreetNumber": "1",
        "Box": "302",
        "Zipcode": "9000",
        "City": "Gent",
        "CountryCode": "BE",
        "IBAN": "HIDDEN",
        "BIC": "GKCCBEBB",
        "Phone": "HIDDEN",
        "Email": "thibau@billit.be",
        "Contact": "Thibau Verberckmoes",
        "ContactFirstName": "Thibau",
        "ContactLastName": "Verberckmoes",
        "VATNumber": "BE0563846944",
        "LastModified": "2024-03-10T15:00:39.91",
        "Created": "2024-03-10T13:16:02.34",
        "PartyType": "Supplier",
        "VATLiable": true,
        "Language": "EN",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [\
            {\
                "IBAN": "HIDDEN",\
                "BIC": "GKCCBEBB",\
                "Currency": "EUR",\
                "Verified": false,\
                "Saldo": 0.00\
            }\
        ],
        "DefaultPaid": false,
        "DisplayName": "Billit Quickstart",
        "FinancialReductionPercentageDefault": 2.00,
        "FinancialReductionDaysDefault": 8,
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR"
    },
    "CounterParty": {
        "PartyID": HIDDEN,
        "Name": "Billit",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "Billit",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "301",\
                "City": "Ghent",\
                "CountryCode": "BE"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "Billit",\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "301",\
                "City": "Ghent",\
                "CountryCode": "BE"\
            }\
        ],
        "Street": "Oktrooiplein",
        "StreetNumber": "1",
        "Box": "301",
        "City": "Ghent",
        "CountryCode": "BE",
        "Contact": "",
        "ContactLastName": "",
        "VATNumber": "HIDDEN",
        "LastModified": "2024-03-10T15:00:49.487",
        "Created": "2024-03-10T13:55:42.723",
        "VATLiable": true,
        "Language": "EN",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [],
        "DefaultPaid": false,
        "DisplayName": "Billit",
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "GLN",\
                "Identifier": "5430003732007",\
                "SchemeID": "0088"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR"
    },
    "OrderDate": "2024-01-01T00:00:00",
    "ExpiryDate": "2024-01-31T00:00:00",
    "OrderType": "Invoice",
    "LastModified": "2024-03-10T15:00:49.72",
    "Created": "2024-03-10T15:00:49.533",
    "OrderDirection": "Income",
    "OrderLines": [\
        {\
            "Quantity": 1.00000,\
            "UnitPriceExcl": 10.00000,\
            "Description": "Box of cookies",\
            "TotalExcl": 10.00,\
            "TotalVAT": 0.60,\
            "VATPercentage": 6.00,\
            "VentilationCode": "2",\
            "CustomFields": {},\
            "InclLeading": false,\
            "TotalIncl": 10.60\
        },\
        {\
            "Quantity": 2.00000,\
            "UnitPriceExcl": 3.75000,\
            "Description": "Sticks",\
            "TotalExcl": 7.50,\
            "TotalVAT": 1.58,\
            "VATPercentage": 21.00,\
            "VentilationCode": "4",\
            "CustomFields": {},\
            "InclLeading": false,\
            "TotalIncl": 9.08\
        }\
    ],
    "PaymentDiscountPercentage": 0.00,
    "PaymentDiscountAmount": 0.00,
    "VatGroups": [\
        {\
            "VentilationCode": "2",\
            "VATPercentage": 6.00,\
            "TotalExcl": 10.00,\
            "TotalVAT": 0.60,\
            "TotalIncl": 10.60,\
            "Mtvh": 10.00,\
            "FinancialReductionAmount": 0.00\
        },\
        {\
            "VentilationCode": "4",\
            "VATPercentage": 21.00,\
            "TotalExcl": 7.50,\
            "TotalVAT": 1.58,\
            "TotalIncl": 9.08,\
            "Mtvh": 7.50,\
            "FinancialReductionAmount": 0.00\
        }\
    ],
    "VentilationCode": "4",
    "TotalExcl": 17.50,
    "TotalIncl": 19.68,
    "TotalVAT": 2.18,
    "Tags": [],
    "PaymentReference": "+++001/1800/63503+++",
    "Paid": false,
    "ExternalProvider": "APIFeed",
    "ExternalProviderReferences": [],
    "Currency": "EUR",
    "IsSent": false,
    "Invoiced": false,
    "CustomFields": {},
    "RemindersSent": 0,
    "ToPay": 19.68,
    "OrderStatus": "ToSend",
    "Overdue": true,
    "DaysOverdue": 39,
    "FXRateToForeign": 1.00000,
    "DeliveryDate": "2024-01-01T00:00:00",
    "PaymentLinks": [\
        {\
            "ClickUrl": "",\
            "QRImageUrl": "HIDDEN"\
        }\
    ],
    "AccountantVerificationNeeded": false,
    "CurrentDocumentDeliveryDetails": {
        "IsDocumentDelivered": false
    },
    "Messages": []
}
```

- [Retrieve List of invoices](retrieve-list-of-invoices.md)
- [Get Status Info of a Sales Invoice](status-content-of-a-sales-invoice.md)
- [Get Files](get-files.md)
- [IMR : More Information](imr.md)
- [Webhooks for pushing e-invoice statuses](retrieving-your-first-e-invoice-statuses.md)

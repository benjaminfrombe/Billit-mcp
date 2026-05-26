---
title: "Retrieve List of invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/retrieve-list-of-invoices"
source_slug: "retrieve-list-of-invoices"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - retrieve
  - list
---

# Retrieve List of invoices

Because you sometimes want to query on lists of invoices or retrieve purchase invoice which you do not already have a unique ID for we have our list API endpoint. This endpoint also returns a order object but less properties and it will be contained in a list (multiple).

We allow Odata queries to be ran on top of the endpoint giving you more freedom to already provide us some queries which will filter the response. More info about Odata can be found here -> [Odata Info](odata.md)

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders | GET | List of Orders |
| /v1/orders?$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Income' | GET | With Odata |

Below results of the first document of the list. The list does not contain all data, but a summary.

JSON

```json
{
    "Items": [\
        {\
            "OrderID": 125478,\
            "CompanyID": HIDDEN,\
            "OrderPDF": {\
                "FileID": "c1cd2bfa-3678-42dd-99f3-2f6d323bd2fc"\
            },\
            "OrderNumber": "QS-001",\
            "CounterParty": {\
                "PartyID": 125999,\
                "Addresses": [],\
                "Street": "Oktrooiplein",\
                "StreetNumber": "1",\
                "Box": "301",\
                "City": "Ghent",\
                "CountryCode": "BE",\
                "VATNumber": "BE0563846944",\
                "PartyType": "Customer",\
                "VATLiable": true,\
                "DisplayName": "Billit",\
                "VATDeductable": true,\
                "Identifiers": [\
                    {\
                        "IdentifierType": "GLN",\
                        "Identifier": "5430003732007"\
                    }\
                ]\
            },\
            "OrderDate": "2024-01-01T00:00:00",\
            "ExpiryDate": "2024-01-31T00:00:00",\
            "OrderType": "Invoice",\
            "LastModified": "2024-03-10T15:00:49.72",\
            "Created": "2024-03-10T15:00:49.533",\
            "OrderDirection": "Income",\
            "TotalExcl": 17.50,\
            "TotalIncl": 19.68,\
            "TotalVAT": 2.18,\
            "PaymentReference": "+++001/1800/63503+++",\
            "Paid": false,\
            "ExternalProvider": "APIFeed",\
            "Currency": "EUR",\
            "IsSent": false,\
            "Invoiced": false,\
            "RemindersSent": 0,\
            "ToPay": 19.68,\
            "OrderStatus": "ToSend",\
            "Overdue": true,\
            "DaysOverdue": 39,\
            "FXRateToForeign": 1.00000,\
            "DeliveryDate": "2024-01-01T00:00:00",\
            "ExportedToConnector": false,\
            "CurrentDocumentDeliveryDetails": {\
                "IsDocumentDelivered": false\
            }\
        }\
    ]
}
```

Updated6 months ago

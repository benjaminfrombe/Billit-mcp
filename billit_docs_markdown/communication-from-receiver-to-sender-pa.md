---
title: "Messages and Status"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/communication-from-receiver-to-sender-pa"
source_slug: "communication-from-receiver-to-sender-pa"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - communication
  - receiver
  - sender
  - pa
  - messages
---

## Which Parties can Send Statusses

Messages can be returned to the sender

- from French Tax Authority (government)
- from the receiver or from the PA-partner of the receiver.

Optional/Mandatory

- Some messages are mandatory, many are optional.
- When a Billit sender receivers messages, all messages will be stored and displayed in Billit.

## Status and Messages in MyBillit User Interface

Billit will display all the messages in the messages section.

Below : example of a positive scenario: French Tax Authority Accepted the invoice and Invoice has been delivered on the Peppol network:

![](https://files.readme.io/c823eaeb3cdcbb81ae68af89bca52573838adf86d495547e814bcd9cef28d5a1-2026-05-07_11-26-09.png)

Extra info about the messages:

1. Invoice has been sent. Click on link when to download the XML file sent via the network. Sending will happen +/- 1 hour after the Exchange with French Tax Authority.
2. Endpoint of the customer.
3. Peppol proof of delivery file.
4. Communication with French Tax Authority (PPF). The message files can be downloaded.
5. Feedback message(s) from the customer (optional).

Below example of a negative scenario : refusal by the French Tax Authority:

![](https://files.readme.io/d7076f83d35fb03c308728012b8be926de9af1b8929eb5f461020a17a5700b9e-2026-05-19_15-31-26.png)

Info:

1. Reporting Failed : Invoice will not be delivered via Open/Peppol
2. Feedback XML file from French Government : does contain rejection information

## Get Feedback via API

See general API documentation : [https://docs.billit.be/docs/retrieve-invoice-information](retrieve-invoice-info-and-status.md)

When asking for information via API GET, the fields to look at are:

| API Feedback Content | Reporting OK | Reporting Error |
| --- | --- | --- |
| CurrentDocumentDeliveryDetails/IsDocumentDelivered | true | false |
| CurrentDocumentDeliveryDetails/IsDocumentDocumentDeliveryStatus | Delivered | Pending |
| TaxReportingStatusTC | Done | Failed |

Sample files:

GET Invoice (Approved French Tax Authority)GET Invoice (Rejected French Tax Authority)

```json
{
    "OrderID": 2637999,
    "CompanyID": 865999,
    "OrderPDF": {
        "FileID": "f8dd5e9d-0aee-4b05-86fe-47a75b550999",
        "FileName": "Facture_00004_TestcustomerPPFReject.pdf"
    },
    "Attachments": [],
    "OrderNumber": "00008",
     "Customer": {
        "PartyID": 1092999,
        "Nr": "1",
        "Name": "Test customer PPF Reject",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "Test customer error from PPF",\
                "StreetNumber": "1",\
                "Zipcode": "75001",\
                "City": "Paris",\
                "CountryCode": "FR"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "Test customer error from PPF",\
                "StreetNumber": "1",\
                "Zipcode": "75001",\
                "City": "Paris",\
                "CountryCode": "FR"\
            }\
        ],
        "StreetNumber": "1",
        "Zipcode": "75001",
        "City": "Paris",
        "CountryCode": "FR",
        "Contact": "",
        "VATNumber": "FR34532578572",
        "LastModified": "2026-05-18T13:24:32.047",
        "Created": "2026-05-18T12:00:03.12",
        "PartyType": "Customer",
        "VATLiable": true,
        "Language": "FR",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [],
        "Users": [],
        "DefaultPaid": false,
        "DisplayName": "Test customer PPF Reject",
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "CTC",\
                "Identifier": "227010068_ERROR",\
                "SchemeID": "0225",\
                "Preferred": false,\
                "IdentifierAddress": "0225:227010068_ERROR"\
            },\
            {\
                "IdentifierType": "SIRENE",\
                "Identifier": "34532578572",\
                "SchemeID": "0002",\
                "Preferred": false,\
                "IdentifierAddress": "0002:34532578572"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR",
        "SendUBL": true,
        "SendPDF": true
    },
    "Supplier": {
        "PartyID": 865999,
        "Name": "Test supplier",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Street": "Rue test",\
                "StreetNumber": "29",\
                "Zipcode": "59760",\
                "City": "Grande-Synthe",\
                "CountryCode": "FR",\
                "Phone": "+33235723999"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Street": "Rue test",\
                "StreetNumber": "27",\
                "Zipcode": "59760",\
                "City": "Grande-Synthe",\
                "CountryCode": "FR",\
                "Phone": "+33235723999"\
            }\
        ],
        "Street": "Rue test",
        "StreetNumber": "29",
        "Zipcode": "59760",
        "City": "Grande-Synthe",
        "CountryCode": "FR",
        "IBAN": "FR7616706050925401337319999",
        "BIC": "AGRIFRPP867",
        "Phone": "+33235723415",
        "Email": "test.user@email.com",
        "Contact": "",
        "VATNumber": "FR27570501999",
        "LastModified": "2026-05-18T11:29:33.803",
        "Created": "2025-11-28T17:18:39.683",
        "PartyType": "Supplier",
        "VATLiable": true,
        "Language": "FR",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [\
            {\
                "IBAN": "FR7616706050925401337319999",\
                "BIC": "AGRIFRPP867",\
                "Currency": "EUR",\
                "Verified": false,\
                "Saldo": 0.00\
            }\
        ],
        "Users": [],
        "DefaultPaid": false,
        "DisplayName": "Test Company",
        "FinancialReductionDaysDefault": 8,
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "SIRENE",\
                "Identifier": "570501999",\
                "SchemeID": "0002",\
                "Preferred": false,\
                "IdentifierAddress": "0002:570501916"\
            },\
            {\
                "IdentifierType": "VAT",\
                "Identifier": "FR27570501999",\
                "SchemeID": "9957",\
                "Preferred": false,\
                "IdentifierAddress": "9957:FR27570501999"\
            },\
            {\
                "IdentifierType": "CTC",\
                "Identifier": "570501916_TEST",\
                "SchemeID": "0225",\
                "Preferred": false,\
                "IdentifierAddress": "0225:570501999"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR",
        "SendUBL": true,
        "SendPDF": true
    },

    "OrderDate": "2026-05-19T00:00:00",
    "ExpiryDate": "2026-06-18T00:00:00",
    "OrderType": "Invoice",
    "LastModified": "2026-05-19T08:24:28.297",
    "Created": "2026-05-19T08:12:19.243",
    "OrderDirection": "Income",
    "OrderLines": [\
        {\
            "OrderLineID": 20506599,\
            "Quantity": 1.00000,\
            "UnitPriceExcl": 1.05000,\
            "Description": "test",\
            "TotalExcl": 1.05,\
            "TotalVAT": 0.21,\
            "VATPercentage": 20.00,\
            "VentilationCode": "4",\
            "CustomFields": {},\
            "InclLeading": false,\
            "TotalIncl": 1.26\
        }\
    ],
    "PaymentDiscountPercentage": 0.00,
    "PaymentDiscountAmount": 0.00,
    "VatGroups": [\
        {\
            "VentilationCode": "4",\
            "VATPercentage": 20.00,\
            "TotalExcl": 1.05,\
            "TotalVAT": 0.21,\
            "TotalIncl": 1.26,\
            "Mtvh": 1.05,\
            "FinancialReductionAmount": 0.00\
        }\
    ],
    "VentilationCode": "4",
    "TotalExcl": 1.05,
    "TotalIncl": 1.26,
    "TotalVAT": 0.21,
    "Tags": [],
    "PaymentReference": "+++000/0863/65968+++",
    "Paid": false,
    "ExternalProviderReferences": [],
    "Currency": "EUR",
    "IsSent": true,
    "Invoiced": false,
    "CustomFields": {},
    "RemindersSent": 0,
    "ToPay": 1.26,
    "OrderStatus": "ToPay",
    "Overdue": false,
    "DaysOverdue": -30,
    "FXRateToForeign": 1.00000,
    "DeliveryDate": "2026-05-19T00:00:00",

    "AccountantVerificationNeeded": false,
    "CurrentDocumentDeliveryDetails": {
        "DocumentDeliveryDate": "2026-05-19T08:13:33.383",
        "DocumentDeliveryInfo": "Received",
        "IsDocumentDelivered": true,
        "DocumentDeliveryStatus": "Delivered"
    },
    "Messages": [\
        {\
            "FileID": "6a1bf464-5f86-474e-8679-7faed6879fd4",\
            "CreationDate": "2026-05-19T08:12:23.087",\
            "TransportType": "Peppol",\
            "Success": true,\
            "Trials": 1,\
            "Destination": "0225:127362116_DEMO",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "FFE0614A",\
            "FileID": "1865d9fb-fcea-4e1b-9713-d78846eea93e",\
            "CreationDate": "2026-05-19T08:13:28.383",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "CFE0614A",\
            "FileID": "5b1be28c-0018-4a3a-89ae-16c090ddc4ef",\
            "CreationDate": "2026-05-19T08:13:29.383",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "FFE0111A",\
            "FileID": "59383f44-fc42-4921-9598-2cb6b3c8de16",\
            "CreationDate": "2026-05-19T08:13:30.383",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "CFE0111A",\
            "FileID": "80963e6c-a17d-45e1-8b7c-cc1d6e969555",\
            "CreationDate": "2026-05-19T08:13:31.383",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "ack",\
            "FileID": "4d399799-bde3-4887-ac6a-199670bb7068",\
            "CreationDate": "2026-05-19T08:13:32.383",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "AB: The document has been successfully received.",\
            "FileID": "8aae4fb8-200b-4688-8daa-93d17e5a29b7",\
            "CreationDate": "2026-05-19T08:24:28.297",\
            "TransportType": "Peppol",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "0225:127362116_DEMO",\
            "MessageDirection": "Incoming"\
        }\
    ],
    "TaxReportingStatusTC": "Done"
}
```

```json
{
    "OrderID": 2637999,
    "CompanyID": 865999,
    "OrderPDF": {
        "FileID": "f8dd5e9d-0aee-4b05-86fe-47a75b550999",
        "FileName": "Facture_00004_TestcustomerPPFReject.pdf"
    },
    "Attachments": [],
    "OrderNumber": "00004",
    "Customer": {
        "PartyID": 1092999,
        "Nr": "1",
        "Name": "Test customer PPF Reject",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "Test customer error from PPF",\
                "StreetNumber": "1",\
                "Zipcode": "75001",\
                "City": "Paris",\
                "CountryCode": "FR"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Name": "Test customer error from PPF",\
                "StreetNumber": "1",\
                "Zipcode": "75001",\
                "City": "Paris",\
                "CountryCode": "FR"\
            }\
        ],
        "StreetNumber": "1",
        "Zipcode": "75001",
        "City": "Paris",
        "CountryCode": "FR",
        "Contact": "",
        "VATNumber": "FR34532578572",
        "LastModified": "2026-05-18T13:24:32.047",
        "Created": "2026-05-18T12:00:03.12",
        "PartyType": "Customer",
        "VATLiable": true,
        "Language": "FR",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [],
        "Users": [],
        "DefaultPaid": false,
        "DisplayName": "Test customer PPF Reject",
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "CTC",\
                "Identifier": "227010068_ERROR",\
                "SchemeID": "0225",\
                "Preferred": false,\
                "IdentifierAddress": "0225:227010068_ERROR"\
            },\
            {\
                "IdentifierType": "SIRENE",\
                "Identifier": "34532578572",\
                "SchemeID": "0002",\
                "Preferred": false,\
                "IdentifierAddress": "0002:34532578572"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR",
        "SendUBL": true,
        "SendPDF": true
    },
    "Supplier": {
        "PartyID": 865999,
        "Name": "Test supplier",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Street": "Rue test",\
                "StreetNumber": "29",\
                "Zipcode": "59760",\
                "City": "Grande-Synthe",\
                "CountryCode": "FR",\
                "Phone": "+33235723999"\
            },\
            {\
                "AddressType": "DeliveryAddress",\
                "Street": "Rue test",\
                "StreetNumber": "27",\
                "Zipcode": "59760",\
                "City": "Grande-Synthe",\
                "CountryCode": "FR",\
                "Phone": "+33235723999"\
            }\
        ],
        "Street": "Rue test",
        "StreetNumber": "29",
        "Zipcode": "59760",
        "City": "Grande-Synthe",
        "CountryCode": "FR",
        "IBAN": "FR7616706050925401337319999",
        "BIC": "AGRIFRPP867",
        "Phone": "+33235723415",
        "Email": "test.user@email.com",
        "Contact": "",
        "VATNumber": "FR27570501999",
        "LastModified": "2026-05-18T11:29:33.803",
        "Created": "2025-11-28T17:18:39.683",
        "PartyType": "Supplier",
        "VATLiable": true,
        "Language": "FR",
        "VentilationCode": "4",
        "CustomFields": [],
        "BankAccounts": [\
            {\
                "IBAN": "FR7616706050925401337319999",\
                "BIC": "AGRIFRPP867",\
                "Currency": "EUR",\
                "Verified": false,\
                "Saldo": 0.00\
            }\
        ],
        "Users": [],
        "DefaultPaid": false,
        "DisplayName": "Test Company",
        "FinancialReductionDaysDefault": 8,
        "DefaultExpiryOffset": 30,
        "GLDefaultExpiryOffset": 30,
        "VATDeductable": true,
        "DefaultReductionPercentage": 0.00,
        "Identifiers": [\
            {\
                "IdentifierType": "SIRENE",\
                "Identifier": "570501999",\
                "SchemeID": "0002",\
                "Preferred": false,\
                "IdentifierAddress": "0002:570501916"\
            },\
            {\
                "IdentifierType": "VAT",\
                "Identifier": "FR27570501999",\
                "SchemeID": "9957",\
                "Preferred": false,\
                "IdentifierAddress": "9957:FR27570501999"\
            },\
            {\
                "IdentifierType": "CTC",\
                "Identifier": "570501916_TEST",\
                "SchemeID": "0225",\
                "Preferred": false,\
                "IdentifierAddress": "0225:570501999"\
            }\
        ],
        "SmallEnterprise": false,
        "DefaultCurrencyTC": "EUR",
        "SendUBL": true,
        "SendPDF": true
    },
    "OrderDate": "2026-05-18T00:00:00",
    "ExpiryDate": "2026-06-17T00:00:00",
    "OrderType": "Invoice",
    "LastModified": "2026-05-18T13:29:32.977",
    "Created": "2026-05-18T13:28:17.143",
    "OrderDirection": "Income",
    "OrderLines": [\
        {\
            "OrderLineID": 20490135,\
            "Quantity": 1.00000,\
            "UnitPriceExcl": 1.01000,\
            "Description": "test",\
            "TotalExcl": 1.01,\
            "TotalVAT": 0.20,\
            "VATPercentage": 20.00,\
            "VentilationCode": "4",\
            "CustomFields": {},\
            "InclLeading": false,\
            "TotalIncl": 1.21\
        }\
    ],
    "PaymentDiscountPercentage": 0.00,
    "PaymentDiscountAmount": 0.00,
    "VatGroups": [\
        {\
            "VentilationCode": "4",\
            "VATPercentage": 20.00,\
            "TotalExcl": 1.01,\
            "TotalVAT": 0.20,\
            "TotalIncl": 1.21,\
            "Mtvh": 1.01,\
            "FinancialReductionAmount": 0.00\
        }\
    ],
    "VentilationCode": "4",
    "TotalExcl": 1.01,
    "TotalIncl": 1.21,
    "TotalVAT": 0.20,
    "Tags": [],
    "PaymentReference": "+++000/0455/57999+++",
    "Paid": false,
    "ExternalProviderReferences": [],
    "Currency": "EUR",
    "IsSent": true,
    "Invoiced": false,
    "CustomFields": {},
    "RemindersSent": 0,
    "ToPay": 1.21,
    "OrderStatus": "ToPay",
    "Overdue": false,
    "DaysOverdue": -29,
    "FXRateToForeign": 1.00000,
    "DeliveryDate": "2026-05-18T00:00:00",
    "AccountantVerificationNeeded": false,
    "CurrentDocumentDeliveryDetails": {
        "IsDocumentDelivered": false,  // Rejected by French Authority, not delivered to customer
        "DocumentDeliveryStatus": "Pending"
    },
    "Messages": [\
        {\
            "Description": "Reporting failed",\
            "CreationDate": "2026-05-18T13:28:20.72",\
            "TransportType": "Peppol",\
            "Success": false,\
            "Trials": 1,\
            "Destination": "0225:227010068_ERROR",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "FFE0614A",\
            "FileID": "2f8f4ab9-fe77-4a30-89b8-1e1634bb0a2f",\
            "CreationDate": "2026-05-18T13:29:33.07",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "CFE0614A",\
            "FileID": "522876ae-2626-4ee1-9494-1d1b76b37221",\
            "CreationDate": "2026-05-18T13:29:34.07",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "FFE0111A",\
            "FileID": "7a3d84ab-fcf0-48a8-9bab-0e89c18df452",\
            "CreationDate": "2026-05-18T13:29:35.07",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "CFE0111A",\
            "FileID": "c0ba7b51-85af-41c5-8eda-ad579a847a82",\
            "CreationDate": "2026-05-18T13:29:36.07",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "ack",\
            "FileID": "660a861e-e240-4cab-b87c-962ece5d859d",\
            "CreationDate": "2026-05-18T13:29:37.07",\
            "TransportType": "FrenchTaxAuthority",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "FrenchTaxAuthority",\
            "MessageDirection": "Incoming"\
        }\
    ],
    "TaxReportingStatusTC": "Failed"
}
```

In the final Feedback file of the French Tax Authority the a SpecifiedDocumentStatus is available.

| Status | Final XML File |
| --- | --- |
| Invoice Approved by French Tax Authority | no SpecifiedDocumentStatus in XML |
| Invoice Rejected by French Tax Authority | SpecifiedDocumentStatus in XML contains the error |

Below example for reject:

Final Feedback Rejected Tax Authority

```xml
      <ram:SpecifiedDocumentStatus>
        <ram:ReasonCode>REJ_UNI</ram:ReasonCode>
        <ram:SequenceNumeric>1</ram:SequenceNumeric>// First Remark
        <ram:IncludedNote>
          <ram:ContentCode>G1.45</ram:ContentCode>
          <ram:Content>Échec du contrôle de l'unicité du F1.</ram:Content> // Text description about error 1
          <ram:SubjectCode>BT-1, BT-2, BT-30</ram:SubjectCode>  // Error related to Business Terms
        </ram:IncludedNote>
      </ram:SpecifiedDocumentStatus>
      <ram:SpecifiedDocumentStatus>
        <ram:ReasonCode>REJ_SEMAN</ram:ReasonCode>
        <ram:SequenceNumeric>2</ram:SequenceNumeric>// Second Remark
        <ram:IncludedNote>
          <ram:ContentCode>G1.05</ram:ContentCode>
          <ram:Content>L'identifiant de la facture BT-1 ne respecte pas le format attendu.</ram:Content>
          <ram:SubjectCode>BT-1</ram:SubjectCode> // Error related to Business Terms
        </ram:IncludedNote>
      </ram:SpecifiedDocumentStatus>
```

## Communication Messages when there are no Issues with Invoice

**Minimum Flow of Status Messages (Mandatory Messages)**

- From Invoice Receiver to the Billit Invoice Sender : no mandatory Message (only optional messages, Billit will not send the optional messages).
- From Billit Invoice Sender to Invoice Receiver : 1 message : 212 Payment Received

![](https://files.readme.io/7d6f6daa71a6d2fac1f4958799fcf5fdd9158ed5c64bfe07084239e07b492eee-2026-03-27_11-05-21.png)

**Maximum Number of Positive Messages (Including Optional) that you can receive when sending sales invoices via Billit (positive scenario)**

![](https://files.readme.io/a90f7d1b173269f95b343aa1ed592adedbc785a829dc1e39e4bacbfd5e5ac28f-2026-03-27_11-17-59.png)

## Messages when more Information is Requested

When you are sending sales invoices via Billit, you might receive the following messages from the receiver:

Communications Overview:

| What | Format | PA Message Number |
| --- | --- | --- |
| Request more info | PA Message | 208 |
| Deliver more info | Outside PA (e.g. email) |  |
| Confirm : info received, information gathering is complete | PA Message | 209 |

Flow of possible PA Messages for more information :

![](https://files.readme.io/04a84d7b5b2746eb4fcd63dc7d46dc8bcaf436aa815a4e5f967720b398f033ad-2026-03-27_11-23-46.png)

## Communication when there are no Issues with Invoice

When you are sending sales invoices via Billit, you might receive the following optional information from the receiver:

- From Invoice Receiver to Invoice Sender : no mandatory Message
- From Invoice Sender to Invoice Receiver : 1 message : 212 Payment Received (Mandatory)

![](https://files.readme.io/7d6f6daa71a6d2fac1f4958799fcf5fdd9158ed5c64bfe07084239e07b492eee-2026-03-27_11-05-21.png)

## Communication in case of Issues with Invoice

When you are sending sales invoices via Billit, you might receive the following negative information from the receiver:

About the messages in case of issues:

![](https://files.readme.io/e2ffa2d6eb3c98e1ebe707c39014af004cfdc71c1cf678302e23f505110e326a-2026-05-18_11-19-14.png)

| PA Message Number | Coming From | What | Type of Status |
| --- | --- | --- | --- |
| 501 | PPF | The content and flow has been controlled by PPF, but is not accepted (Non Recevable) | Final |
| 213 | Service Providers | Rejected in platform (technical or business rejection) | Final |
| 207 | Receiver | In dispute : does not agree with a part or the total. This is an intermediate message, not a final status | Intermediary |
| 210 | Receiver | Refused by Receiver : the receiver rejects the complete invoice. | Final |

## Global Overview of the statuses when sending Invoices

About the statuses:

- Mandatory / Optional :
  - only a few of the 14 statuses are mandatory
  - only 1 of the 4 mandatory statuses has to be initiated by the seller/supplier (payment received)
- Message from:
  - Indicating who is the initiator of the message
  - Only one message has to be launched by the seller/supplier

Main functional statuses you might receive via Billit when sending invoices via Billit to the Customer:

| Status | Description | M/O | Action Supplier? | Message from |
| --- | --- | --- | --- | --- |
| 200 | Submitted with success (to Billit, to PPF) | **Mandatory** | No | Billit |
| 201 | Billit transmitted to the receiver | Optional | No | Billit |
| 202 | Service provider of receiver has received | Optional | No | Service provider receiver |
| 203 | Service provider of receiver has submitted to the receiver | Optional | No | Service provider receiver |
| 204 | Receipt confirmation by the receiver | Optional | No | Receiver |
| 205 | Receiver has approved | Optional | No | Receiver |
| 206 | Receiver has partially approved | Optional | No | Receiver |
| 207 | In dispute : does not agree with a part or the total | Optional | **Yes** | Receiver |
| 208 | Suspended : receiver requires more information | Optional | **Yes** | Receiver |
| 212 | Paid (supplier) : the supplier confirms that the payment is received (complete amount or partial amount) | **Mandatory** | **Yes** | Supplier |
| 213 | Rejected in platform (message coming from service providers) | **Mandatory** | **yes** | Service Provider |

Other statuses:

| Status | Description | Message From |
| --- | --- | --- |
| 250 | Reception (technical acknowledgement before validation) | PPF, Service Provider Buyer |
| 200 | Validation ok (basic compliance : ready for further processing) | PPF (Gov) |
| 280 | Routing / Processing / Transmitted | PPF (Gov) |
| 281 | Delivered to the next step (Recipient can access it) | PPF (Gov) |
| 500 | Rejection = blocking error. Typically invalid or missing data, incorrect identifiers. Can happen after 250 and 200. | PPF (Gov) |

---
title: "Get the Inbox List for Supplier Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/get-supplier-invoices-and-responses-from-sales-invoices"
source_slug: "get-supplier-invoices-and-responses-from-sales-invoices"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - get
  - supplier
  - invoices
  - responses
  - sales
  - inbox
  - list
---

## About IMR/MLR and the Inbox

Endpoint to use:

| Information Element | Info |
| --- | --- |
| GET Command on Sandbox | GET [https://api.sandbox.billit.be/v1/peppol/inbox](https://api.sandbox.billit.be/v1/peppol/inbox) |
| GET Command on Production | GET [https://api.billit.be/v1/peppol/inbox](https://api.billit.be/v1/peppol/inbox) |
| Include Party and Secret key in the header | More info : [https://docs.billit.be/docs/authentication](authentication.md) |

Via the GET Peppol inbox, a list of documents can be retrieved.

About the list of documents:

- max. 10 documents
- consists of the oldest documents
- Odata filtering is not supported.

Type of files that can occur in the list:

- Incoming invoices and incoming credit notes (supplier related),
- Feedback from receivers on the delivered sales invoices (sales - income related). The feedback can consist of:
  - (Invoice Responses = IMR)
  - Message Level Responses or MLR

## IMR and MLR Concept and Use

| Type | Value (example) | Sample value |
| --- | --- | --- |
| InboxItemID | the ID to perform a Get as a next step to get the file | 69791 |
| SenderPeppolID | identifier and value of the Sender | "0208:0759529999" |
| PeppolDocumentType | This indicates that it is an Invoice, a credit note, and IMR and MLR. In this example it is an Invoice. | "urn:oasis:names:specification:ubl:schema: xsd:Invoice-2:: Invoice##urn:cen.eu:en16931:2017compliant#urn: fdc:peppol.eu:2017:poacc:billing:3.0::2.1" |
| ReceiverPeppolID | identifier type and value of the Receiver | "9925:BE0437295999" |
| ReceiverCompanyID | value for the receiver company | "BE0437295999" |
| CreationDate | Date and time when it was received at Billit | "2025-04-07T13:30:32.1327398" |
| PeppolFileID | with this fileID the file can be obtained with a separate call | "8758f630-1fbe-478c-b872-77f5652e2999 |

## Inbox Result Sample

Below an Example of a result with 1 incoming supplier invoice, 1 incoming supplier credit note and 1 incoming IMR - Invoice Response (feedback from receiver of your sales invoice):

Inbox list

```json
{
    "InboxItems": [\
        {\
            "InboxItemID": 69791,\
            "SenderPeppolID": "0208:0759529202",\
            "PeppolDocumentType": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "ReceiverPeppolID": "9925:BE0437295999",\
            "ReceiverCompanyID": "BE0437295999",\
            "CreationDate": "2025-04-07T13:30:32.1327398",\
            "PeppolFileID": "b155ec2e-a74c-4972-928b-f87d6056f999"\
        },\
        {\
            "InboxItemID": 69848,\
            "SenderPeppolID": "0208:0759529202",\
            "PeppolDocumentType": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "ReceiverPeppolID": "9925:BE0437295999",\
            "ReceiverCompanyID": "BE0437295999",\
            "CreationDate": "2025-04-08T22:30:39.1691603",\
            "PeppolFileID": "b67e0285-39d9-4420-b99b-e2170b9dc999"\
        },\
        {\
            "InboxItemID": 69854,\
            "SenderPeppolID": "9925:BE0759529999",\
            "PeppolDocumentType": "IMR",\
            "ReceiverPeppolID": "0208:0437295999",\
            "ReceiverCompanyID": "BE0437295999",\
            "CreationDate": "2025-04-08T22:31:39.544541",\
            "PeppolFileID": "8758f630-1fbe-478c-b872-77f5652e2999"\
        },\
    ]
}
```

Updated8 months ago

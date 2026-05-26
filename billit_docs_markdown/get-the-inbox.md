---
title: "Get the Inbox List for IMR and MLR files"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/get-the-inbox"
source_slug: "get-the-inbox"
category: "files-documents"
topics:
  - files
  - documents
  - get
  - inbox
  - list
  - imr
  - mlr
---

## About the Inbox List

Via the GET Peppol inbox (endpoint on sandbox [https://api.sandbox.billit.be/v1/peppol/inbox](https://api.sandbox.billit.be/v1/peppol/inbox) ), the list of incoming files can be retrieved

Type of files that can occur in the list:

- Incoming invoices and incoming credit notes (supplier related) - this is not relevant for sales invoices.
- Feedback from receivers on the delivered sales invoices, this is sales/income related. The feedback can consist of:
  - Invoice Responses = IMR
  - Message Level Responses or MLR

Will you receive IMR and MLR file:

- When you are registered on Open/Peppol via Billit, you are capable to receive IMR/MLR messages.
- An invoice receiver is not have to send an IMR or MLR to the receiver. It is an optional message.

What IMR/MLR file is not?

- It is not a proof of delivery. When you Billit has confirmed that sending was succesful, it is sure and proven that document has been inserted into the Open/Peppol network.

## Meaning of the Fields

Meaning of the Information fields

| Type | Value (example) | Sample value |
| --- | --- | --- |
| InboxItemID | the ID to perform a Get as a next step to get the file | 69791 |
| SenderPeppolID | identifier and value of the Sender | "0208:0759529999" |
| PeppolDocumentType | This indicates that it is an Invoice, a credit note, and IMR and MLR | "IMR" |
| ReceiverPeppolID | identifier type and value of the Receiver | "9925:BE0437295999" |
| ReceiverCompanyID | value for the receiver company | "BE0437295999" |
| CreationDate | Date and time when it was received at Billit | "2025-04-07T13:30:32.1327398" |
| PeppolFileID | with this fileID the file can be obtained with a separate call | "8758f630-1fbe-478c-b872-77f5652e2999" |

Specific remarks:

- It is a list of files, Odata filtering on that list is not supported.
- The list displays maximum 10 entries (the oldest files).

## Example

Below an Example of a result with 4 incoming IMR - Invoice Response files (feedback from receiver related to your sales invoice):

Inbox list

```json
{
    "InboxItems": [\
        {\
            "InboxItemID": 69873,\
            "SenderPeppolID": "9925:BE0759529202",\
            "PeppolDocumentType": "IMR",\
            "ReceiverPeppolID": "0208:0437295202",\
            "ReceiverCompanyID": "BE0437295202",\
            "CreationDate": "2025-04-09T09:02:10.0168981",\
            "PeppolFileID": "cc41ebf6-974c-4f32-8ef2-04d78836d999"\
        },\
        {\
            "InboxItemID": 69886,\
            "SenderPeppolID": "9925:BE0759529202",\
            "PeppolDocumentType": "IMR",\
            "ReceiverPeppolID": "0208:0437295202",\
            "ReceiverCompanyID": "BE0437295202",\
            "CreationDate": "2025-04-09T09:03:09.9704004",\
            "PeppolFileID": "2ab35770-7f44-43be-8fc8-ea3c724e7999"\
        },\
        {\
            "InboxItemID": 69887,\
            "SenderPeppolID": "9925:BE0759529202",\
            "PeppolDocumentType": "IMR",\
            "ReceiverPeppolID": "0208:0437295202",\
            "ReceiverCompanyID": "BE0437295202",\
            "CreationDate": "2025-04-09T09:03:09.9546929",\
            "PeppolFileID": "6814ff29-ae4c-47a0-a9b6-478da2ee3999"\
        },\
        {\
            "InboxItemID": 69888,\
            "SenderPeppolID": "9925:BE0759529202",\
            "PeppolDocumentType": "IMR",\
            "ReceiverPeppolID": "0208:0437295202",\
            "ReceiverCompanyID": "BE0437295202",\
            "CreationDate": "2025-04-09T09:03:41.0017427",\
            "PeppolFileID": "c4be227d-6415-44ed-bf13-048bfd95b999"\
        }\
    ]
}
```

Updated8 months ago

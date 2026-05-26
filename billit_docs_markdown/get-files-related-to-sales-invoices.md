---
title: "Get Files"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/get-files-related-to-sales-invoices"
source_slug: "get-files-related-to-sales-invoices"
category: "files-documents"
topics:
  - files
  - documents
  - get
  - related
  - sales
  - invoices
---

## What Files can be retrieved ?

| File Content | Via API | On MyBillit User Interface |
| --- | --- | --- |
| Main PDF file (PDF invoice) | x | x |
| Optional additional attachments (PDF or other) | x | x |
| File delivered in the network (e.g. UBL file via Peppol). Files must have been sent with success before you can retrieve it. | x | x |
| IMR and MLR files (can be multiple, as IMR/MLR is optional can be 0) | x | x |
| Evidence file (Proof of delivery) | - | x |

## References to the Files

When executing the GET v1/order command, you also get information about the available files.

**Examples of available files:**

1\. PDF Attachments (1)2\. PDF Attachments (3)3\. PDF and Excel Attachment4\. Messages (UBL/IMR/MLR)

```json
 "OrderPDF": {
        "FileID": "db40c68c-2ff2-4989-b7d9-6baa1aedff1c",
        "FileName": "Invoice_QS-X014_VILBOXBV.pdf"
    },
    "Attachments": [\
        {\
            "FileID": "130fd171-72ff-4375-a4ce-1c3a4ac3c61c",\
            "FileName": "QS-X014__9_09_2025 8_46_42.json"\
        }\
    ],
```

```json
    "OrderPDF": {
        "FileID": "5b78345f-a107-4a4e-bf5d-293585a49199",
        "FileName": "Invoice_001t038_XYZBV.pdf"
    },
    "Attachments": [\
        {\
            "FileID": "01740d1f-5aef-4765-a3ad-dbef1e199a6f",\
            "FileName": "test attachment2.pdf"\
        },\
        {\
           "FileID": "c1178d8a-f3d2-452b-a339-c6a67b7bbf99",\
          "FileName": "test attachment3.pdf",\
        },\
        {\
           "FileID": "130fd171-72ff-4375-a4ce-1c3a4ac3c61c",\
           "FileName": "QS-X014__9_09_2025 8_46_42.json"\
        }\
    ],
```

```json
    "OrderPDF": {
        "FileID": "75b84e87-acdc-4039-aac1-eebb8184a492",
        "FileName": "QS_001_SalesInvoice.pdf"
    },
    "Attachments": [\
        {\
            "FileID": "c2d6fd1a-2bfc-4031-b03c-5c2ef7b68168",\
            "FileName": "SampleAttachment2.xlsx"\
        },\
        {\
            "FileID": "8c060fb4-e9a3-4ced-97b1-00a9b9feddfd",\
            "FileName": "QS-003PDFAttach8__9_05_2025 16_17_25.json"\
        }\
    ],
```

```json
    "Messages": [\
        {\
            "FileID": "845e4774-7d76-4d2c-a7de-e6d790cb57c6",\
            "CreationDate": "2025-05-07T14:08:07.813",\
            "TransportType": "Peppol",\
            "Success": true,\
            "Trials": 1,\
            "Destination": "0208:0446725877",\
            "MessageDirection": "Outgoing"\
        },\
        {\
            "Description": "AB: The document has been successfully received.",\
            "FileID": "7ee8b70c-3dd7-423a-8269-79f8bc49e0c5",\
            "CreationDate": "2025-05-07T14:09:54.203",\
            "TransportType": "Peppol",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "0208:0446725877",\
            "MessageDirection": "Incoming"\
        },\
        {\
            "Description": "PD: The document has been paid.",\
            "FileID": "b39065a9-8c82-4beb-9c04-010435f4c5fa",\
            "CreationDate": "2025-05-07T14:25:11.427",\
            "TransportType": "Peppol",\
            "Success": true,\
            "Trials": 0,\
            "Destination": "0208:0446725877",\
            "MessageDirection": "Incoming"\
        }\
    ]
}
```

About the 3 examples:

- 1 PDF Attachments (1)
  - OrderPDF : the main PDF
  - Attachment : Json used for Posting the Invoice/CreditNote
- 2 PDF Attachments (3)
  - OrderPDF : the main PDF
  - Attachments :
    - additional PDF attachment,
    - additional PDF attachment,
    - the Json used for Posting the Invoice/CreditNote
- 3 PDF and Excel Attachment
  - OrderPDF : the main PDF
  - Attachments :
    - Excel attachment,
    - the Json used for Posting the Invoice/CreditNote
- 4 Messages (UBL/IMR/MLR)
  - the UBL file sent via the network
  - IMR 1 (AB)
  - IMR 2 (PD)

## How to Get the files?

GET Command of the File

| Endpoint | Method | Response | Extra Info |
| --- | --- | --- | --- |
| /v1/files/FileID | GET | 1 file | Includes full data and file references |

Point of Attention:

- [x]  Your can request 1 file per GET call, so for multiple files you perform multiple gets

Examples of the Result body for a GET File:

PDFXML UBLExcel

```json
{
    "FileID": "57eade47-f402-4605-849b-58c223c6b970",
    "FileName": "140532-206676-9688ab12-2c34-437c-808e-ee279999z99.xml_1.pdf",
    "MimeType": "application/pdf",
    "FileContent": "JVBERi0xLjUKJb662+4KOCAwIG9i................UgL0ltYWdlL1dpZHRoIDUxMi9IZ"
}
```

```text
{
    "FileID": "57eade47-f402-4605-849b-58c223c6b999",
        "FileName": "140532-206676-9688ab12-2c34-437c-808e-ee2793579999.xml",
        "MimeType": "text/xml",
    "FileContent": "JVBERi0xLjUKJb662+4KOCAwIG9i................UgL0ltYWdlL1dpZHRoIDUxMi9IZ"
}
```

```text
{
    "FileID": "57eade47-f402-4605-849b-58c223c9zb999",
    "FileName": "Test Excel 1.xlsx",
    "MimeType": "application/vnd.ms-excel",
    "FileContent": "JVBERi0xLjUKJb662+4KOCAwIG9i................UgL0ltYWdlL1dpZHRoIDUxMi9IZ"
}
```

### How to Process a File from Base64

More info: [https://docs.billit.be/docs/how-can-i-save-a-file](https://docs.billit.be/docs/how-can-i-save-a-file)

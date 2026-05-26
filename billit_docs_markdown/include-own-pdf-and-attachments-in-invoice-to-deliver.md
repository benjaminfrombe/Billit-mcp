---
title: "Include your Own PDF and Attachments"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/include-your-own-pdf-and-attachments"
source_slug: "include-your-own-pdf-and-attachments"
category: "files-documents"
topics:
  - files
  - documents
  - include
  - own
  - pdf
  - attachments
  - invoice
  - deliver
---

## Adding your Own Files when posting to Billit

When you send a document Billit will automatically generate a PDF and include it.

If you prefer to include your own files then this is possible, options:

- Option 1: Just One PDF, no Billit Human readable:
  - Include your own PDF, it will replace the Billit generated PDF.
  - On the User Interface it will be shown as the main document/PDF.
  - Json : in the "OrderPDF" section.
  - Restrictions :
    - you can only include 1 OrderPDF.
    - must be PDF format, encoded (encoding info see below).
- Option 2 Additional Attachments:
  - You can also include one or more additional attachments.
  - This can also be PDF files, or other formats such as Excel, csv. Supported file types are limited.
  - Does not replace the Billit Human Readable.
    - Json : in the "Attachments" section.
- Option 3 : Combined use:
  - Combined Use of the sections "OrderPDF" and "Attachments" is supported

## FileName

In the OrderPDF and Attachment Section following blocks are included:

| Property | Description | Example |
| --- | --- | --- |
| FileName | Contains a filename and a file extension. The file name is free, it refer to the meaning of the attachment. The file extension must be in the supported list (PDF, xls or xlsx, csv). | QS\_001\_SalesInvoice.pdf |
| FileContent | Used to include the Base64 encoded file |  |

## Examples of Files included in the Json body

Below 3 examples:

- Example 1 : One PDF included as "OrderPDF", no Billit human readable will be used
- Example 2:
  - 1 x OrderPDF
  - 1 attachment in "Attachments" section: 1 PDF
- Example 3:
  - 1 x OrderPDF
  - 2 attachment in "Attachments" section:
    - 1 PDF
    - 1 Excel

Below the 3 Examples of Json body. Remark : The encoded FileContent is shorter than normal, to keep the overview.

1 PDF Invoice1 PDF Invoice + 1 PDF Attachment1 PDF Invoice + 1 Excel Attachment

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
        "FileContent": "JVBERi0xLjcNCiW1tbW1DQoxIDAgb.....................cnR4cmVmDQoxOTYxMQ0KJSVFT0Y="
}
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0563846944"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
        "FileContent": "JVBERi0xLjcNCiW1tbW1D2JqDQo8PC9UeXBlL0NhdGFsb2c.........Pg0Kc3RhcnR4cmVmDQoxOTYxMQ0KJSVFT0Y="
    },
     "Attachments": [\
     {\
        "FileName": "SampleAttachment1.pdf",\
        "FileContent": "JVBERi0xLjcNCiW1tbW1.......ZWZTdG0gMTUyNTI+Pg0Kc3RhcnR4cmVmDQoxNjMxNw0KJSVFT0Y="\
    },\
     ],
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0563846944"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

```text
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
        "FileContent": "JVBERi0xLjcNCiW1t1WpIU5........qxXWdXRtv7D/Z9Pje7WeaKneuCN5PH7+eOtn1cHPLjpu715
     "Attachments": [\
     {\
        "FileName": "SampleAttachment2.xlsx",\
        "FileContent": "UEsDBBQABgAIAAAAIQ.........AA0ADQBpAwAA7iI="\
    },\
     ],
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0563846944"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

## Getting files

Endpoints in the Billit API that return files, such as [Order](https://docs.billit.be/reference/order-1), [Document](https://docs.billit.be/reference/document-1) and [File](https://docs.billit.be/reference/file-1).

A File will consist of a FileID, Filename, MimeType and FileContent.

- The FileID can be used to retreive a file from the [File](https://docs.billit.be/reference/file-1) endpoint
- The FileName can be the name
- The MimeType is always in the "type/subtype" form, more info about the types can be found here [Basics of HTTP - MIME\_types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- The FileContent is Base64 encoded

## Sample Code for decoding the Base64 encoding

Example Received document : extractfilecontent as a PDF in C#

C#

```csharp
byte[] PDFDecoded = Convert.FromBase64String(base64Str);

File.WriteAllBytes(@"c:\pdfFromBillit.pdf", PDFDecoded);
```

If you want to manually generate a PDF file as Base64 and include it : Example of a web tool: [https://www.base64encode.net/pdf-to-base64](https://www.base64encode.net/pdf-to-base64).

---
title: "Billit API Source Docs - Include Own PDF And Attachments In Invoice To Deliver"
updated: 2026-05-26
---

# Include own PDF and Attachments in Invoice to Deliver\n\n## Send documents including you own Attachments   [Skip link to Send documents including you own Attachments](https://docs.billit.be/docs/how-can-i-save-a-file\#send-documents-including-you-own-attachments)

When you send a document Billit will automatically generate a PDF and include it.

If you prefer to include your own files then this is possible, options:

- Include your own PDF, it will replace the Billit generated PDF. On the User Interface it will be shown as the main document/PDF.
- You can also include one or more additional attachments. This can also be PDF files, or other formats such as Excel, csv.

Below 3 examples

1 PDF Invoice1 PDF Invoice + 1 PDF Attachment1 PDF Invoice + 1 Excel Attachment

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
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
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
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

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
    },
     "Attachments": [\
     {\
        "FileName": "SampleAttachment1.pdf",\
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
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
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

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-003PDFAttach8",
 "OrderDate": "2025-05-09",
 "ExpiryDate": "2025-06-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
    },
     "Attachments": [\
     {\
        "FileName": "SampleAttachment2.xlsx",\
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
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
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

## Concept   [Skip link to Concept](https://docs.billit.be/docs/how-can-i-save-a-file\#concept)

There's a few endpoints in the Billit API that return files, such as [Order](https://docs.billit.be/reference/order-1), [Document](https://docs.billit.be/reference/document-1) and [File](https://docs.billit.be/reference/file-1).

A File will consist of a FileID, Filename, MimeType and FileContent.

- The FileID can be used to retreive a file from the [File](https://docs.billit.be/reference/file-1) endpoint
- The FileName can be the name
- The MimeType is always in the "type/subtype" form, more info about the types can be found here [Basics of HTTP - MIME\_types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- The FileContent is Base64 encoded

## Sample Code   [Skip link to Sample Code](https://docs.billit.be/docs/how-can-i-save-a-file\#sample-code)

Example Received document : extractfilecontent as a PDF in C#

C#

```\1

byte[] PDFDecoded = Convert.FromBase64String(base64Str);

File.WriteAllBytes(@"c:\pdfFromBillit.pdf", PDFDecoded);

```

If you want to manually generate a PDF file as Base64 and include it : Example of a web tool: [https://www.base64encode.net/pdf-to-base64](https://www.base64encode.net/pdf-to-base64).

Updated21 days ago

* * *

Did this page help you?

Yes

No
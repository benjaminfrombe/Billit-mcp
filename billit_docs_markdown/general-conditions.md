---
title: "General Conditions"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/general-conditions"
source_slug: "general-conditions"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - general
  - conditions
---

# General Conditions

Each supplier has general conditions related to the Invoice. In case of E-invoicing, this can be managed in different ways.

Options when using the API:

- Include a reference in the einvoice that links to your web page with the general conditions
- Include a PDF attachement with the general conditions

About the ability to use the general conditions as PDF attachment in the MyBillit user interface:

- there is an option to store in MyBillit a PDF version of the general conditions
- when you Post invoices with the API, this will not be used
- it can only be used when you manually create an invoice in MyBillit

Link to General ConditionsPDF Attachment for General Conditions

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "Comments": "Our general conditions apply.  They are available on https://companyname.com/generalconditions.html",
 "OrderNumber": "QS-0064587954",
 "OrderDate": "2025-12-09",
 "ExpiryDate": "2025-12-30",
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
        "FileName": "General_Conditions.pdf",\
        "FileContent": "JVBERi0xLjcNCiW1tbW1.......ZWZTdG0gMTUyNTI+Pg0Kc3RhcnR4cmVmDQoxNjMxNw0KJSVFT0Y="\
    },\
     ],
```

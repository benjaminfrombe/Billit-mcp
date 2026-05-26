---
title: "Extra Fields : Extend Content (Header)"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support"
source_slug: "how-can-i-add-certain-peppol-values-that-billit-json-does-not-support"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - add
  - certain
  - values
  - that
  - billit
  - json
  - not
  - support
  - extra
  - fields
---

## About Extra Fields

Billit provides a JSON structure with a wide range of basic fields. Additional fields might be needed for more advanced billing scenario's, or to use it in international networks (Peppol and non-Peppol).

You can add these fields for both Invoices and Creditnote.

The allowed values for Income can be found in the lists below.

## Order (Header Level) - Comments and Notes

If the want to add free text information on Header level, then you have 2 options.

| Key (Header) | Where in Json | Result in Peppol UBL | Result on Billit generated Human Readable |
| --- | --- | --- | --- |
| Invoice.Note | Header - Custom Fields | Note | Not displayed on PDF |
| Comments | Header | Note | Will be displayed on PDF |

Other remarks:

- Use only one of the values in one document : use Invoice.Note **or** Comments, NOT both
- Billit Human Readable will only be generated if you did not include your own PDF

Multiple text information elements can be combined in one field. Example how to put it in the Json body:

Multiple valuesMultiple values, separate lines

```json
"Comments": "test comment 1. Test comment 2.  Test comment 3.  Test comment 4",
```

```json
"Comments": "test comment 1
 test comment 2
 test comment 3
 test comment 4",
```

## Order (Header Level)

| Key (Header) | Linked Info When Peppol | Extra Information |
| --- | --- | --- |
| Invoice.TaxPointDate | [TaxPointDate](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-TaxPointDate/) | Mention date if if the VAT tax point date is different from the Invoice issue date |
| Invoice.InvoicePeriod.StartDate | [InvoicePeriod](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoicePeriod/cbc-StartDate/) | Start date of the services (header level) |
| Invoice.InvoicePeriod.EndDate | [InvoicePeriod](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoicePeriod/cbc-EndDate/) | End date of the services (header level) |
| Invoice.ContractDocumentReference.ID.Text | [ContractDocRef](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-ContractDocumentReference/) | Contract number |
| Invoice.ProjectReference.ID.Text | [ProjectReference](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-ProjectReference/cbc-ID/) | Project Identification |
| Invoice.AccountingCost | [AccountingCost](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-AccountingCost/) | Info for the Buyer about how to put in the Accounts (CostID, General Ledger (G/L, "grootboek"), other reference on request of buyer). This will appear on header as "AccountingCost". Free format, but just the refernence is recommended. |
| PaymentTerms | [PaymentTerms/Note](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-PaymentTerms/cbc-Note/) | Additional free text description for Payment Terms. Here you can add various payment terms descriptions |
| PaymentMeansCode | [PaymentMeansCode](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-PaymentMeans/cbc-PaymentMeansCode/) | Billit will automatically generate a payment means code. But if a specific code is required, it can be set. It must be a valid code. |
| Invoice.OrderReference.SalesOrderID.Text | [SalesOrderID](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-OrderReference/cbc-SalesOrderID/) | Sales order number (Number of the order registered by the Seller) |
| Invoice.DespatchDocumentReference.ID.Text | [DespatchDocRef](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-DespatchDocumentReference/) | Number of the Delivery Note |
| AdditionalDocumentReference | [AdditionalDocumentReference](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AdditionalDocumentReference/) | Add one or more document references, this is free additional information on header level, more info in separate segment below |

## Additional Document Reference (Header)

About Additional Document Reference (Header):

- When sending over Peppol, one additional document reference is used for including the file attachment (e.g. PDF).
- Multiple Additional Document References can be added.
- Each Reference can contain just the value or also a signification of the value.
- This can be useful when you have no other structured field to put the information in.
- Background peppol documentation : [AdditionalDocumentReference](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AdditionalDocumentReference/).

Examples Below with additional document references in custom field. In the Peppol UBL, no DocumentTypeCode is included.

API JSON Additional Doc RefUBL Result (Additional Doc Ref Only)

```json
 "CustomFields"  : {
    "AdditionalDocumentReference1": "Customer Number 1236547",
    "AdditionalDocumentReference2": "International Transport Document 2565781",
    "AdditionalDocumentReference3": "Total Weight 422 kg"
    },
```

```xml
  <cac:AdditionalDocumentReference>
    <cbc:ID>BE0454298213_2460330_900-DocRef3.pdf</cbc:ID>
    <cac:Attachment>
      <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="BE0454298213_2460330_900-DocRef3.pdf">JVBERi0xLjUKJb66yVsNQuIoEhnxlbhSurfJuPgq5hj9vEIAnnhcM+69BaP3Dtq2bPQW1zmuvRCxWRD2/QSXMbG0i7p5rjwqLHNL ...  SxuJk2YcJ8ZrI2mXnFJ2N3yXSv0Dgj5bugplbmRzdHJlYW0KZW5kb2JqCnN0YXJ0eHJlZgoxNTYxMTIKJSVFT0YK</cbc:EmbeddedDocumentBinaryObject>
    </cac:Attachment>
  </cac:AdditionalDocumentReference>
  <cac:AdditionalDocumentReference>
    <cbc:ID>Customer Number 1236547</cbc:ID>
  </cac:AdditionalDocumentReference>
  <cac:AdditionalDocumentReference>
    <cbc:ID>International Transport Document 2565781</cbc:ID>
  </cac:AdditionalDocumentReference>
  <cac:AdditionalDocumentReference>
    <cbc:ID>Total Weight 422 kg</cbc:ID>
  </cac:AdditionalDocumentReference>
```

## Tax Representative Party (Header level - Income)

In case of international trade there can be a Tax Representative Party who is different from the Seller. Information about this Party can also be included.

| Value | Linked Info When Peppol |
| --- | --- |
| Invoice.TaxRepresentativeParty.PartyName.Name (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PartyName/cbc-Name/) |
| Invoice.TaxRepresentativeParty.PostalAddress.StreetName (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cbc-StreetName/) |
| Invoice.TaxRepresentativeParty.PostalAddress.AdditionalStreetName (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cbc-AdditionalStreetName/) |
| Invoice.TaxRepresentativeParty.PostalAddress.CityName (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cbc-CityName/) |
| Invoice.TaxRepresentativeParty.PostalAddress.PostalZone (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cbc-PostalZone/) |
| Invoice.TaxRepresentativeParty.PostalAddress.CountrySubentity (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cbc-CountrySubentity/) |
| Invoice.TaxRepresentativeParty.PostalAddress.AddressLine.Line (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cac-AddressLine/) |
| Invoice.TaxRepresentativeParty.PostalAddress.Country.IdentificationCode (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PostalAddress/cac-Country/cbc-IdentificationCode/) |

Json Example:

Custom Tax Representative Party

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-002",
 "OrderDate": "2025-05-05",
 "ExpiryDate": "2025-06-30",
  "CustomFields"  : {
        "Invoice.TaxRepresentativeParty.PartyName.Name": "TaxRepresentative.Name",
        "Invoice.TaxRepresentativeParty.PostalAddress.StreetName": "Oktrooiplein 1",
        "Invoice.TaxRepresentativeParty.PostalAddress.PostalZone": "9000",
        "Invoice.TaxRepresentativeParty.PostalAddress.CityName": "Gent",
        "Invoice.TaxRepresentativeParty.PostalAddress.Country.IdentificationCode.Text": "BE",
        "Invoice.TaxRepresentativeParty.PartyTaxScheme.CompanyID.Text": "BE0400409999",
        "Invoice.TaxRepresentativeParty.PartyTaxScheme.TaxScheme.ID.Text": "VAT"
    },
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003799999"\
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
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}
```

_Not operational:_

| Invoice.TaxRepresentativeParty.PartyTaxScheme.CompanyID (Text) |
| --- |
| Invoice.TaxRepresentativeParty.PartyTaxScheme.TaxScheme.ID |

## Using Custom Fields in case of a Credit Note

> ❗️
>
> ### Custom Field must contain Credit Note
>
> In case of Credit Note, the Custom Field name must contain "CreditNote".
>
> Example in case of invoice : "Invoice.Delivery.DeliveryLocation.ID.Text": "658798574"
>
> Example in case of Credit Note : "CreditNote.Delivery.DeliveryLocation.ID.Text": "658798574"
>
> More info : [https://docs.billit.be/docs/custom-fields-credit-note](custom-fields-credit-note.md)

## Global Examples Json with Extra / Custom Fields (Income)

See below content of Custom Fields (Income) on Header Level and Detail Line Level.

Example 1 is all main fields, Example 2 is focused on Tax Representative Party.

Example Custom FieldsAdditional CustomFields

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-002",
 "OrderDate": "2025-05-05",
  "ExpiryDate": "2025-06-30",
  "Reference": "8541518745 ", //PO Reference of the buyer
  "OrderTitle": "Other Reference 45215487", // Buyer Reference : Another reference of the buyer
  "CustomFields"  : {
    "Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail":"piet.pieters@live.com",
    "Invoice.AccountingCustomerParty.Party.Contact.Name":"Piet Pieters",
     "Invoice.AccountingCustomerParty.Party.Contact.Telephone":"015999999",
     "Invoice.AccountingSupplierParty.Party.Contact.Telephone":"0385478749",
     "Invoice.AccountingSupplierParty.Party.Contact.ElectronicMail": "email.user@billit.eu",
     "Invoice.AccountingSupplierParty.Party.Contact.Name": "Jean Dupont",
    "Invoice.Delivery.DeliveryLocation.ID.Text": "658798574", //in the Delivery segment, goal is give the delivery address a specific identification
    "Invoice.AccountingCost":"AccCost95421", //Reference of a Cost center for use by the Receiver
    "Invoice.InvoicePeriod.StartDate": "2025-04-01", //To what period the invoice is referring
    "Invoice.InvoicePeriod.EndDate": "2025-04-30",
    "Invoice.Note": "header note description: additional text information",
    "Invoice.ProjectReference.ID.Text": "project number 456854",
    "Invoice.ContractDocumentReference.ID.Text": "contract 456999", //A reference to the contract
    "PaymentMeansCode": "30",
    "PaymentTerms": "30 days end of the month" // PaymentTerms/Note : Free description
    },
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003799999"\
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
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
       "CustomFields"\
    :\
    {\
               "PeppolUnitCode":"H87",\
               "PeppolLineID": "40",\
               "InvoiceLine.Note": "LineNote Extra Free text 1234",\
                "InvoiceLine.InvoicePeriod.StartDate":"2025-04-01",\
               "InvoiceLine.InvoicePeriod.EndDate":"2025-04-30"\
\
        },\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}
```

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-002",
 "OrderDate": "2025-10-06",
  "ExpiryDate": "2025-11-30",
  "Reference": "8541518799 ", //PO Reference of the buyer
  "OrderTitle": "Other Reference 45215487", // Another reference of the buyer
  "CustomFields"  : {
    "Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail":"piet.pieters@live.com",
    "Invoice.AccountingCustomerParty.Party.Contact.Name":"Piet Pieters",
     "Invoice.AccountingCustomerParty.Party.Contact.Telephone":"015999999",
     "Invoice.AccountingSupplierParty.Party.Contact.Telephone":"0385478749",
     "Invoice.AccountingSupplierParty.Party.Contact.ElectronicMail": "emailuser@billit.eu",
     "Invoice.AccountingSupplierParty.Party.Contact.Name": "Jean Dupont",
    "Invoice.Delivery.DeliveryLocation.ID.Text": "658798574", //in the Delivery segment, goal is give the delivery address a specific identification
    "Invoice.AccountingCost":"AccCost95421", //Reference of a Cost center for use by the Receiver
    "Invoice.InvoicePeriod.StartDate": "2025-04-01", //To what period the invoice is referring
    "Invoice.InvoicePeriod.EndDate": "2025-04-30",
    "Invoice.Note": "header note description: additional text information",
    "Invoice.ProjectReference.ID.Text": "project number 456854",
    "Invoice.ContractDocumentReference.ID.Text": "contract 456999", //A reference to the contract
    "PaymentMeansCode": "30",
    "PaymentTerms": "30 days end of the month", // PaymentTerms/Note : Free description
    "AdditionalDocumentReference1": "General Conditions Still Apply",  //First Document Reference (available on sandbox)
     "AdditionalDocumentReference2": "No Commercial Discount",  //Second Document Reference (available on sandbox)
     "Invoice.OrderReference.SalesOrderID.Text": "TestSalesOrderID",  //Reference of the order by the Seller (available on sandbox)
     "Invoice.DespatchDocumentReference.ID.Text": "TestDespatchDocumentReference"  //Delivery not number (available on sandbox)
    },
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003799999"\
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
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
       "CustomFields"\
    :\
    {        },\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}
```

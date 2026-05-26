---
title: "Billit API Source Docs - Extra Fields How Can I Extend Content With Extra Values"
updated: 2026-05-26
---

# Extra Fields : How can I Extend Content with  Extra Values\n\nBillit provides a JSON structure with a wide range of basic fields. Additional fields might be needed for more advanced billing scenario's, or to use it in international networks with other requirement then Peppol.

You can add these fields for both Invoices and Creditnote. To avoid mistakes, the root element (Invoice, CreditNote, InvoiceLine,CreditNoteLine) must always be declared.

The allowed values for Income can be found in the lists below.

## Order (Header Level - Income)   [Skip link to Order (Header Level - Income)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#order-header-level---income)

| Key (Header) | Linked Info When Peppol | Extra Information |
| --- | --- | --- |
| Invoice.TaxPointDate | [TaxPointDate](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-TaxPointDate/) | Mention date if if the VAT tax point date is different from the Invoice issue date |
| Invoice.AccountingCustomerParty.Party. PartyIdentification.ID.Text | [AccountingCustParty](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/) | Party identification is one of the optional identifications |
| Invoice.InvoicePeriod.StartDate | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoicePeriod/cbc-StartDate/) | Start date of the services (header level) |
| Invoice.InvoicePeriod.EndDate | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoicePeriod/cbc-EndDate/) | End date of the services (header level) |
| Invoice.ContractDocumentReference.ID.Text | [ContractDocumentRef](https://docs.billit.be/docs/ContractDocumentReference) | Contract number |
| Invoice.ProjectReference.ID.Text | [ProjectReference](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-ProjectReference/cbc-ID/) | Project Identification |
| Invoice.AccountingCost | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-AccountingCost/) | Info for the Buyer about how to put in the Accounts (CostID, GL, other reference on request of buyer) |
| PaymentTerms | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-PaymentTerms/cbc-Note/) | Additional text description for Payment Terms |
| Invoice.Note | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-Note/) | Free text on header level for comments |
| PaymentMeansCode | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-PaymentMeans/cbc-PaymentMeansCode/) | Billit will automatically generate a payment means code. But if a specific code is required, it can be set. |

## Order : Delivery Location (Header Level - Income)   [Skip link to Order : Delivery Location (Header Level - Income)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#order--delivery-location-header-level---income)

It can be important the specify where goods are delivered. Below more information.

| Key (Header) | Linked Info When Peppol | Extra Information |
| --- | --- | --- |
| Invoice.Delivery.DeliveryLocation.ID.Text | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cbc-ID/) | A number of reference for the delivery location |
| Invoice.Delivery.DeliveryLocation.PostalAddress. StreetName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-StreetName/) |  |
| Invoice.Delivery.DeliveryLocation.PostalAddress. AdditionalStreetName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-AdditionalStreetName/) |  |
| Invoice.Delivery.DeliveryLocation.PostalAddress. CityName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-CityName/) |  |
| Invoice.Delivery.DeliveryLocation.PostalAddress. PostalZone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-PostalZone/) |  |
| Invoice.Delivery.DeliveryLocation.PostalAddress. CountrySubentity | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-CountrySubentity/) |  |
| Invoice.Delivery.DeliveryLocation.PostalAddress. Country. IdentificationCode.Text | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cac-Country/cbc-IdentificationCode/) |  |

## Additional Contact Information on Header Level (Income / Cost)   [Skip link to Additional Contact Information on Header Level (Income / Cost)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#additional-contact-information-on-header-level-income--cost)

Within the Basic Json you can include a lot of information about Customer and Supplier contacts. Optionally, it can also be included in the fields below.

| Key (Header) | Linked Info When Peppol |  |
| --- | --- | --- |
| Invoice.AccountingSupplierParty.Party.Contact.Name | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-Name/) |  |
| Invoice.AccountingSupplierParty.Party.Contact.Telephone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-Telephone/) |  |
| Invoice.AccountingSupplierParty.Party.Contact.ElectronicMail | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-ElectronicMail/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.Name | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-Name/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.Telephone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-Telephone/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-ElectronicMail/) |  |

## Orderline (Line level - Income)   [Skip link to Orderline (Line level - Income)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#orderline-line-level---income)

| Key (Line) | Linked Info When Peppol |  |
| --- | --- | --- |
| PeppolUnitCode | [Link](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNECERec20/) . | Unit of Measure. Code list. Sample value H87 |
| InvoiceLine.InvoicePeriod.StartDate | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-InvoicePeriod/cbc-StartDate/) | Start date of the services (Line level) |
| InvoiceLine.InvoicePeriod.EndDate | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-InvoicePeriod/cbc-EndDate/) | End date of the services (Line level) |
| InvoiceLine.Item.CommodityClassification.ItemClassificationCode.Text | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-Item/cac-CommodityClassification/cbc-ItemClassificationCode/) | The description text. |
| InvoiceLine.Item.CommodityClassification.ItemClassificationCode.ListID | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-Item/cac-CommodityClassification/cbc-ItemClassificationCode/listID/) | This ID must be compliant with the code list. |
| PeppolLineID | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cbc-ID/) | The line number is autogenerated by Billit. With PeppolLineID, you can set your own values. |
| InvoiceLine.Note | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cbc-Note/) | Extra free text for additional info |

## Tax Representative Party (Header level - Income)   [Skip link to Tax Representative Party (Header level - Income)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#tax-representative-party-header-level---income)

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
| Invoice.TaxRepresentativeParty.PartyTaxScheme.CompanyID (Text) | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PartyTaxScheme/cbc-CompanyID/) |
| Invoice.TaxRepresentativeParty.PartyTaxScheme.TaxScheme.ID | ( [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxRepresentativeParty/cac-PartyTaxScheme/cac-TaxScheme/cbc-ID/) |

## Example Json with Extra / Custom Fields (Income)   [Skip link to Example Json with Extra / Custom Fields (Income)](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#example-json-with-extra--custom-fields-income)

See below content of Custom Fields (Income) on Header Level and Detail Line Level.

Example 1 is all main fields, Example 2 is focused on Tax Representative Party.

Main Example Custom FieldsCustom Tax Representative Party

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-002",
 "OrderDate": "2025-05-05",
 "ExpiryDate": "2025-06-30",
  "CustomFields"  : {
    "Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail":"ivan.vanhaecht@live.com",
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
               "InvoiceLine.Item.CommodityClassification.ItemClassificationCode.Text":"45123456789",\
               "InvoiceLine.Item.CommodityClassification.ItemClassificationCode.ListID":"PO",\
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

```\1

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
        "Invoice.TaxRepresentativeParty.PostalAddress.CityName": "TaxRepresentative.Address.City",
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

## Will be supported in the future   [Skip link to Will be supported in the future](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support\#will-be-supported-in-the-future)

| Key (Header) | Value (TransferType = Peppol) |
| --- | --- |
| Invoice.OrderReference.SalesOrderID.ID.Text | [https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-OrderReference/cbc-SalesOrderID/](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-OrderReference/cbc-SalesOrderID/) |

Updated21 days ago

* * *

Did this page help you?

Yes

No
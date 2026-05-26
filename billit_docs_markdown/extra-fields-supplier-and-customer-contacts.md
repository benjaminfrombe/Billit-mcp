---
title: "Extra Fields : Supplier and Customer Contacts"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/extra-fields-supplier-and-customer-contacts"
source_slug: "extra-fields-supplier-and-customer-contacts"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - extra
  - fields
  - supplier
  - customer
  - contacts
---

## Standard Behaviour

Within the Basic Json body, when sending, contact information is set as follows:

- Customer : you include contacts in the customer segment of the Json
- Supplier : this is taken from the contact information in "My Company"

Customer Data in Json

```json
{
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Email" : "piet.pieters@telenet.be",  //Useful when sending via email is done
   "Language" : "NL",  // Language can be useful when an email is sent
   "Phone" : "+3292035699",  // Customer Phone
   "Nr": "5624871",  //Customer number from ERP, shown in Billit customer data, not in Einvoice message
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",  //Only when additional identifiers must be added\
        "Identifier": "5430003732007"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode" : "9001",\
        "Box": "box1",  // Postal box in the building"\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
				"Zipcode": "9001",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
```

## Alternative Solution for Contact Information on Header Level (Income / Cost)

As an alternative, Specific API fields are available:

- What : Contact info :
  - Name, Email, Telephone
  - For Supplier (sender) and Customer (Receiver)
- Specific behaviour:
  - When these data are included in the posted invoice data, they do not update the customer data stored in Billit.
  - The contact data do only apply to this invoice
  - You can still communicatie in the customer segment the regular customer section, but the contact data in the custom fields section of the API will have priority for this invoice
  - These contact info:
    - will appear in the output einvoice file (typically UBL)
    - will not appear in on the Billit Human Readable (you might use you own human readable)
- Type of use:
  - supported : in UBL the contact details of supplier and/or customer will be filled
  - not supported : use the email address of customer to send via email

Field information:

| Custom Field (Header, when Invoice) | Linked Info When Peppol |  |
| --- | --- | --- |
| Invoice.AccountingSupplierParty.Party.Contact.Name | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-Name/) |  |
| Invoice.AccountingSupplierParty.Party.Contact.Telephone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-Telephone/) |  |
| Invoice.AccountingSupplierParty.Party.Contact.ElectronicMail | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingSupplierParty/cac-Party/cac-Contact/cbc-ElectronicMail/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.Name | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-Name/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.Telephone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-Telephone/) |  |
| Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AccountingCustomerParty/cac-Party/cac-Contact/cbc-ElectronicMail/) |  |

Example of the Json segment

Contacts via Custom Fields

```json
    "CustomFields"  : {
     "Invoice.AccountingSupplierParty.Party.Contact.Name":"Piet Pieters2",
     "Invoice.AccountingSupplierParty.Party.Contact.Telephone":"0385478999",
     "Invoice.AccountingSupplierParty.Party.Contact.ElectronicMail": "piet.pieters1@gmail.com",
     "Invoice.AccountingCustomerParty.Party.Contact.Name": "Jean Dupont2",
     "Invoice.AccountingCustomerParty.Party.Contact.Telephone": "0385478888",
     "Invoice.AccountingCustomerParty.Party.Contact.ElectronicMail": "jean.dupont2@live.com"
    },
```

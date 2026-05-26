---
title: "How can I send to a specific Company Numer ?"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-can-i-send-to-a-specific-company-number"
source_slug: "how-can-i-send-to-a-specific-company-number"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - send
  - specific
  - company
  - number
  - numer
---

## Customer has Company Number but no VAT Number

A company might not have a VAT number, they are identified with another identification number, typically a company number. In that case the field VAT number is not used, an additional identifier is included.

Below the identifier info for Belgium and the Netherlands:

| Country (example) | Identifier Type | Identifier |
| --- | --- | --- |
| Belgium | Company Number | CBE |
| Netherlands | Kamer van Koophandel nummer | KvK |

For the full list of identifiers, we refer to [Identifier List](allowed-identifiers.md).

Examples of the API content for Belgium and the Netherlands:

BE : Company NumberNL : KvK

```json
  "Customer": {
   "Name": "Customer Company Name",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
          	"IdentifierType": "CBE",  //Identifier for Belgian Company Number\
          	"Identifier": "0862884999"  //Belgian Company Number\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Customer Company Name Belgium",\
        "Street": "XXXXX",\
        "StreetNumber": "XXXX",\
        "City": "XXXX",\
        "Box": "XXXX",\
        "CountryCode": "BE”\
       	}\
   ]
 }
```

```json
  "Customer": {
   "Name": "Customer Company Name",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
          	"IdentifierType": "CBE",  //Identifier for Belgian Company Number\
          	"Identifier": "0862884999"  //Belgian Company Number\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Customer Company Name Netherlands",\
        "Street": "XXXXX",\
        "StreetNumber": "XXXX",\
        "City": "XXXX",\
        "Box": "XXXX",\
        "CountryCode": "NL”\
       	}\
   ]
 }
```

## VAT different from Company Number

When sending e-invoice you might come across the possibility that you have to send an invoice towards an entity which has multiple entities with the same VAT number. To make sure the invoices are delivered to the correct receiver you have a few options.

CBE (Company number) is communicated as an additional identifier. For this customer, the company number will get preference and used it the number is registered on Peppol as receiver.

JSON

```json
  "Customer": {
   "Name": "Politie Antwerpen",
   "VATNumber": " BE0207500123",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
          	"IdentifierType": "CBE",\
          	"Identifier": "0862884185"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Politie",\
        "Street": "XXXXX",\
        "StreetNumber": "XXXX",\
        "City": "XXXX",\
        "Box": "XXXX",\
        "CountryCode": "XXXX”\
       	}\
   ]
 }
```

---
title: "Billit API Source Docs - How Can I Send An Invoice With VAT Number Different To Company Number Or GLN CBE"
updated: 2026-05-26
---

# How can I send an invoice with VAT number different to Company Number or GLN CBE\n\nWhen sending e-invoice you might come across the possibility that you have to send an invoice towards an entity which has multiple entities with the same VAT number. To make sure the invoices are delivered to the correct receiver you have a few options.

### Using: VAT - CBE.   [Skip link to Using: VAT - CBE.](https://docs.billit.be/docs/how-can-i-send-an-invoice-with-vat-different-to-cbe\#using-vat---cbe)

CBE (Company number) is communicated as an additional identifier. For this customer, the company number will get preference and used it the number is registered on Peppol as receiver.

JSON

```\1

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

### Using: VAT - GLN or other identifier   [Skip link to Using: VAT -  GLN or other identifier](https://docs.billit.be/docs/how-can-i-send-an-invoice-with-vat-different-to-cbe\#using-vat----gln-or-other-identifier)

GLN is communicated as an additional identifier. For this customer, GLN will be added as a receiving capability. In Billit interface, the Priority can be set to GLN for a specific customer: [https://www.billit.eu/en-int/help-page/peppol/frequently-asked-questions-about-peppol/prioritize-identifiers/?q=gln#f-3](https://www.billit.eu/en-int/help-page/peppol/frequently-asked-questions-about-peppol/prioritize-identifiers/?q=gln#f-3) .

How to communicatie in the Json order info:

JSON

```\1

  "Customer": {
   "Name": "Billit",
   "VATNumber": " BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
          	"IdentifierType": "GLN",\
          	"Identifier": "5430003732007"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "XXXXX",\
        "StreetNumber": "XXXX",\
        "City": "XXXX",\
        "Box": "XXXX",\
        "CountryCode": "XXXX”\
       	}\
   	]
 }

```

Updated23 days ago

* * *

Did this page help you?

Yes

No
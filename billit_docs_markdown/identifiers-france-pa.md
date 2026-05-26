---
title: "Identifiers in France"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/identifiers-france-pa"
source_slug: "identifiers-france-pa"
category: "partner-france"
topics:
  - partner
  - france
  - identifiers
  - pa
---

## Identifier Overview

Multiple identifiers can be used for defining the receiver and the sender :

| Name | Info | Billit Identifier ID in API | Peppol code | Where to put in API |
| --- | --- | --- | --- | --- |
| SIREN | Enterprise number (9 number, including check digit) | SIRET | 0002 | Identifiers |
| SIRET | Is Siren (9 digits) with a seperate estblishment number (5 digits) = 14 digits. So for 1 Siren, there can be multiple Siret Numbers for one company (Establishment Number) | SIRENE (will become SIREN) | 0009 | Identifiers |
| VAT number | French VAT number. Consists of FR + the Siren number. | not needed | 9957 | VATNumber |
| Suffixe | Routing address to specified by the receiver for specific routing purposes. This number is Siren + additional code. Can also be used by the sender. | CTC | 0225 | Identifiers |
| CTC | Additional Electronic Address specified by the receiver for specific routing purposes. Address can be long, max. 130 characters. Can also be used by the sender. Considered as the primary identifier. Standard value is the Siren number, can be extended with more information. | CTC | 0225 | Identifiers |
| Codes Routage | B2G only, is an extra identification delivered by the receiving goverment customer | next step | next step | Identifiers |

## How to include your Customer Identifiers in Billit

Identifiers you should include:

- If the company has a VAT number, it should always be included
- If the customer has registered with a specific identifier, you should include this identifier

Examples in Json API when posting an invoice, for the customer segment:

VAT-SiretVAT-SIRENVAT-SIREN-CTC

```json
    "Customer": {
        "Nr": "000700999,
        "Name": "BAUDIN TEST CHATEAUNEUF",
        "VATNumber": "FR25842499999",
				"PartyType": "Customer",

        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "BAUDIN TEST CHATEAUNEUF",\
                "Street": "Rue de la Brosse 999",\
                "Zipcode": "45110",\
                "City": "CHATEAUNEUF SUR LOIRE",\
                "CountryCode": "FR"\
            }\
        ]
  		 "Identifiers": [\
        {\
        "IdentifierType": "SIRET",\
        "Identifier": "84249114400999"\
        }\
}\
```\
\
```json\
    "Customer": {\
        "Nr": "000700999,\
        "Name": "BAUDIN TEST CHATEAUNEUF",\
        "VATNumber": "FR25842499999",\
				"PartyType": "Customer",\
\
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "BAUDIN TEST CHATEAUNEUF",\
                "Street": "Rue de la Brosse 999",\
                "Zipcode": "45110",\
                "City": "CHATEAUNEUF SUR LOIRE",\
                "CountryCode": "FR"\
            }\
        ]\
  		 "Identifiers": [\
        {\
        "IdentifierType": "SIRENE",\
        "Identifier": "842491144"\
        }\
}\
```\
\
```json\
    "Customer": {\
        "Nr": "000700999,\
        "Name": "BAUDIN TEST CHATEAUNEUF",\
        "VATNumber": "FR25842499999",\
				"PartyType": "Customer",\
\
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "BAUDIN TEST CHATEAUNEUF",\
                "Street": "Rue de la Brosse 999",\
                "Zipcode": "45110",\
                "City": "CHATEAUNEUF SUR LOIRE",\
                "CountryCode": "FR"\
            }\
        ]\
  		 "Identifiers": [\
        {\
        "IdentifierType": "SIRENE",\
        "Identifier": "842491144"\
        },\
				{\
        "IdentifierType": "CTC",\
        "Identifier": "842491144_12345"\
         }\
	}\
```\
\
Updated 7 days ago\
\
* * *\
\
Did this page help you?\
\
Yes\
\
No\
\

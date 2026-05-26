---
title: "Customer has Special Identifiers"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/customer-has-special-identifiers"
source_slug: "customer-has-special-identifiers"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - customer
  - has
  - special
  - identifiers
---

## Why Special Identifiers

- Organisations get special identifiers which are not country related.
  - E.g. GLN [https://www.billit.eu/en-int/help-page/income/invoices/what-is-a-gln-number/](https://www.billit.eu/en-int/help-page/income/invoices/what-is-a-gln-number/). GLN and API use : [https://docs.billit.be/docs/send-to-customer-with-gln-number](send-to-customer-with-gln-number.md).
  - Duns number (Dun & Bradstreet) [https://www.billit.eu/en-int/help-page/peppol/international-invoicing/register-on-peppol-without-vat-or-kvk-number/](https://www.billit.eu/en-int/help-page/peppol/international-invoicing/register-on-peppol-without-vat-or-kvk-number/)
  - LEI number
- Organisations with country specific identifiers
  - For the full list of identifiers in Billit : [https://docs.billit.be/docs/allowed-identifiers](allowed-identifiers.md)

## How to Include the special Identifier in the API

This is in the identifier section int he Customer segment.

Below examples:

Swedish OrgNrFrance Siret

```json
"Customer": {
"Name": "Långtest AB",
"PartyType": "Customer",
 "Identifiers": [\
        {\
        "IdentifierType": "ORGNR",\
        "Identifier": "5564326808"\
        }\
],
"Street": "Test 9116",
"City": "Stockholm",
"Zipcode": "10999",
"CountryCode": "",
"ContactFirstName": "",
"ContactLastName": "",
"VATNumber": "SE5564326999"
}
```

```json
"Customer":
{
  "Name": "TESTCUSTOMER",
  "VATNumber": "FR25842499999", // Use only If Government Organisation has a VAT
  "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "SIRET", //Mandatory Identifier for Chorus\
        "Identifier": "84249114400015"\
        },\
\
    ]
 }
```

- [Send to Customer with GLN Number](send-to-customer-with-gln-number.md)

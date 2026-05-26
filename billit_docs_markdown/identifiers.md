---
title: "Identifiers DE"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/identfiers"
source_slug: "identfiers"
category: "reference-errors"
topics:
  - reference
  - errors
  - identifiers
  - de
---

## Customer Identifiers

Per customer, in the Json API content, the idenfier(s) can be defined:

| Identifier | Accepted identifier | Use | Content in API Json |
| --- | --- | --- | --- |
| VAT-number | yes | Most common | field "VATNumber" |
| Steuer number | no | - | - |
| GLN-number | yes | If specified by the customer | Identifier section, IdentifierType "GLN" |
| LEITWEG ID | yes | When government organisation | Identifier section, IdentifierType "LEITWEGID" |

## API Examples with customer identifier

Customer section in Json API:

VAT-numberLeitwegID

```text
 "Customer": {
   "Name": "Gemeinde XYZ",
   //"VATNumber": "",  // no VAT number available
	 "PartyID" : "452154"  //technical ID of customer in Billit, allows to find customer in easier way in Billit, not mandatory
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "LEITWEGID",\
        "Identifier": "13074099-k000-99"\
        }\
    ],
	"Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Customer Name",\
        "Street": "Landstraße ",\
        "StreetNumber": "99",\
        "City": "Frankfurt am Main",\
        "CountryCode": "DE"\
        }\
```\
\
```text\
\
```\
\
## Supplier Identifier\
\
When you are a commercial company, adding the VAT-number in MyBillit / My Company is enough as identifier.\
\
Updated 19 days ago\
\
* * *\
\
Did this page help you?\
\
Yes\
\
No\
\

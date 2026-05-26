---
title: "Billit API Source Docs - Identifiers"
updated: 2026-05-26
---

# Identifiers\n\n# Usage   [Skip link to Usage](https://docs.billit.be/docs/allowed-identifiers\#usage)

You are allowed to add the following piece of code in any party Object.

Some Examples below:

Single IdentifierMultiple Identifiers

```\1

"Identifiers": [\
    {\
      "IdentifierType": "SDIPEC",\
      "Identifier": "Support@Billit.be"\
    }\
  ]

```

```\1

"Identifiers": [\
  { "IdentifierType": "SDICODFIS", "Identifier": "" },\
  { "IdentifierType": "SDICODDEST", "Identifier": "3PRL4IK" },\
  { "IdentifierType": "SDIPEC", "Identifier": "Support@Billit.be" }\
]

```

The Billit API supports multiple identifiers from multiple countries. A list can be found below. Some identifiers are 'Global", they can be used in multiple countries.

| IdentifierType | CountryCode | EInvoiceNetwork | NetworkCode |
| --- | --- | --- | --- |
| VAT | AD | Peppol | 9922 |
| VAT | AE |  |  |
| VAT | AL | Peppol | 9923 |
| VAT | AT | Peppol | 9914 |
| VAT | BA | Peppol | 9924 |
| VAT | BE | Peppol | 9925 |
| CBE | BE | Peppol | 0028 |
| VAT | BG | Peppol | 9926 |
| CNPJ | BR |  |  |
| VAT | CH | Peppol | 9927 |
| VAT | CN |  |  |
| VAT | CV |  |  |
| VAT | CY | Peppol | 9928 |
| VAT | CZ | Peppol | 9929 |
| LEITWEGID | DE | Peppol | 0204 |
| VAT | DE | Peppol | 9930 |
| VAT | DK |  |  |
| ERST | DK | Peppol | 0198 |
| DIGST | DK | Peppol | 0184 |
| CVR | DK | Peppol | 9902 |
| VAT | EE | Peppol | 9931 |
| VAT | EL | Peppol | 9933 |
| VAT | ES | Peppol | 9920 |
| NIE | ES |  |  |
| DNI | ES |  |  |
| NIF | ES |  |  |
| CIF | ES |  |  |
| VAT | FI | Peppol | 0213 |
| OVT | FI | Peppol | 0037 |
| ORG | FI | Peppol | 0213 |
| NOVT | FI | Peppol | 0216 |
| SIRET | FR | Chorus / Peppol | 0009 |
| SIRENE | FR | Chorus / Peppol | 0002 |
| Service Code | FR | Chorus |  |
| VAT | FR | Peppol | 9957 |
| FRCTC | FR | Peppol | 0225 |
| VAT | GB | Peppol | 9932 |
| GLN | Global | Peppol | 0088 |
| DUNS | Global | Peppol | 0060 |
| LEI | Global | Peppol | 0199 |
| VAT | Global |  |  |
| VAT | GR | Peppol | 9933 |
| VAT | HR | Peppol | 9934 |
| OIB | HR | Peppol | 9934 |
| VAT | HU | Peppol | 9910 |
| VAT | ID |  |  |
| VAT | IE | Peppol | 9935 |
| VAT | IL |  |  |
| SDICODDEST | IT | SDI | IT:CODDEST |
| SDICODFIS | IT | SDI | 0210 |
| SDIPEC | IT | SDI | IT:PEC |
| SDIB2G | IT | SDI | IT:CODDEST |
| VAT | IT | Peppol | 9906 |
| VAT | JP | Peppol | 0221 |
| SST | JP | Peppol | 0188 |
| VAT | KR |  |  |
| VAT | LI | Peppol | 9936 |
| VAT | LT | Peppol | 9937 |
| LEC | LT | Peppol | 0200 |
| VAT | LU | Peppol | 9938 |
| RPM | LU | Peppol | 9938 |
| VAT | LV | Peppol | 9939 |
| VAT | MA |  |  |
| VAT | MC | Peppol | 9940 |
| VAT | ME | Peppol | 9941 |
| VAT | MK | Peppol | 9942 |
| VAT | MT | Peppol | 9943 |
| TIN | MX | SAT |  |
| EIF | MY | Peppol | 0230 |
| KVK | NL | Peppol | 0106 |
| OIN | NL | Peppol | 0190 |
| VAT | NL | Peppol | 9944 |
| VAT | NO | Peppol | 0192 |
| ORG | NO | Peppol | 0192 |
| VAT | NZ | Peppol | 0088 |
| ABN | NZ | Peppol | 0151 |
| VAT | PL | Peppol | 9945 |
| VAT | PT | Peppol | 9946 |
| VAT | RO | Peppol | 9947 |
| VAT | RS | Peppol | 9948 |
| MBR | RS |  |  |
| VAT | SE | Peppol | 9955 |
| ORGNR | SE | Peppol | 0007 |
| VAT | SG | Peppol | 0195 |
| VAT | SI | Peppol | 9949 |
| VAT | SK | Peppol | 9950 |
| VAT | SM | Peppol | 9951 |
| SDICODDEST | SM | SDI | IT:CODDEST |
| SDICODFIS | SM | SDI | 0210 |
| SDIPEC | SM | SDI | IT:PEC |
| SDIB2G | SM | SDI | IT:CODDEST |
| VAT | TR | Peppol | 9952 |
| EIN | US | Peppol | 9959 |
| VAT | VA | Peppol |  |

Updated23 days ago

* * *

Did this page help you?

Yes

No
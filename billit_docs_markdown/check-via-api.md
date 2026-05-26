---
title: "Check Peppol Receiving Capabilities via API"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/check-via-api"
source_slug: "check-via-api"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - check
  - peppol
  - capabilities
---

### How : Get information

In order to launch a request about receiving capabilities, below examples.

- VAT-based: For many countries, results for a customer VAT number can be retrieved with endpoint: (example for sandbox environment)

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0437299999)

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/NL002059999B90](https://api.sandbox.billit.be/v1/peppol/participantInformation/NL002059999B90)

- Company number: For Belgium, company number can be retrieved in a similar way:

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0437299999)

### Peppol Test versus Peppol Production

| Endpoint | Method | Result of Environment |
| --- | --- | --- |
| [https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999) | GET | Peppol test |
| [https://api.billit.be/v1/peppol/participantInformation/9925:BE0437299999](https://api.billit.be/v1/peppol/participantInformation/9925:BE0437299999) | GET | Peppol production |

Be aware that on Peppol list much less receivers are registered than on Peppol production.

### Check Receiving capabilities via specific schemeID

There are several other schemeID's that might be relevant (country specific, GLN-numbers, other). It might also be needed to use them to get a full insight of receiving capabilities.

For the full list of Billit identifiers : [https://docs.billit.be/docs/allowed-identifiers](allowed-identifiers.md)

Examples how to get the information:

- GLN number
  - Certain organisations are registered with GLN numbers. You cannot search the correct GLN number via a VAT number. But once you know the GLN number, you can check the receiving capabilities.
  - Example of a search via the GLN number : GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0088:5430003799999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0088:5430003799999)
- Search a VAT number with the country specific scheme ID
  - Belgium, VAT : GET \[< [https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999>](https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999)\]( [https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999))
  - Netherlands, VAT GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/9944:NL00205999B90](https://api.sandbox.billit.be/v1/peppol/participantInformation/9944:NL002059999B90)
  - Germany, VAT: GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/9930:NL00205999B90](https://api.sandbox.billit.be/v1/peppol/participantInformation/9944:NL00205999B90)
- Other country specific endpoint schemeID's
  - Netherlands, KvK : GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0106:27379999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0106:27379999)
  - Netherlands, OIN (government) : \[< [https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:0000000100807999000>](https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:00000001008078452000)\]( [https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:00000001008078452000](https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:00000001008078452000))

### What Information do I get back ?

| IdentifierType | Example | Information |
| --- | --- | --- |
| Registered | true, false | This is the main element : Registration is true or false |
| Identifier | 0190:0000000100807999000 | Confirmation of scheme ID and identifier used for the search |
| DocumentTypes | "BISv3Invoice",<br>"IMR",<br>"BISv3CreditNote"<br>"MLR", | Registered true/false is not enough, support must be for the document types invoice and CreditNote for being able to send these documents. BISv3Invoice and BISv3CreditNote is most common, some variants are possible. |
| ServiceDetails | More advanced information on Peppol details |  |

Below 3 examples of results:

Result BE Query via Company NumberResult BE Query via VATResult NetherlandsNo Registrations

```json
{
    "Registered": true,
    "Identifier": "0208:0563846944",
    "DocumentTypes": [\
        "BISv3Invoice",\
        "IMR",\
        "MLR",\
        "BISv3CreditNote",\
        "MYPintInvoice",\
        "MYPintCreditNote"\
    ],
    "ServiceDetails": [\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2::ApplicationResponse##urn:fdc:peppol.eu:poacc:trns:invoice_response:3::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:poacc:bis:invoice_response:3",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2::ApplicationResponse##urn:fdc:peppol.eu:poacc:trns:mlr:3::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:poacc:bis:mlr:3",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:peppol:pint:billing-1@my-1::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:peppol:bis:billing",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:peppol:pint:billing-1@my-1::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:peppol:bis:billing",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        }\
    ]
}
```

```json
{
    "Registered": true,
    "Identifier": "9925:BE0563846944",
    "DocumentTypes": [\
        "BISv3Invoice",\
        "IMR",\
        "MLR",\
        "BISv3CreditNote"\
    ],
    "ServiceDetails": [\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2::ApplicationResponse##urn:fdc:peppol.eu:poacc:trns:invoice_response:3::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:poacc:bis:invoice_response:3",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2::ApplicationResponse##urn:fdc:peppol.eu:poacc:trns:mlr:3::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:poacc:bis:mlr:3",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        }\
    ]
}
```

```json
{
    "Registered": true,
    "Identifier": "0190:00000001008078452000",
    "DocumentTypes": [\
        "BISv3Invoice",\
        "SIInvoice",\
        "SICreditNote",\
        "BISv3CreditNote"\
    ],
    "ServiceDetails": [\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:nen.nl:nlcius:v1.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:cen.eu:en16931:2017#compliant#urn:fdc:nen.nl:nlcius:v1.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        },\
        {\
            "DocumentIdentifier": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2::CreditNote##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1",\
            "DocumentIdentifierScheme": "busdox-docid-qns",\
            "Processes": [\
                {\
                    "ProcessIdentifier": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",\
                    "ProcessIdentifierScheme": "cenbii-procid-ubl"\
                }\
            ]\
        }\
    ]
}
```

```json
{
    "Registered": false,
    "Identifier": "9925:BE0402940374",
    "DocumentTypes": [],
    "ServiceDetails": []
}
```

## Other networks then Peppol

Other networks cannot be searched via the same endpoint. Country specific websites and tools are available to get the required information.

---
title: "How to Find a Receiver in France"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-to-find-a-receiver-in-france"
source_slug: "how-to-find-a-receiver-in-france"
category: "partner-france"
topics:
  - partner
  - france
  - find
  - receiver
---

## Context

French companies are registered for receiving in :

- the French Annuaire (all registered companies)
- on the Peppol network (the majority of the companies registered on the Annuaire).

Billit supports the sending to the customer via the Peppol network.

## How to find a company on Peppol - Concepts

A company can be registered with one more identifiers. The full list is found on [https://docs.billit.be/docs/identifiers-france-pa](identifiers-france-pa.md).

In order to find the published identifier of the customer, possible steps are

- Search with structured data : this can be done with VAT-number and SIREN/SIRET
- If you cannot find it, a search on name of the customer could be done via [https://directory.peppol.eu/public](https://directory.peppol.eu/public) (Peppol production environment)
- For the other identifier types, you (Suffixe, CTC, Code Routage) you need information from the customer (direct contact, web pages, info on purchase orders)

Keep in mind that most receivers are only registered on the Peppol production environment, not the Peppol test environment.

## How to find a company on Peppol via API (Participant Information)

General capabilities are explained on : [https://docs.billit.be/docs/check-via-api](check-via-api.md).

Via the Billit API, the receiving capability on Peppol can be verified. Examples below for French identifiers

| Identifier type | API-call on production | API-call on sandbox |
| --- | --- | --- |
| SIREN | GET [https://api.billit.be/v1/peppol/participantInformation/0002:501842389](https://api.billit.be/v1/peppol/participantInformation/0002:501842389) | GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0002:501842389](https://api.sandbox.billit.be/v1/peppol/participantInformation/0002:501842389) |
| SIRET | GET [https://api.billit.be/v1/peppol/participantInformation/0009:49495677400744](https://api.billit.be/v1/peppol/participantInformation/0009:49495677400744) | GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0009:49495677400744](https://api.sandbox.billit.be/v1/peppol/participantInformation/0009:49495677400744) |
| VAT Number | GET [https://api.billit.be/v1/peppol/participantinformation/FR39694636118](https://api.billit.be/v1/peppol/participantinformation/FR39694636118) | GET [https://api.sandbox.billit.be/v1/peppol/participantinformation/FR39694636118](https://api.sandbox.billit.be/v1/peppol/participantinformation/FR39694636118) |
| Suffixe or CTC | GET [https://api.billit.be/v1/peppol/participantInformation/0225:501842389](https://api.billit.be/v1/peppol/participantInformation/0225:501842389) | GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0225:501842389](https://api.sandbox.billit.be/v1/peppol/participantInformation/0225:501842389) |

## Retrieve info from Annuaire

As an end-user you can check the French website (valid for production environment).

This allows you to fill in the Siren or Siret or company name or the address and get information back about the annuaire registration. Valid on the production environment.

URL : [https://facturation.chorus-pro.gouv.fr/annuaire/#/](https://facturation.chorus-pro.gouv.fr/annuaire/#/)

Updated7 days ago

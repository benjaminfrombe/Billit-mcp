---
title: "Setup the Companies for France"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/create-account-and-french-integration"
source_slug: "create-account-and-french-integration"
category: "partner-france"
topics:
  - partner
  - france
  - create
  - account
  - french
  - integration
  - setup
  - companies
---

## Company Creation

Create French company in Billit.

- Set the country code to France first
- Make sure country code is filled
- Make sure that VAT-number and Siren number are filled. Example below.

![](https://files.readme.io/1d89ad4adee1bf0d15438c9bead2003726e79ece27d71df4b6a68aa10ceb0cb3-company1.png)

- Fill in other missing data, such as company name, invoice address, bank account, etc.

Overview in My billit :

![](https://files.readme.io/235200bea33c8716ff797c528b8c0e708efb4a6fd9bcc37eb09260149c32e84d-2026-05-19_14-22-14.png)

About colour codes:

- blue line : minimum data to start with
- green line : extra info, can be added as a second step
- blue dotted line : will be added by Billit when the integration is created (see next step)

## Configure the Integration

For use in France the specific integration tile must be set up.

Currently limited to the Billit production environment.

You can search the integration tile :

| Language | Title of the integration tile |
| --- | --- |
| English | Electronic invoicing in France |
| French | Facturation électronique en France |

How to find:

![](https://files.readme.io/478489baca5f82b545f76f6b99ebb245797cf2c3ee11980c5e677cf1a1c3c4df-integration.png)

Fill in the integration:

| Field | Info | Mandatory |
| --- | --- | --- |
| Siren | Automatically filled if present in MyCompany | Yes |
| Siret | Automatically filled if present in MyCompany | No |
| Adressing suffix | This is for generating the CTC. If left empty, Billit will generate automatically from Siren. If you add info, this will be added to the CTC. CTC is the primary identifier. | Yes |
| Adressing Identifier | This is th full CTC (Siren + optional Addressing Suffix) |  |

Result after saving (Example) :

![](https://files.readme.io/627e8aefeed5254e5e5c280d35891fee66942256ff4664ffc459e0bc3f2db4ef-integrfr.png)

## Registration on Annuaire and Peppol

In My company, go to E-invoicing:

![](https://files.readme.io/7eec08409252caa0aa5f46809b70d2cf83ede653b3eed66bf8c2b758c17bd1f7-company_peppol.png)

Make sure that minimum the CTC is registered:

![](https://files.readme.io/c180a7dfbc76ac54944aa550fa92779d922ac9bc9f4dd44f4bd6e6592592c1ad-CTC.png)

Info about the registrations:

| What | Billit activity |
| --- | --- |
| Annuaire | Billit will automatically register on the French Annuaire. This will be effective next business day around 10 am CET. |
| Peppol | Registration on Peppol will be automatically executed when Annuaire registration is ready. |

Updated7 days ago

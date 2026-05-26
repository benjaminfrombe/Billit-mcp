---
title: "Split Payment / Reverse Charge"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/split-payment-reverse-charge"
source_slug: "split-payment-reverse-charge"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - split
  - payment
  - reverse
  - charge
---

## Set value for P\_18 and P\_18A fields

Billit will set a value for P\_18 depending on ventilation code ( [https://docs.billit.be/docs/ksef-tax-codes](ksef-tax-codes.md) ) and no value for P\_18A.

The values for the fields P\_18 and P\_18A can be set via CustomFields. This will always overrule the default settings by Billit.

How to do this (custom fields on header level):

P\_18 and P\_18A

```json
    "CustomFields":
    {
			"Faktura.Fa.Adnotacje.P_18": "1",
			"Faktura.Fa.Adnotacje.P_18A": "1"
    },
```

## Adding Text Descriptions linked to Split Payment

When needed, legal descriptions for Split Payment can be added via the DodatkowyOpis custom fields.

Example Below.

Legal texts

```json
    "CustomFields":
    {
			"Faktura.FA.DodatkowyOpis1.Klucz": " Informacja o MPP",
			"Faktura.FA.DodatkowyOpis1Wartosc": "mechanizm podzielonej płatności",
    },
```

Updated29 days ago

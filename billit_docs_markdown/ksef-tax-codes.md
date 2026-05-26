---
title: "Tax Codes KSeF"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ksef-tax-codes"
source_slug: "ksef-tax-codes"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - tax
  - codes
---

## Ventilation Codes to Use for KSeF

For General use of ventilation codes in Billit, see [https://docs.billit.be/docs/ventilation-codes](ventilation-codes.md) .

Remark : in case of KSeF, ventilation code must be put on the header of the invoice, not the detail line. In case of domestic use, no ventilation code must be added.

**Specific Polish KSeF codes for 0 %, exempt and related:**

| P\_12 KSeF code | Description | Billit Ventilation Code |
| --- | --- | --- |
| zw | Exempt (Zwolnione) | 22 |
| 0 WDT | 0 % rate for intra-community supply ICS of goods (WDT) | 51 |
| np I | "np I" - in the case of supplies of goods and provision of services outside the (territory of the) country which are not subject to taxation, ( _excluding_ _the transactions referred to in Article 100 sec. 1 item 4 of the Act and the OSS_) | 104 |
| np II | "np II" - in case of provision of services referred to in Article 100 sec. 1 item 4 of the Act. | 55 |
| 0 EX | Export of Goods | 70 |
| oo | Domestic RC | 21 |

**Domestic overview**

| Tax Percentage | P\_12 KSeF code | Billit Ventilation Code |
| --- | --- | --- |
| 23 % | 23 | do not use ventilation code |
| 8 % | 8 | do not use ventilation code |
| 5 % | 5 | do not use ventilation code |
| 0 % (Domestic) | 0 KR | 1 |

> ❗️
>
> Ventilation Code - not on detail lines. When you have invoices lines with VAT that is zero-related (no positive VAT percentages) then the Ventilation code should be included on the header. Do not include the ventilation code on the line.

## Ventilation Codes and associated KSeF Data

FYI, Billit fills automatically in the the KSeF XML P\_13, P\_14 and P\_18 with the correct values. Below how this happens.

**Specific Polish KSeF codes for 0 %, exempt and related:**

| P\_12 KSeF code | Description | VentilCode | Summary Net P\_13 | Summary VAT P\_14 | P\_18 |
| --- | --- | --- | --- | --- | --- |
| zw | Exempt (Zwolnione) | 22 | P\_13\_7 | - | 2 |
| 0 WDT | IC Goods (WDT) | 51 | P\_13\_6\_2 | - | 2 |
| np I | provision of services article 100 sec 1 (OSS) | 104 | P\_13\_5 | - | 2 |
| np II | IC Services (EU) | 55 | P\_13\_9 | - | 1 |
| 0 EX | Export of Goods | 70 | P\_13\_6\_3 | \_ | 2 |
| oo | Domestic RC | 21 | P\_13\_11 | - | 1 |

**Domestic overview**

| Tax Percentage | P\_12 KSeF code | VentilCode | Summary Net P\_13 | Summary VAT P\_14 | P\_18 |
| --- | --- | --- | --- | --- | --- |
| 23 % | 23 | 4 | P\_13\_1 | Amount Filled | 2 |
| 8 % | 8 | 3 | P\_13\_2 | Amount Filled | 2 |
| 5 % | 5 | 2 | P\_13\_3 | Amount Filled | 2 |
| 0 % (Domestic) | 0 KR | 1 | P\_13\_6\_1 | Amount Filled | 2 |

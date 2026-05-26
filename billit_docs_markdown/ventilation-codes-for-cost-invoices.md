---
title: "Ventilation Codes for Expenditure Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ventilation-codes-for-cost-invoices"
source_slug: "ventilation-codes-for-cost-invoices"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - ventilation
  - codes
  - cost
  - invoices
  - expenditure
---

# Cost (Expenditure) related Invoices and Credit Notes

This is related to:

- Receiving Invoices and Credit Notes of Suppliers
- Sending Self-Bill invoices

What ventilation codes are allowed ?

| Billit Ventilation Code | Descr. Ventilation Code | Default Vat % | UBL TaxCategory ID | TaxExemptionReason in UBL | Peppol description |
| --- | --- | --- | --- | --- | --- |
| 1 | Binnenland (Inland) | NULL | 0% - Z<br>6%, 12%, 21% - S |  |  |
| 21 | BTW Verlegd (VAT shifted) | 0.00 | AE | Reverse charge | Vat Reverse Charge. Standard VAT rate is levied from the invoicee |
| 22 | Div. Buiten BTW (Misc. Excluding VAT) | NULL | O | Not subject to VAT | Services outside scope of tax. Taxes are not applicable to the services |
| 51 | IC Goederen (IC Goods) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services | VAT exempt for EEA intra-community supply of goods and services |
| 55 | IC Diensten (IC Services) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services | VAT exempt for EEA intra-community supply of goods and services |
| 70 | Import / Export | 0.00 | G | Free export item, VAT not charged | Free export item, VAT not charged |
| 102 | Import Via EU | NULL | E | Exempt from VAT | Exempt from Tax. |
| 111 | Marge (Margin) | 0.00 | E | Exempt from VAT | Exempt from Tax.<br>Taxes are not applicable. |

Updated2 months ago

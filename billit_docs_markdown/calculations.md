---
title: "Calculation Method"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/calculations"
source_slug: "calculations"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - calculations
  - calculation
  - method
---

# Calculation Method

Optimizing accuracy in VAT calculations is a crucial aspect of our API's functionality. Users may occasionally notice minor discrepancies, ranging from 1-10 cents, between the data submitted and the recalculated values provided by our system. This variance arises from our commitment to ensuring the highest level of accuracy in your financial transactions.

# Why Billit Prioritizes Taxable Amount-Based Calculations

Billit employs a VAT calculation method that is aligned with European Union standards, focusing on the cumulative taxable amount. This approach is recognized for its precision and is compliant with both EU directives and Belgian regulations. While Belgian businesses have the flexibility to calculate VAT per invoice line or based on the total taxable amount, we have chosen the latter for its distinct advantages:

- **Enhanced Accuracy:** By aggregating taxable amounts before applying VAT rates, we minimize rounding errors that can occur when calculating VAT for each line item separately.
- **EU Compliance:** This method aligns with EU standards, ensuring that our API is accessible and accurate for both Belgian and non-Belgian customers.
- **Simplified Cross-border Transactions:** It facilitates smoother financial operations for companies engaging in cross-border trade within the EU.

Since the EU way is more specific and correct we use that one. This also makes it easy for Non Belgian customers to use our API.

# How to Align Your Data with Billit's Calculations

To synchronize your invoicing data with Billit's calculation method, specify whether VAT-inclusive or VAT-exclusive values should govern the calculations at the order line level. This flexibility allows you to determine the primary value for each item, ensuring consistency with the overall invoice calculation.

# Comparison of Calculation Methods

Billit adopts the taxable amount-based method for VAT calculation, contrasting with the per-order-line calculation method. Below are revised examples to illustrate the differences between these approaches more clearly.

Example Invoice Lines

Consider the following invoice lines for a clearer comparison:

| Order line Title | Net Price | VAT Rate |
| --- | --- | --- |
| Drinks | €49.99 | 6% |
| Computer Mouse | €24.95 | 21% |
| Keyboard | €59.99 | 21% |

**Order Line-Based Rounding (Less Preferred) ❌**

This method calculates VAT for each line separately, potentially leading to rounding differences:

- Stationery: €49.99 + (€49.99 \* 0.06) = €52.9894 ≈ €52.99
- Computer Mouse: €24.95 + (€24.95 \* 0.21) = €30.1895 ≈ €30.19
- Keyboard: €59.99 + (€59.99 \* 0.21) = €72.5889 ≈ €72.59
- **Total: €155.77**

**Taxable Amount-Based Rounding (Billit's Method✅)**

This method aggregates items by VAT rate before calculating and applies rounding at the final step:

- Items at 21% VAT: (€24.95 + €59.99) _1.21 = (€84.94)_ 1.21 = €102.7774 ≈ €102.78
- Items at 6% VAT: €49.99 \* 1.06 = €52.9894 ≈ €52.99
- **Total: €155.76**

# Conclusion

While both methods yield the same total in this simplified example, the taxable amount-based method ensures greater accuracy and compliance with EU standards. It is particularly advantageous when dealing with fractions of currency, reducing rounding discrepancies and fostering greater consistency across financial documents.

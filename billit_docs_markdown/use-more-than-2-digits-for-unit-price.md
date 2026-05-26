---
title: "Use more than 2 digits for Unit Price"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/use-more-than-2-digits-for-unit-price"
source_slug: "use-more-than-2-digits-for-unit-price"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - use
  - more
  - than
  - digits
  - unit
  - price
---

# Use more than 2 digits for Unit Price

Billit calculates the total price in order to avoid validation errors in networks such as Peppol (more info : [https://docs.billit.be/docs/calculations](calculations.md)). In your Billit environment for unit prices 2 digits are used by default. This is very common, but sometimes automated calculation of totals by Billit can calculate a minor difference in price totals.

In order to get maximum accuracy, you can increase the number of digits after the comma. You can increase this to 3, 4 or 5 (you can send more than 5, but it will be ignored). The more digits the higher the accuracy, but of course it depends also on how many digits/decimals the invoicing software can deliver.

You can use these additional decimals for 2 elements on line level:

- Unit price exluded VAT (most important to avoid rounding errors)
- Quantity (if you have quantities with digits)

If you want to activate more decimals than 2, go to the MyBillit user interface to Settings, General, and edit:

![](https://files.readme.io/1db68fb1716773270076108de6fcdd28c5d1f08cb127bcfa46f648406e096241-afbeelding.png)

With the API you can then send unit prices with more digits on the level of invoice lines. Example:

![](https://files.readme.io/ef589b7dd27b180ac6a7e0f7889d3a2be7be756e8f6f1d676110d5c8f67dbba3-afbeelding.png)

How it will appear in the UBL :

![](https://files.readme.io/00fb49eaa8347012740b2b35729baed8bf8a10acfede8740f296c9a085b35148-2025-12-19_09-32-13.png)

Blue : maximum 2 digits. Green : 5 digits.

Updated5 months ago

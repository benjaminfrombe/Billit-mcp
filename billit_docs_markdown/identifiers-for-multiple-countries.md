---
title: "Identifiers for Multiple Countries"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/identifiers-for-multiple-countries"
source_slug: "identifiers-for-multiple-countries"
category: "reference-errors"
topics:
  - reference
  - errors
  - identifiers
  - multiple
  - countries
---

## Approach

When you have to send to multiple countries, you need to have a good approach on how to identify the customers in these countries;

The customer can be registered with one of more identifiers as a receiver.

Below some identifer types:

| Type of Identifier | Billit AP Field | More Info |
| --- | --- | --- |
| VAT Number | VATNumber |  |
| Company / Registration / Organisation number | Identifiers |  |
| Other country specific identification | Identifiers |  |
| Identifier not linked to a country | Identifiers | [https://docs.billit.be/docs/customer-has-special-identifiers](customer-has-special-identifiers.md) |

Typical approach:

- If customer has a VAT number, always include the VAT number in the API field VATNumber.
  - When customer is registered for receiving via VAT number, then this can be used as identifier for sending
  - When customer is not registered for receiving via VAT number, then this is still useful as it should be included in tax information
- If other identifiers are needed, they can be added in the identifier segment
  - One or more identiers can be added
  - If these identifiers are registered for receiving, they can be used for sending
  - The list of identifiers can be found on : [https://docs.billit.be/docs/allowed-identifiers](allowed-identifiers.md).

How to check that certain identifiers are registerd on the Peppol network

- More info : [https://docs.billit.be/docs/peppol-receiving-capabilities](peppol-receiving-capabilities.md).

Updated2 months ago

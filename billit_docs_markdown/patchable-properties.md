---
title: "Patchable Properties"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/patchable-properties"
source_slug: "patchable-properties"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - patchable
  - properties
---

# Patchable Properties

Some endpoints allow patching, others are not allowed.

Below you can find which of the endpoints allow it and which property is allowed to be patched.

# Order Endpoint

| Property Name | Property Type |
| --- | --- |
| Paid | Boolean |
| PaidDate | DateTime |
| IsSent | Boolean |
| ApprovalStatus | [Types](https://docs.billit.be/docs/party-types#order-approval-states) |
| AccountCode | String |
| InternalInfo | String |
| Invoiced | Boolean |
| AccountantVerificationNeeded | Boolean |

# Party Endpoint

| Property Name | Property Type |
| --- | --- |
| GLAccountCode | String |
| GLDefaultExpiryOffset | String |
| Nr | String |
| Email | String |
| ExternalProviderTC | String |
| ExternalProviderID | String |
| Name | String |
| CommercialName | String |
| ContactFirstName | String |
| ContactLastName | String |
| CountryCode | String (ISO CODE) |
| City | String |
| Street | String |
| StreetNumber | String |
| Zipcode | String |
| Box | String |
| Phone | String |
| Mobile | String |
| Fax | String |
| VATNumber | String |
| IBAN | String |
| Language | String |
| VATLiable | Boolean |

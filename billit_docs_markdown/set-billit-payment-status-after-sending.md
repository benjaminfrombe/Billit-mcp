---
title: "Set Billit Payment Status after Sending"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/set-billit-payment-status-after-sending"
source_slug: "set-billit-payment-status-after-sending"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - set
  - billit
  - payment
  - after
  - sending
---

# Set Billit Payment Status after Sending

Some users find in interesting to set the payment status of outgoing sales invoices in the MyBillit user interface.

This is interesting when:

- Payment is monitored in your financial software
- You use the MyBillit user interface for follow-up of your invoices. Payment status is then displayed in MyBillit, giving users additional information.

Patch Command

| Endpoint | Method | Response | Tag |
| --- | --- | --- | --- |
| /v1/order | PATCH | 200 OK | Paid |

Example of a Patch:

![](https://files.readme.io/0d1663317925761f093157dcdeb98ae1a3e09d2e9d75310201069cb53382c123-2026-03-25_08-26-50.png)

Updated2 months ago

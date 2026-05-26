---
title: "PaymentMethod"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/paymentmethod"
source_slug: "paymentmethod"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - paymentmethod
---

# PaymentMethod

Payment Method 🙅‍♂️

- is displayed in the detail screen of the Billit user interface
- allows to filter in the menu of the interface
- when exporting to excel, this info is included.

It can be used via the API via the tag "PaymentMethod"

| Endpoint | Method | Response | Tag |
| --- | --- | --- | --- |
| /v1/order | POST | 200 OK | One of the allowed values |
| /v1/order | PATCH | 200 OK | One of the allowed values |
| /v1/order | GET | 200 OK | The result |

Below the list of values

| Possible Values in API field | English Display Text in User Interface |
| --- | --- |
| Wired | Bank transfer |
| Visa | Visa/MC/Amex |
| Bancontact | Bancontact |
| Contant | Cash |
| Domiciliation | Direct Debit |
| Online | Online |
| Other | Other |
| PrivateAccount | Privately |

Updated2 months ago

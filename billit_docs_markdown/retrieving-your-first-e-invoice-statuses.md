---
title: "Webhooks for pushing e-invoice statuses"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/retrieving-your-first-e-invoice-statuses"
source_slug: "retrieving-your-first-e-invoice-statuses"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - retrieving
  - first
  - invoice
  - statuses
  - pushing
---

# Webhooks for pushing e-invoice statuses

When running a company invoice statuses are important. The power this information can grant you knowing some invoices are delivered, refused or still in progress are big. We learnt that in our API integrators from Small to big enterprises want to know this information on an almost instant possibility.

For the instant e-invoice statuses we have our Webhook option. This will send you an update when the invoice has received an update. Allowing you to instantly process the update in your platform or backend.

If you rather want to use polling to check for statuses this is also a possibility. For this you can use information explained in an earlier topic for retrieving invoice data.

# Webhook Setup

> 📘
>
> ### Testable request in Postman: 01 - Create Webhook

The webhook process can be setup in 4 Steps. Following the guide [behind this link](use-webhooks-to-catch-e-invoice-statuses.md) will set you up perfectly

An important step for webhooks are verifications that the webhook is valid and not someone pushing data to your backend. The webhooks can be validated through -> [Validate webhooks](verify-signature.md)

> 🚧
>
> ### Restrictions
>
> - Max 20 Active Webhooks
> - Wrongly used Webhooks will lead into removal of the webhook

Updated6 months ago

- [Use webhooks to catch E-Invoice statuses](use-webhooks-to-catch-e-invoice-statuses.md)
- [Verify Signature](verify-signature.md)
- [Get and Delete](get-and-delete.md)
- [/v1/webhooks](https://docs.billit.be/reference/webhook_postwebhook)
- [Refresh Webhook](https://docs.billit.be/reference/refresh-webhook)

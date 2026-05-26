---
title: "Billit API Source Docs - Webhooks For Pushing E Invoice Statuses"
updated: 2026-05-26
---

# Webhooks for pushing e-invoice statuses\n\nWhen running a company invoice statuses are important. The power this information can grant you knowing some invoices are delivered, refused or still in progress are big. We learnt that in our API integrators from Small to big enterprises want to know this information on an almost instant possibility.

For the instant e-invoice statuses we have our Webhook option. This will send you an update when the invoice has received an update. Allowing you to instantly process the update in your platform or backend.

If you rather want to use polling to check for statuses this is also a possibility. For this you can use information explained in an earlier topic for retrieving invoice data.

# Webhook Setup   [Skip link to Webhook Setup](https://docs.billit.be/docs/retrieving-your-first-e-invoice-statuses\#webhook-setup)

> ## 📘  Testable request in Postman: 01 - Create Webhook

The webhook process can be setup in 4 Steps. Following the guide [behind this link](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses) will set you up perfectly

An important step for webhooks are verifications that the webhook is valid and not someone pushing data to your backend. The webhooks can be validated through -> [Validate webhooks](https://docs.billit.be/docs/verify-signature)

> ## 🚧  Restrictions
>
> - Max 20 Active Webhooks
> - Wrongly used Webhooks will lead into removal of the webhook

Updated21 days ago

* * *

Did this page help you?

Yes

No
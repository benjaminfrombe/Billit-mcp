---
title: "Webhooks"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/webhooks"
source_slug: "webhooks"
category: "webhooks-status"
topics:
  - webhooks
  - status
---

# Webhooks

The Billit API Allows you to use Webhooks. This so your integration can listen automatically to any updates and trigger reactions.

Billit uses webhooks to notify your application when an event happens in your account. These are useful to able to catch async events such as an invoice that has been paid, updated or created.

## Webhook Entity Types

| Type | Definition |
| --- | --- |
| Order | Orders, creditnotes, deliverynotes, .... Focus on document creation and update. |
| Message | Message contains all digital Transport Types. This can contain status feedbacks and in general more details. |

## Webhook Update Types

| Type | Definition |
| --- | --- |
| I | A new entity |
| U | Updated entity |
| D | Deleted entity |

It is recommended to always add an Update type.

## How to use the Billit Webhooks

The Billit webhooks push HTTPS calls to the registered URL provided. We will send a JSON payload to your integration. This data can be used to execute actions in you backend systems.

### Steps to receive a webhook

1. Create the webhook [Webhook](https://docs.billit.be/reference/webhook)
2. Handle the returned request. This payload will provide you a Secret. This secret can be used to verify incoming webhooks
3. You can delete or retrieve webhooks via the API
4. If needed you can refresh the Secret by using the API endpoint

The Webhooks will soon be visible your web application.

## SSL

Please make sure the endpoint has an active SSL domain. We will refuse to send webhooks to non SSL endpoints.

## Webhook Signatures

All webhook messages contain a signature.

If you want to verify the signature : the signature can be decrypted by using the Secret provided when creating the webhook. More info can be found here -> [Verify Signature](verify-signature.md)

## Webhook Validity Period and Updates

Webhooks remain valid, there is no expiration date or time.

Updates that are possible:

- You can delete a webhook
- You can refresh the secret of the webhook

- [Use webhooks to catch E-Invoice statuses](use-webhooks-to-catch-e-invoice-statuses.md)
- [Verify Signature Webhook](verify-signature.md)
- [Get and Delete Webhook](get-and-delete.md)
- [/v1/webhooks](https://docs.billit.be/reference/webhook_postwebhook)
- [Refresh Webhook](https://docs.billit.be/reference/refresh-webhook)
- [/v1/webhooks](https://docs.billit.be/reference/webhook_getwebhooks)

---
title: "Billit API Source Docs - Webhooks"
updated: 2026-05-26
---

# Webhooks\n\nThe Billit API Allows you to use Webhooks. This so your integration can listen automatically to any updates and trigger reactions.

Billit usess webhooks to notify your application when an event happens in your account. These are useful to able to catch async events such as an invoice that has been paid, updated or created.

## How to use the Billit Webhooks   [Skip link to How to use the Billit Webhooks](https://docs.billit.be/docs/webhooks\#how-to-use-the-billit-webhooks)

The Billit webhooks push HTTPS calls to the registered URL provided. We will send a JSON payload to your integration. This data can be used to execute actions in you backend systems.

### Steps to receive a webhook   [Skip link to Steps to receive a webhook](https://docs.billit.be/docs/webhooks\#steps-to-receive-a-webhook)

1. Create the webhook [Webhook](https://docs.billit.be/reference/webhook)
2. Handle the returned request. This payload will provide you a Secret. This secret can be used to verify incomming webhooks
3. You can delete or retrieve webhooks via the API
4. If needed you can refresh the Secret by using the API endpoint

The Webhooks will soon be visible in the web application.

## Webhook Signatures   [Skip link to Webhook Signatures](https://docs.billit.be/docs/webhooks\#webhook-signatures)

We sign all webhooks we send out with a signature. This Signature can be decrypted by using the Secret we provided you when creating the webhook. More info can be found here -> [Verify Signature](https://docs.billit.be/docs/verify-signature)

Updatedover 1 year ago

* * *

Did this page help you?

Yes

No
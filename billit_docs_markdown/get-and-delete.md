---
title: "Get and Delete Webhook"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/get-and-delete"
source_slug: "get-and-delete"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - get
  - delete
  - webhook
---

### Get Webhook

You can check the information about your Webhoods.

When performing the GET [https://api.sandbox.billit.be/v1/webhooks](https://api.sandbox.billit.be/v1/webhooks) (example environment sandbox), a list is returned with all active webhooks for your PartyID. This allows you to verify that all your webhooks are active, and contain the right information.

### Delete Webhook

When performing the DELETE [https://api.sandbox.billit.be/v1/webhooks/9999](https://api.sandbox.billit.be/v1/webhooks/9999) (example environment sandbox), you can delete one webhook.

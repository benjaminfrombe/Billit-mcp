---
title: "Mark Inbox as Read/Confirmed (Purchase)"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/mark-inbox-as-readconfirmed-copy"
source_slug: "mark-inbox-as-readconfirmed-copy"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - mark
  - readconfirmed
  - copy
  - read
  - confirmed
  - purchase
---

# Mark Inbox as Read/Confirmed (Purchase)

Once the Invoice or CreditNote is retrieved, it can be marked as Read. R

### POST Command Inbox Confirm

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/peppol/inbox/inboxItemId/confirm | POST | OK |

When confirm is used, the Invoice or CreditNote will be removed from the list.

Remark :

Example:

| Information Element | Info |
| --- | --- |
| Post example on sandbox | POST [https://api.sandbox.billit.be/v1/peppol/inbox/69220/confirm](https://api.sandbox.billit.be/v1/peppol/inbox/69220/confirm) |
| Feedback | Status code 200 |

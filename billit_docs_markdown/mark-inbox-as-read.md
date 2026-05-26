---
title: "Mark Inbox as Read/Confirmed (Sales)"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/mark-inbox-as-read"
source_slug: "mark-inbox-as-read"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - mark
  - read
  - confirmed
  - sales
---

# Mark Inbox as Read/Confirmed (Sales)

Once the IMR and MLR files is retrieved, it can be marked as Read. Impact will be that when the item in the inbox is retrieved the next time, the item will not appear any more in the list of the inbox.

### POST Command Inbox Confirm

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/peppol/inbox/inboxItemId/confirm | POST | OK |

When confirm is used, the IMR or MLR file will be removed from the list.

Example:

| Information Element | Info |
| --- | --- |
| Post example on sandbox | POST [https://api.sandbox.billit.be/v1/peppol/inbox/69220/confirm](https://api.sandbox.billit.be/v1/peppol/inbox/69220/confirm) |
| Feedback | Status code 200 |

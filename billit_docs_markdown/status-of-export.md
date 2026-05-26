---
title: "Status of Export"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/status-of-export"
source_slug: "status-of-export"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - export
---

### Incoming Invoice is Processed in Target System

Possible methods:

- Filter on modification date with Odata
- Store the processed OrderID's in your application. This allows to check which orderID is new and not processed yet.
- Store the status in a field in Billit (via a Patch command) This is explained below.

### Store Export StatusInfo at Billit

Value that can be updated:

- Property "Is Sent".
- Possible value are true or false. Default value is false.
- Is not displayed in the My Billit Interface (cannot be modified by users).
- Update via a Patch of the OrderID : Patch [https://api.sandbox.billit.be/v1/orders/1571999](https://api.sandbox.billit.be/v1/orders/1571999) : set "IsSent" status to true.

Content of the Patch command:

Patch Is Sent status

```json
{
    "IsSent": true
 }
```

- When we request list of items still to be processed, we can include with Odata a filter based on the filter IsSent = false.
- Example: GET [https://api.sandbox.billit.be/v1/orders?$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Cost'+and+LastModified+ge+DateTime'2025-04-23'+and+IsSent+eq+false](https://api.sandbox.billit.be/v1/orders?$filter=OrderType+eq+%27Invoice%27+and+OrderDirection+eq+%27Cost%27+and+LastModified+ge+DateTime%272025-04-23%27+and+IsSent+eq+false)
- So the invoices you just have patched will not be in the list anymore.

FYI Other related fields that can also be patched:

- Internal Info : add free text
- Approval Status : do only use when approval is activated. Possible values are Approved / Pending / Rejected.

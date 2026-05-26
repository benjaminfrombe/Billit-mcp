---
title: "Billit API Source Docs - Sending Your First Sales Invoice"
updated: 2026-05-26
---

# Sending your first Sales Invoice\n\nFollowing the creation of your first invoice, the next step is to dispatch it to the recipient. Understanding that invoice delivery methods can vary significantly from one country to another and even among different customers, we've simplified the process to ensure ease and flexibility.

You can explore the various transportTypes available for sending invoices by visiting our documentation page [Transport Types](https://docs.billit.be/docs/types#transport-types). It's important to note that not all features may be available on the test network within the sandbox environment. Therefore, we recommend regularly checking our network environments documentation for the most recent updates and changes. This proactive approach helps ensure that you're always aligned with the latest capabilities and requirements for invoice delivery.

Sending the invoices can be done by 2 options:

1. Enable auto sending invoices
1. This can be found in the company settings page. Everyday at 9 am all invoices will be sent.
2. Use the command Send API endpoint
1. Use the postman request setup for sending or the description below
2. TransportTypes can be found here -> [Transport Types](https://docs.billit.be/docs/types#transport-types)

> ## 📘  Testable request in Postman: 05 - Send Sales Invoice

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders/commands/send | POST | OK |

JSON

```\1

{
    "Transporttype" : "Peppol",
    "OrderIDs" : {UniqueID, UniqueID, ....}
}

```

## Validations   [Skip link to Validations](https://docs.billit.be/docs/sending-your-first-invoice\#validations)

It is possible that you will receive validations when trying to send. These can be that the receiver is not on the Peppol network or something is not inline with network rules. You will have to adjust the invoice before sending again.

Updated21 days ago

* * *

Did this page help you?

Yes

No
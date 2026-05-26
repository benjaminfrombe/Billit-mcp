---
title: "Billit API Source Docs - Send Via Email When Delivery As Einvoice Is Not Possible"
updated: 2026-05-26
---

# Send via Email When delivery as Einvoice is not Possible\n\n## What Happens when no Einvoice Receiving is Possible   [Skip link to What Happens when no Einvoice Receiving is Possible](https://docs.billit.be/docs/email-sending-strict-transport-types\#what-happens-when-no-einvoice-receiving-is-possible)

In the Billit API, you can send your invoices using the commands/send API endpoint. This endpoint allows you to specify a transport type.

When using Peppol as the transport type,

- If the customer is registered on the Peppol network, then normal delivery via Peppol will happen.
- If the customer is not registered on the Peppol network,
  - Then alternative sending via email will be launched.
    - If no email address is available, then sending via Paper based postal service will happen. This applies to production environment, not for sandbox.
  - This might not be the desired behaviour : if the receiver is not on Einvoice network, then no delivery should happen. To activate this via "StrictTransportType", see further.

## Requirement for Alternative Sending via Email   [Skip link to Requirement for Alternative Sending via Email](https://docs.billit.be/docs/email-sending-strict-transport-types\#requirement-for-alternative-sending-via-email)

When the alternative email sending is launched, then a valid customer email address must be defined.

Remark : on einvoicing test networks such as Open/Peppol less companies are registered as a receiver than on production, so the email alternative email sending might occur more regularly.

When the email of the Receiver is not defined, then the sending will be set to error. Error info:

{"errors":\[{"Code":"TheCustomer\_0\_DoesNotHaveAValidEmailAddress","Description":"Customer XYZ does not have a valid email address"}\]}

## Avoid Sending via alternative Channel such as Email   [Skip link to Avoid Sending via alternative Channel such as Email](https://docs.billit.be/docs/email-sending-strict-transport-types\#avoid-sending-via-alternative-channel-such-as-email)

By setting the **StrictTransportType** header to **true**, the system will prevent sending the invoice via email and will instead throw a validation error if the customer is not registered on the Einvoicing network such as Peppol.

This ensures that invoices are only sent through the specified transport type, no alternatives are tried.

Below an example of the use of StrictTransportType on header level in Postman:

![](https://files.readme.io/1775f0e43d97e61e14d23383001c5a2ec8763aeda2ffc68557ea9efd2725820e-afbeelding.png)

Updated21 days ago

* * *

- [Header values](https://docs.billit.be/docs/header-values)

Did this page help you?

Yes

No
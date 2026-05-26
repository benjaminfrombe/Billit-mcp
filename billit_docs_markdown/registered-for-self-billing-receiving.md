---
title: "Self-Billing Receiver Registered on Peppol"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/registered-for-self-billing-receiving"
source_slug: "registered-for-self-billing-receiving"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - registered
  - self
  - billing
  - receiver
  - peppol
---

## When Receiver is Receiving via Billit

In Settings, General, Additional : activate the self-billing Icon. This is **mandatory** : self-bill receiving cannot happen is there is not registration for the self-bill document type.

![](https://files.readme.io/6df62c869fed0bf67a9fdc2d272e25bbf62a541750c1bdddc5121f86277353f1-2025-12-17_17-55-29.png)

This will allow:

- display the self-billing info on the user interface
- trigger the automatic Peppol registration for the receiving of the Self-billing interface

So when checking the Peppol registration with GET Participant Information, you should see the mentioning of Self-Bill invoice and CreditNote :

Result Participant Information

```json
{
    "Registered": true,
    "Identifier": "9925:BE0871169999",
    "DocumentTypes": [\
        "BISv3InvoiceSelfBilling",\
        "BISv3CreditNoteSelfBilling",\
        "IMR",\
        "MLR",\
        "BISv3CreditNote",\
        "BISv3Invoice"\
    ],
```

## When Receiver is Receiving via Another Access Point

If the receiving of Peppol documents via another Access Point then Billit:

- Make sure the document types Self-Bill Invoice and Self-bill Credit Note get registered via this Access Point.
- Check this before starting the Self-Bill sending.
- If the receiver is not registered for self-billing, contact the receiver and request the self-bill activation.

Updated3 months ago

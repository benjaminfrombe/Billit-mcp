---
title: "Billit API Source Docs - Set Invoice Number How Can I Retrieve The Next Sequence"
updated: 2026-05-26
---

# Set Invoice Number - How can I retrieve the next sequence\n\nWhen the invoice number is determined by the Source system (ERP / accounting software) then the invoice number can be communicated via the API. "OrderNumber": "20250012545"

If this OrderNumber is not determined by a non-Billit software, then the options are:

- Is automatically determined by Billit : increasing number
- Get the sequence number : When using multiple platforms to create invoices knowing the next number in the pipeline can be helpfull. This to make sure the numbers are sequential in each tool and not having any gaps between them. The [/v1/account/sequences](https://docs.billit.be/reference/account_postsequences-1) Endpoint allows you to retrieve the next sequence and even consume it if needed. The sequence types can be found under our [Types](https://docs.billit.be/docs/types) section. Consuming a sequence can be done by adding the Consume Boolean in the Post request.

Updated24 days ago

* * *

Did this page help you?

Yes

No
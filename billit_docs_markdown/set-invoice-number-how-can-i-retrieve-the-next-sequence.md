---
title: "Retrieve or Set Invoice Number"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-can-i-retrieve-the-next-sequence"
source_slug: "how-can-i-retrieve-the-next-sequence"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - set
  - invoice
  - number
  - retrieve
  - next
  - sequence
---

# Retrieve or Set Invoice Number

There are scenario's where setting the correct invoice number is clear and simple:

- API : When the invoice number is determined by the Source system (ERP / accounting software) then the invoice number can be communicated via the API based on the tag Ordernumber. Example: "OrderNumber": "20250012545"
- Manually create invoice in MyBillit Portal

For certain scenario's it may be more complex:

- Example : When using multiple platforms to create invoices then knowing the next number in the pipeline can be helpful. This to make sure the numbers are sequential in each tool and not having any gaps between them.

The [/v1/account/sequences](https://docs.billit.be/reference/account_postsequences-1) Endpoint allows you to retrieve the next sequence and even consume it if needed. The sequence types can be found under the [Types](types.md) section. Consuming a sequence can be done by adding the Consume Boolean in the Post request.

Remark : The use of the sequence is limited to sales invoices (Income).

Examples for 4 scenarios are given below. We always use POST [https://api.sandbox.billit.be/v1/account/sequences](https://api.sandbox.billit.be/v1/account/sequences)

Retrieve Invoice SequenceRetrieve Credit Note SequenceConsume Next Invoice NumberConsume Next CreditNote number

```json
{
 "SequenceType": "Income-Invoice",
 "Consume": false
}
```

```json
{
 "SequenceType": "Income-CreditNote",
 "Consume": false
}
```

```json
{
 "SequenceType": "Income-Invoice",
 "Consume": true
}
```

```json
{
 "SequenceType": "Income-CreditNote",
 "Consume": true
}
```

When Posting the next Document via POST v1/order, the OrderNumber to set can the the number that has been marked as consumed.

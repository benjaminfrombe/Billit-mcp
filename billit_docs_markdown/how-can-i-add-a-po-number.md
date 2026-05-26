---
title: "PO number : 1 or multiple PO-numbers"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-can-i-add-a-po-number"
source_slug: "how-can-i-add-a-po-number"
category: "reference-errors"
topics:
  - reference
  - errors
  - add
  - po
  - number
  - multiple
  - numbers
---

# PO number : 1 or multiple PO-numbers

A customer may ask a PO number to put as reference on your invoice.

The PO number should be added on Order header level in the property Reference.

## PO on header

PO header

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-004",
 "OrderDate": "2025-05-05",
 "ExpiryDate": "2025-05-30",
 "Reference": "45123456789", //PO Reference of the buyer on header level
}
```

Remarks:

- Put only **one** PO number in this tag.
- Only put the PO reference, not additional text.

## PO on line

Although **not** the preferred scenario with networks such as Peppol, it might be useful/needed to reference PO numbers on line level (one PO per line):

- In that case only one PO is mentioned on header level,
- and multiple on line level (one PO per line).

First option is to include PO as text in a LineNote as free text. Benefit is that it is easy to understand for a receiver:

PO LineNote

```json
                 {
                "Quantity": 3,
                 "UnitPriceExcl": 5.00,
                 "Description": "Cookies",
                 "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //Optional longer description
                 "Reference": "917865", //Supplier Article Number
                 "VATPercentage": 0,
                "CustomFields" :
         {
               "InvoiceLine.Note": "Purchase Order Number 45123456789"
        },

   }
```

Second option is to include PO in commodity classification:

- The listID PO is an offical value in the code list.
- Not all receivers may be able to process this information. So you can combine with free text in InvoiceLine.Note.
- Below example of the combination.

PO Line CommodityClassification

```json
                 {
                "Quantity": 3,
                 "UnitPriceExcl": 5.00,
                 "Description": "Cookies",
                 "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //Optional longer description
                 "Reference": "917865", //Supplier Article Number
                 "VATPercentage": 0,
                "CustomFields"     :
    {
     "CommodityClassificationPO": "45123456789",
		 "CommodityClassificationSRV": "5410355405132" ,
		 "InvoiceLine.Note": "Purchase Order Number 45123456789"
     },
   }
```

---
title: "Billit API Source Docs - How Can I Add A PO Number To An Invoice Or Multiple PO Numbers"
updated: 2026-05-26
---

# How can I add a PO number to an invoice (or multiple PO numbers)\n\nIt sometimes happens that a customer asks you to add a PO number to your invoice.

The PO number should be added on Order (root)level in the property Reference.

## PO on header   [Skip link to PO on header](https://docs.billit.be/docs/how-can-i-add-a-po-number\#po-on-header)

PO header

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-004",
 "OrderDate": "2025-05-05",
 "ExpiryDate": "2025-05-30",
 "Reference": "45123456789", //PO Reference of the buyer on header level
}

```

## PO on line   [Skip link to PO on line](https://docs.billit.be/docs/how-can-i-add-a-po-number\#po-on-line)

Although not the preferred scenario, it might be useful/needed to reference PO numbers on line level (one PO per line). In that case only one PO is mentioned on header level, and multiple on line level (one PO per line.

First option is to include PO as text in a LineNote. Benefit is that it is easy to understand for a receiver

PO LineNote

```\1

                 {
                "Quantity": 3,
                 "UnitPriceExcl": 5.00,
                 "Description": "Cookies",
                 "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //Optional longer description
                 "Reference": "917865", //Supplier Article Number
                 "VATPercentage": 0,
                "CustomFields"
    :
         {
               "InvoiceLine.Note": "Purchase Order Number 45123456789"
        },

   }

```

Second option is to include PO in commodity classification. The listID PO is an offical value in the code list (You can combine with InvoiceLine.Note).

PO Line CommodityClassification

```\1

                 {
                "Quantity": 3,
                 "UnitPriceExcl": 5.00,
                 "Description": "Cookies",
                 "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //Optional longer description
                 "Reference": "917865", //Supplier Article Number
                 "VATPercentage": 0,
                "CustomFields"
    :
         {
         "InvoiceLine.Item.CommodityClassification.ItemClassificationCode.Text":"45123456789",
         "InvoiceLine.Item.CommodityClassification.ItemClassificationCode.ListID":"PO"
        },

   }

```

Updated23 days ago

* * *

Did this page help you?

Yes

No
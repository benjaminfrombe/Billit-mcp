---
title: "Products"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/products"
source_slug: "products"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - products
---

## About Products

Within Billit, you can create products, and add information to it. Information : [https://www.billit.eu/en-int/help-page/products/add-products/](https://www.billit.eu/en-int/help-page/products/add-products/)

This allows to used products for proposals, invoices, etc.

## If you only want to send Product Info in eInvoice

If your goal is only to send invoices, and your products are managed in your ERP-software, then you do not have to store product information in Billit.

With v1/order you can fill product information directly in the message content. More info on [https://docs.billit.be/docs/create-first-invoice](creating-sales-invoices.md) and [https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support](how-can-i-add-certain-peppol-values-that-billit-json-does-not-support.md)

## Create a Product

_Currently issue with the Post, will be updated when fixed._

Sandbox command : POST [https://api.sandbox.billit.be/v1/products](https://api.sandbox.billit.be/v1/products)

You can Post 1 or multiple products with one command.

Example Json body

Create Product

```text
{
    "Items": [\
        {\
            "Reference": "Cleaning liquid",\
            "Description": "Cleaning liquid extra info",\
            "AmountExcl": 0.90000,\
            "VAT": 21.00,\
            "Unit": "NAR",\
            "GroupID": 30279,\
            "StockQuantity": 20.00,\
            "MinimumBilledQuantity": 50.0000,\
            "InternalInformation": "extra info"\
        }\
    ]
}
```

## Update a Product

In order to update a product, you can send a POST command and include the ProductID.

Example Json body:

Update Product

```text
{
    "Items": [\
        {\
        		"ProductID": 419999,  // When adding the ProductID, the existing product will be updated\
						"Reference": "Cleaning liquid",\
            "Description": "Cleaning liquid extra info",\
            "AmountExcl": 0.90000,\
            "VAT": 21.00,\
            "Unit": "NAR",\
            "GroupID": 30279,\
            "StockQuantity": 20.00,\
            "MinimumBilledQuantity": 50.0000,\
            "InternalInformation": "extra info"\
        }\
    ]
}
```

## GET Product Information

| Command (sandbox) | Info |
| --- | --- |
| GET [https://api.sandbox.billit.be/v1/products](https://api.sandbox.billit.be/v1/products) | Give complete list of products |
| GET [https://api.sandbox.billit.be/v1/products/419999](https://api.sandbox.billit.be/v1/products/419999) | Get info of one product |

## References

| What | Link |
| --- | --- |
| API Reference | [https://docs.billit.be/reference/product\_getproduct-1](https://docs.billit.be/reference/product_getproduct-1) |
| Swagger | [https://api.billit.be/swagger/ui/index#/Product](https://api.billit.be/swagger/ui/index#/Product) |

Updated6 months ago

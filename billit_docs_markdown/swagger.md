---
title: "Swagger / Readme / Datamodel"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/swagger"
source_slug: "swagger"
category: "reference-errors"
topics:
  - reference
  - errors
  - swagger
  - readme
  - datamodel
---

# Swagger / Readme / Datamodel

3 useful references / libraries are available:

- Always Start with documentation on this site
- Readme API Endpoints overview: [https://docs.billit.be/reference](https://docs.billit.be/reference) . It contains the parameters and Sample code in nearly 20 development languages.
- For a Full list of data elements use, you can looka at Swagger UI Guide [https://api.billit.be/swagger/ui/index](https://api.billit.be/swagger/ui/index). For the meaning of earch field, check on this documentation site.

## 1\. What is the Billit API

The Billit API allows you to programmatically interact with Billit’s services — such as **invoices, clients, quotes, and payments**. It is built around REST endpoints and supports standard CRUD operations (Create, Read, Update, Delete).

## 2\. API Overview and Supported Values

- First read documentation on this website.
- Then 2 additional sites are available to find detailed list of supported values:
  - API Endpoints : [https://docs.billit.be/reference/order-1](https://docs.billit.be/reference/order-1). Including sample code in 20 development languages
  - Swagger [https://api.billit.be/swagger/ui/index](https://api.billit.be/swagger/ui/index)
- Browse all available endpoints, methods, parameters, and schemas
- Use the interactive interface to test endpoints with **“Explore”**

## 3\. Common API Endpoints

While the full list is in Swagger, here are examples:

| Resource | How can it help you? |
| --- | --- |
| **Account** | - Retrieve the context of the Account (aka company) context you are operating in. [https://docs.billit.be/docs/create-new-companies](create-new-companies.md) |
| **Orders** | - Perform create, read, update, delete, or query operations on invoices, quotes, and credit notes (both income and expense).<br>- Assigning a customer or supplier to an order will either create a new party or link the order to an existing party. |
| **Party** | - Manage the **customers** and **suppliers** of an Account |

## 4\. Datamodel

More info: [https://docs.billit.be/docs/data-model](data-model.md)

Updated3 months ago

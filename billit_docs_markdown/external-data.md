---
title: "External Data"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/external-data"
source_slug: "external-data"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - external
  - data
---

# External Data

Some of our endpoints support the use of Externalprovider data:

- This allows you to store unique data from your end into Billit. Which on the other end allows you to use that data in further API calls or checks.
- When you use the GET command, you will get this information back.
- Data will not be included in the einvoicing content.
- It can be used for filtering on result lists with Odata.
- Maximum 1 occurrence is included.

Below you can see an example of the usage of this parameter.

**Party or Order**

| Field | Value |
| --- | --- |
| ExternalProviderID | Custom value |

You can add this field into any customer or order object allowing you to store this in Billit. Check out [this](odata.md) to see how to use ExternalproviderID and filter it using OData

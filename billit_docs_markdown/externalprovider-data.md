---
title: "ExternalProvider data"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/externalprovider-data"
source_slug: "externalprovider-data"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - externalprovider
  - data
---

# ExternalProvider data

Some of our endpoints support the use of Externalprovider data. This allows you to store unique data from your end into Billit. Which on the other end allows you to use that data in further API calls or checks.

Below you can see an example of the usage of this parameter.

**Party or Order**

| Field | Value |
| --- | --- |
| ExternalProviderID | Custom value |

You can add this field into any customer or order object allowing you to store this in Billit. Check out [this](odata.md) to see how to use ExternalproviderID and filter it using OData

Updated12 months ago

- [OData](odata.md)

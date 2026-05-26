---
title: "Billit API Source Docs - Odata"
updated: 2026-05-26
---

# OData\n\n# OData (Open Data Protocol)   [Skip link to OData (Open Data Protocol)](https://docs.billit.be/docs/odata\#odata-open-data-protocol)

Is an ISO certified standard that is used in rest APIs to define filters.

[Odata start guide](https://www.odata.org/getting-started/) or [Odata References](https://www.odata.org/odata-services/)

> ## 📘  Pagination
>
> Endpoints in the API that support OData such as [documents](https://docs.billit.be/reference/document_getdocuments-1), [orders](https://docs.billit.be/reference/order_getorders-1), [parties](https://docs.billit.be/reference/party_getparties-1) and [products](https://docs.billit.be/reference/product_getproducts-1) have a default pagesize op 120 records. The responses will contain a NextpageLink as long as there are still records left to be fetched.
>
> Alternatively the "&$skip={skipAmount}" filter can be used to manually go over different pages.

## Quick guide   [Skip link to Quick guide](https://docs.billit.be/docs/odata\#quick-guide)

### Apply a filter   [Skip link to Apply a filter](https://docs.billit.be/docs/odata\#apply-a-filter)

To add filters the "$filter" query param must be added. The property on which the filter must be applied is added as plain text followed by +eq+ to signify that the filter must find a record where the property value is equal to the filter value. The filter value can be added between single or double quotes. Eg. filter on the parties DisplayName: /v1/parties$filter=DisplayName+eq+'Billit'.

Multiple filters can be applied at once by chaining them with "+and+", eg. filtering on OrderType and Direction: `/v1/orders?$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Income'`

Filters can be applied to subproperties by appending a /(slash) and the subproprty eg. filter on the subproperty DisplayName of the CounterParty of an order: ` /v1/orders?$filter=CounterParty/DisplayName+eq+'Billit'`

### Apply sorting   [Skip link to Apply sorting](https://docs.billit.be/docs/odata\#apply-sorting)

Sorting is applied via the "$orderby" param and simply adding the property the sorting needs to be applied on, eg. `/v1/orders?$orderby=OrderNumber`. The default sorting is ascending, this can be reversed by adding "desc".

Sorting on subproperties is also possible and the subproperty is defined in the same way as in a filter, property/subproperty.

Multiple properties can be defined to sort on, these are added separated by a comma, eg. order on OrderNumber and then on OrderDate: ` /v1/orders?$orderby=OrderNumber, OrderDate`.

### Combine multiple query options   [Skip link to Combine multiple query options](https://docs.billit.be/docs/odata\#combine-multiple-query-options)

Multiple types of query paramters can be combined by chaining them with the & (ampersand) eg. give a top 5 of the most recent income invoice for the customer Billit: `$filter=CounterParty/DisplayName+eq+'Billit'+and+OrderType+eq+'Invoice'+and+OrderDirection+eq+'Income'`

### Limit your results   [Skip link to Limit your results](https://docs.billit.be/docs/odata\#limit-your-results)

Limit the amount of items present in the result by using the `$top={amount}`. Note: this can not be used to exceed the default page size of 120 records.

### Skip over rows   [Skip link to Skip over rows](https://docs.billit.be/docs/odata\#skip-over-rows)

A page with result will contain a maximum of 120 records by default. You can retrieve records outside of the page by using the `$skip={amout}` query param. Alternatively you can use the url provided in the NextpageLink in the result, this will always have the correct amount to not fetch any records more than once.

## Examples   [Skip link to Examples](https://docs.billit.be/docs/odata\#examples)

Let's see with some examples what OData can do for you.

**The following GET request will provide you with all changed invoices from the date provided, in this example: the first of January**

HTTP

```\1

GET /v1/orders?$filter=LastModified+ge+DateTime'2022-01-01'+and+OrderType+eq+'Invoice'&$orderby=LastModified+asc

```

You can use this on other GET endpoints too, here is an example on our Party Endpoint.

**The following GET request will provide us with all customers that were Last Modified >= 1st of January 2019, sorted**

HTTP

```\1

GET /v1/parties?$filter=PartyType+eq+'Customer'+and+LastModified+ge+DateTime'2019-01-01'&$orderby=LastModified+asc

```

**The following GET request will provide us with all products that were Last Modified >= 1st of January 2019, sorted**

HTTP

```\1

GET /v1/products?$filter=LastModified+ge+DateTime'2019-01-01'+and+GroupName+eq+'Testgroep'&$orderby=LastModified+asc

```

**The following GET request will provide us with all the orders, with an order date between 2022-01-01 and 2022-12-31**

HTTP

```\1

GET /v1/orders?$filter=OrderDate ge datetime'2022-01-01' and OrderDate le datetime'2022-12-31'

```

**The following GET request will provide us with all the orders, Using the ExternalProviderID and only returning those**

Use case: Using a POST, you stored the Unique Invoice ID from your software in Billit using the ExternalProviderID. Now you want to check if any invoices exists with that unique

ExternalProviderID . You can use the following filter.

HTTP

```\1

GET /v1/orders?$filter=ExternalProviderID+eq+'MyCustomNumber'

```

Updatedover 1 year ago

* * *

Did this page help you?

Yes

No
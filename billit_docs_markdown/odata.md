---
title: "OData for Filtering"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/odata"
source_slug: "odata"
category: "reference-errors"
topics:
  - reference
  - errors
  - odata
  - filtering
---

# OData (Open Data Protocol) Info

Is an ISO certified standard that is used in rest APIs to define filters.

Documentation sites:

[Odata start guide](https://www.odata.org/getting-started/) or [Odata References](https://www.odata.org/odata-services/)

## How to use Odata filtering at Billit

### Apply a filter

To add filters the "$filter" query param must be added. The property on which the filter must be applied is added as plain text followed by +eq+ to signify that the filter must find a record where the property value is equal to the filter value. The filter value can be added between single or double quotes.

Multiple filters can be applied at once by chaining them with "+and+", eg. filtering on OrderType and Direction: `/v1/orders?$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Income'`

Filters can be applied to subproperties by appending a /(slash) and the subproprty eg. filter on the subproperty Order of the CounterParty of an order:` /v1/orders?$filter=CounterParty/PartyID+eq+'Billit'`

### Apply Sorting

Sorting is applied via the "$orderby" param and simply adding the property the sorting needs to be applied on, eg. `/v1/orders?$orderby=OrderNumber`. The default sorting is ascending, this can be reversed by adding "desc".

Sorting on subproperties is also possible and the subproperty is defined in the same way as in a filter, property/subproperty.

Multiple properties can be defined to sort on, these are added separated by a comma, eg. order on OrderNumber and then on OrderDate:` /v1/orders?$orderby=OrderNumber, OrderDate`.

### Combine Multiple Query Options

Multiple types of query paramters can be combined by chaining them with the & (ampersand) eg. give a top 5 of the most recent income invoice for the customer Billit: `$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Income'`

### Limit your Results and Pagination

Limit the amount of items present in the result by using the `$top={amount}`. Note: this can not be used to exceed the default page size of 120 records.

> 📘
>
> ### Pagination
>
> Endpoints in the API that support OData such as [documents](https://docs.billit.be/reference/document_getdocuments-1), [orders](https://docs.billit.be/reference/order_getorders-1), [parties](https://docs.billit.be/reference/party_getparties-1) and [products](https://docs.billit.be/reference/product_getproducts-1) have a default pagesize op 120 records. The responses will contain a NextpageLink as long as there are still records left to be fetched.
>
> Alternatively the "&$skip={skipAmount}" filter can be used to manually go over different pages.

### Skip over rows

A page with result will contain a maximum of 120 records by default. You can retrieve records outside of the page by using the `$skip={amout}` query param. Alternatively you can use the url provided in the NextpageLink in the result, this will always have the correct amount to not fetch any records more than once.

## Odata Billit Examples

Let's see with some examples what OData can do for you.

**The following GET request will provide you with all changed invoices from the date provided, in this example: the first of January**

HTTP

```http
GET /v1/orders?$filter=LastModified+ge+DateTime'2022-01-01'+and+OrderType+eq+'Invoice'&$orderby=LastModified+asc
```

You can use this on other GET endpoints too, here is an example on our Party Endpoint.

**The following GET request will provide us with all customers that were Last Modified >= 1st of January 2019, sorted**

HTTP

```http
GET /v1/parties?$filter=PartyType+eq+'Customer'+and+LastModified+ge+DateTime'2019-01-01'&$orderby=LastModified+asc
```

**The following GET request will provide us with all products that were Last Modified >= 1st of January 2019, sorted**

HTTP

```http
GET /v1/products?$filter=LastModified+ge+DateTime'2019-01-01'+and+GroupName+eq+'Testgroep'&$orderby=LastModified+asc
```

**The following GET request will provide us with all the orders, with an order date between 2022-01-01 and 2022-12-31**

HTTP

```http
GET /v1/orders?$filter=OrderDate ge datetime'2022-01-01' and OrderDate le datetime'2022-12-31'
```

**The following GET request will provide us with all the orders, Using the ExternalProviderID and only returning those**

Use case: Using a POST, you stored the Unique Invoice ID from your software in Billit using the ExternalProviderID. Now you want to check if any invoices exists with that unique

ExternalProviderID . You can use the following filter.

HTTP

```http
GET /v1/orders?$filter=ExternalProviderID+eq+'MyCustomNumber'
```

## What Properties are supported for Odata filtering at Billit

Not all properties at Billit are supported for filtering, this is for performance reasons. _On 17/03/2026, some properties have been disabled for Odata filtering._

Below the list of supported properties:

- OrderID
- CounterParty/PartyID
- CompanyID
- OrderDirection
- OrderType
- OrderDate
- OrderNumber
- ExpiryDate
- ExportedToConnector
- AccountantVerificationNeeded
- TotalExcl
- TotalVAT
- TotalIncl
- FXRateToForeign
- Paid
- OrderStatus
- ExternalProviderID
- Currency
- PaymentReference
- LastModified
- Created
- ApprovalStatus
- PaidDate
- PaymentMethod
- Reference
- RemindersSent
- ExternalProvider
- IsSent

When applying Odata filtering on a property that does not allow filtering, then an error is returned:

- Response: "Code":"GenericError","Description":"Could not find a property named 'VATNumber' on type 'Domain.Order.OrderPartyPerformanceSafeColumns'."

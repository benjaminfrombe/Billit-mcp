---
title: "Billit API Source Docs - Get List Of Incoming Invoices"
updated: 2026-05-26
---

# Get List of Incoming Invoices\n\n### Get including filtering   [Skip link to Get including filtering](https://docs.billit.be/docs/get-list-of-incoming-invoices\#get-including-filtering)

The processing is similar as for sales invoices. For Sales Invoices, we refer to : [https://docs.billit.be/docs/retrieve-invoice-information](https://docs.billit.be/docs/retrieve-invoice-information)

Because you sometimes want to query on lists of invoices or retrieve purchase invoice which you do not already have a unique ID for we have our list API endpoint. This endpoint also returns a order object but less properties and it will be contained in a list.

Below the endpoint with and without Odata filtering. More info about Odata can be found here -> [Odata Info](https://docs.billit.be/docs/odata)

| Endpoint | Method | Response | Extra Info |
| --- | --- | --- | --- |
| /v1/orders | GET | List of Orders | Full list of sales and cost/expense invoices / credit notes |
| /v1/orders?$filter=OrderType+eq+'Invoice'+and+OrderDirection+eq+'Cost' | GET | With Odata | Full list of sales and cost/expense invoices / credit notes |
| v1/orders?$filter=OrderType+eq+'Invoice'+and+<br>OrderDirection+eq+'Cost'+and+<br>LastModified+ge+DateTime'2025-04-01' | GET | With Odata | List of sales and cost/expense invoices / credit notes, filtered on modification date. |

For date filtering use the modification date. For Incoming invoices, time difference between CreationDate and Modification Date is small.

### Result main info   [Skip link to Result main info](https://docs.billit.be/docs/get-list-of-incoming-invoices\#result-main-info)

The first return values of the Json body are:

Json First fields

```\1

{
    "Items": [\
        {\
            "OrderID": 1077603,\
            "CompanyID": 574991,\
            "OrderPDF": {\
                "FileID": "28acb9ee-d0b1-4ee9-8a9d-2317712a9a11"\
            },\
            "OrderNumber": "QS-Contact2",\
\
```\
\
Explanation:\
\
- OrderID : the unique Billit ID of the document , to use for the next steps.\
- CompanyID : The Billit ID of the receiving company.\
- OrderPDF : Billit ID of the linked file.\
- OrderNumber : the Invoice or CreditNote number of the supplier.\
\
The Json result contains a selection of the data, the full data are obtained when getting one specific document (next step)\
\
Updatedabout 1 month ago\
\
* * *\
\
Did this page help you?\
\
Yes\
\
No
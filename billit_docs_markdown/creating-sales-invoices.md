---
title: "Billit API Source Docs - Creating Sales Invoices"
updated: 2026-05-26
---

# Creating Sales Invoices\n\nCreating the first invoice is that illuminating moment when you think, _"Aha! This is how it works!"_ Understanding the significance of this experience, we've streamlined the process to make it as straightforward as possible.

No need for multiple calls to create the invoice or additional development to accommodate various e-invoice networks. Everything is consolidated into one simple endpoint.

As you will see in the example there is no need to first create the customer and then the invoice. We will try and find an existing customer based on VAT, Email, Address, CustomerNr if enabled. if not we will auto create a new one for you saving the hassle for the extra API Call.

Link to Postman collection -> [(Create First Invoice)](https://www.postman.com/billit/workspace/billit-quickstart-guide/request/13542996-850bc833-38fc-4ab9-8d9d-744a75d3ce85)

When the Postman or the information below is successfully implemented you can start creating invoices as much as you want. No limits! Running Bulk invoice runs or continuous runs this is how you handle it!

# Information Scenario 1 : Simple   [Skip link to Information Scenario 1 : Simple](https://docs.billit.be/docs/create-first-invoice\#information-scenario-1--simple)

Below you can find the Endpoint used and the JSON for creating a basic invoice. By executing this request you will receive a _**Unique ID**_. This ID indicates **success** together with the **200 response code**, we advice storing the Unique ID onto your own invoice Object or references to this invoice.

When sending, Billit will generate the appropriate output file, many items are added automatically. About totals (line totals, global totals) calculations are done by Billit. This avoids validation issues with total amounts e.g. due to rounding. More information on the total calculations can be found [here](https://docs.billit.be/docs/calculations)

The example below will create a **Sales invoice** this can be seen by the following properties.

| Property | Value | Info |
| --- | --- | --- |
| OrderType | Invoice | Indicating the invoice type. "Invoice", "CreditNote",... |
| OrderDirection | Income | Indicating the direction for the company. "Income" (sales), "Cost" (Expense) |

The Metadata of the invoice is stored in the following properties.

| Property | Value | Info |
| --- | --- | --- |
| OrderNumber | QS-001 | Invoice number, Unique invoice identifier, used by the seller.... |
| OrderDate | 2025-05-01 | The issue date of the invoice |
| ExpiryDate | 2025-06-30 | Due date. The date where the invoice is due for payment by the recipient |
| Reference | 45123456789 | PO (Purchase Order) reference of the buyer |
| PaymentReference | 012/9999/61525 | Value to use by buyer as a reference in the payment. Can be structured payment reference or other non-structured payment identification such as invoice number. |
| Customer | Object | Customer information |
| Orderlines | List | The products, invoiceable items, .... |

Customer Object

| Property | Value | Info |
| --- | --- | --- |
| Name | Billit | Commercial Name, DisplayName, ... |
| VATNumber | BE0563846944 | Taxnumber for the company |
| PartyType | Customer | **Customer** for Sales invoices, **Supplier** for Purchase invoices |
| Identifiers | Object | List of idenitifiers for the customer outside of the Unique Taxnumber |
| Addresses | List | List of addresse for the customer |

OrderLines Object

| Property | Value | Info |
| --- | --- | --- |
| Quantity | 1 | The amount to quantify with |
| UnitPriceExcl | 10.0 | The NET price of the line |
| Description | Box of cookies | The title of the line |
| DescriptionExtended | Box of cookies 20 pieces, 200 g | Optional longer description |
| Reference | 915025 | Supplier Article Number |
| VATPercentage | 6.0 | Percentage of tax to be added on the line |

# API Request - Simple Scenario - Create Sales Invoice   [Skip link to API Request - Simple Scenario  - Create Sales Invoice](https://docs.billit.be/docs/create-first-invoice\#api-request---simple-scenario----create-sales-invoice)

> ## 📘  Testable request in Postman: 01 - Create Sales Invoice

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders | Post | INT (Unique OrderID) |

With the following minimum content a valid einvoice can be sent in many networks.

Json body Post

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-001",
 "OrderDate": "2024-01-01",
 "ExpiryDate": "2024-01-31",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003732007"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}

```

# API Request - Scenario 2 - More Info   [Skip link to API Request - Scenario 2  - More Info](https://docs.billit.be/docs/create-first-invoice\#api-request---scenario-2----more-info)

json

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-006",
 "OrderDate": "2024-01-01",
 "ExpiryDate": "2024-01-31",
 "Reference": "45123456789", //PO Reference of the buyer
 "PaymentReference": "+++012/3623/61525+++", //Can be structured payment reference or other non-structured payment identification such as invoice number.  If you fill this field, then you can the OGM filled by Billit will be replaced by your value"
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",\
        "Identifier": "5430003732007"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies",\
   "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //Optional longer description, confirmed\
   "Reference": "915025", //Supplier Article Number, confirmed\
   "VATPercentage": 6\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21\
   }\
 ]
}

```

# API Request - Scenario 3 - Using Additional Fields   [Skip link to API Request - Scenario 3  - Using Additional Fields](https://docs.billit.be/docs/create-first-invoice\#api-request---scenario-3----using-additional-fields)

Much more fields are supported. They are explained on the page: [https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support](https://docs.billit.be/docs/how-can-i-add-certain-peppol-values-that-billit-json-does-not-support)

# API Request - Scenario 4 - Adding Files   [Skip link to API Request - Scenario 4  - Adding Files](https://docs.billit.be/docs/create-first-invoice\#api-request---scenario-4----adding-files)

When no file is included in the Json by the sender, then a PDF attachment will be generated by Billit and included in the file (this applies to most networks, including Peppol).

When the sender wants to include an own file attachment, then this is possible.

Below Example of including the PDF Invoice:

Add PDF.

```\1

{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-033a",
 "OrderDate": "2025-04-09",
 "ExpiryDate": "2025-04-30",
  "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
    },
  "Customer": {


```

```\1

```

For more scenarios and options, se details page : [Link](https://docs.billit.be/docs/how-can-i-save-a-file)

# Validations   [Skip link to Validations](https://docs.billit.be/docs/create-first-invoice\#validations)

> ## 📘  Testable request in Postman: 02 - Validation Example

The Billit platform will validate your data before processing it into Billit. Therefor you could potentially run into one of these while building. A response can look like the following for example when using a wrong VAT percentage for the country you are invoicing from.

JSON

```\1

{
    "errors": [\
        {\
            "Code": "InvalidVAtPercentageForTaxCountry_0_",\
            "Description": "Invalid VAT percentage for country code BE"\
        }\
    ]
}

```

Updated21 days ago

* * *

Did this page help you?

Yes

No
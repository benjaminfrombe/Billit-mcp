---
title: "Creating Sales Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/create-first-invoice"
source_slug: "create-first-invoice"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - creating
  - sales
---

# Creating Sales Invoices

Creating the first invoice is that illuminating moment when you think, _"Aha! This is how it works!"_ Understanding the significance of this experience, we've streamlined the process to make it as straightforward as possible.

No need for multiple calls to create the invoice or additional development to accommodate various e-invoice networks. Everything is consolidated into one simple endpoint.

As you will see in the example there is no need to first create the customer and then the invoice. We will try and find an existing customer based on VAT, Email, Address, CustomerNr if enabled. if not we will auto create a new one for you saving the hassle for the extra API Call.

Link to Postman collection -> [(Create First Invoice)](https://www.postman.com/billit/workspace/billit-quickstart-guide/request/13542996-850bc833-38fc-4ab9-8d9d-744a75d3ce85)

When the Postman or the information below is successfully implemented you can start creating invoices as much as you want. No limits! Running Bulk invoice runs or continuous runs this is how you handle it!

# Information Scenario 1 : Simple

Below you can find the Endpoint used and the JSON for creating a basic invoice. By executing this request you will receive a _**Unique ID**_. This ID indicates **success** together with the **200 response code**, we advice storing the Unique ID onto your own invoice Object or references to this invoice.

When sending, Billit will generate the appropriate output file, many items are added automatically. About totals (line totals, global totals) calculations are done by Billit. This avoids validation issues with total amounts e.g. due to rounding. More information on the total calculations can be found [here](calculations.md)

The example below will create a **Sales invoice** this can be seen by the following properties.

| Property | Value | Info |
| --- | --- | --- |
| OrderType | Invoice | Indicating the invoice type. "Invoice", "CreditNote",... |
| OrderDirection | Income | Indicating the direction for the company. "Income" (sales), "Cost" (Expense) |

The Metadata of the invoice is stored in the following properties (the main information elements).

| Property | Value | Info |
| --- | --- | --- |
| OrderNumber | QS-001 | Invoice number, Unique invoice identifier, used by the seller. |
| OrderDate | 2025-05-01 | The issue date of the invoice |
| ExpiryDate | 2025-06-30 | Due date. The date where the invoice is due for payment by the recipient |
| DeliveryDate | 2025-04-30 | Date of the delivery of the goods (Delivery Date) |
| Reference | 2025-04-30 | PO (Purchase Order) reference of the buyer. Include one one is this field, without additional text. |
| OrderTitle | 20259875 | BuyerReference : reference mentioned by the buyer (other then Purchase Order - Reference) |
| PaymentReference | 012/9999/61525 | Value to use by buyer as a reference in the payment. Can be structured payment reference or other non-structured payment identification such as invoice number. |
| Currency | EUR | When no currency is mentioned, Billit sets the currency to Euro. Fill in an ISO value, e.g. USD |

Customer Object

| Property | Value | Info |
| --- | --- | --- |
| Name | Billit | Commercial Name, DisplayName, ... |
| VATNumber | BE0563846944 | Taxnumber for the company |
| PartyType | Customer | **Customer** for Sales invoices, **Supplier** for Purchase invoices |
| Identifiers | Object | List of idenitifiers for the customer outside of the Unique Taxnumber |
| Addresses | List<Object> | List of address for the customer |

OrderLines Object

| Property | Value | Info |
| --- | --- | --- |
| Quantity | 1 | The amount to quantify with (by default 2 decimals, can be extended to 5) |
| UnitPriceExcl | 10.0 | The NET price of the line, excl. VAT (by default 2 decimals, can be extended to 5) |
| Description | Box of cookies | The title of the line. This description is typically shorter as Description Extended. Can support 512 characters, recommended is less. |
| DescriptionExtended | Box of cookies 20 pieces, 200 g | Optional longer description. Can support 512 characters. If you want to add more information, see Extra Fields : InvoiceLine.Note for a third fields with free text descriptions. |
| Reference | 915025 | Supplier Article Number |
| VATPercentage | 6.0 | Percentage of tax to be added on the line |

# API Request - Simple Scenario - Create Sales Invoice

> 📘
>
> ### Testable request in Postman: 01 - Create Sales Invoice

| Endpoint | Method | Response |
| --- | --- | --- |
| /v1/orders | Post | INT (Unique OrderID) |

With the following sample content a valid einvoice can be sent in many networks.

Json body Post

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-001",
 "OrderDate": "2025-09-01",
 "DeliveryDate": "2025-08-30",
 "ExpiryDate": "2025-10-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Email" : "piet.pieters@telenet.be",  //Useful when sending via email is done
   "Language" : "NL",  // Language can be useful when an email is sent
   "Phone" : "+3292035699",  // Customer Phone
   "Nr": "5624871",  //Customer number from ERP, shown in Billit customer data, not in Einvoice message
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",  //Only when additional identifiers must be added\
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
        "Zipcode" : "9001",\
        "Box": "box1",  // Postal box in the building"\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
				"Zipcode": "9001",\
        "Box": "301",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.0,\
   "Description": "Box of cookies", // In peppol will come in the field "Name"\
   "DescriptionExtended": "Box of cookies 20 pieces, 200 g", //In peppol will come in the field "Description"\
   "Reference": "915025", //Supplier Article Number\
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

# API Request - Scenario 2 - More Info

json

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-006",
 "OrderDate": "2024-01-01",
 "ExpiryDate": "2024-01-31",
 "Reference": "45123456789", //PO Reference of the buyer
  "OrderTitle": "565987522", //Other Reference of a buyer
 "Currency": "EUR",  // If not mentioned, currency is EUR by default
 "PaymentReference": "+++012/3623/61525+++", //Can be structured payment reference or other non-structured payment identification such as invoice number.  If you fill this field, then you can the OGM filled by Billit will be replaced by your value"
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
    "PartyType": "Customer",
   "Nr": "3487" //The customer number of your invoicing system, to store as an information element in Billit customer overview
   "Identifiers": [\
        {\
        "IdentifierType": "GLN",  // optional additional identifier\
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

# API Request - Scenario 3 - Using Additional Fields (Advanced)

Much more fields are supported. They are explained on the next pages.

# Validations

> 📘
>
> ### Testable request in Postman: 02 - Validation Example

The Billit platform will validate your data before processing it into Billit. Therefor you could potentially run into one of these while building. A response can look like the following for example when using a wrong VAT percentage for the country you are invoicing from.

JSON

```json
{
    "errors": [\
        {\
            "Code": "InvalidVAtPercentageForTaxCountry_0_",\
            "Description": "Invalid VAT percentage for country code BE"\
        }\
    ]
}
```

# When you Send for Multiple Companies

- [x]  If you send for multiple companies, make sure you put the correct PartyID of the correct company in the header. When you send a list of ID's, it can only be ID's of that specific company
- [x]  With the command send API you are able to send invoices to over transport Types. [Types](types.md)

- [Extra Fields : Extend Content (Header)](how-can-i-add-certain-peppol-values-that-billit-json-does-not-support.md)
- [Extra Fields : Supplier and Customer Contacts](extra-fields-supplier-and-customer-contacts.md)
- [Extra Fields : Extend Content (Line)](extra-fields-extend-content-with-extra-values-line.md)
- [How can I add a PO number to an invoice (or multiple PO's) numbers)](how-can-i-add-a-po-number.md)

---
title: "Customer is Private Person"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/customer-is-private-person"
source_slug: "customer-is-private-person"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - customer
  - private
  - person
---

## Customer Info in MyBillit Interface

Result in detail screen of Customer in the MyBillit portal (advanced details screen has been selected)

![](https://files.readme.io/f37ccbc27f69758eaeff66fcbb5a9759c9c35875a74f06af0cbe6240e6c2bdf2-2025-12-08_08-22-56.png)

Additional Info:

1. PartyID of the Customer (Technical ID)
2. Private person is not marked automatically in user interface of MyBillit customer screen (limitation, but not causing practical problems)
3. VAT number, company number is empty. Person is marked as not subject to VAT
4. Customer number communicated via API
5. Email address of the private person

## What to include in Invoice Data When Customer is Private

How to make sure that customer is created only once:

- When posting the invoice, make sure that customer data are included in the correct way (see sample below)
  - Email Address
  - Name
  - Customer number (optional)
  - IBAN,BIC (optional)
  - flags VATLiable, VATDeductable (not mandatory, goal is to make it clearer in customer overview)
- Alternative Solution : Create customer before:
  - Create
    - via Exel upload
    - or via API,
  - Get the PartyID of the customer (via API, or read on the screen)
  - Post invoice including Party ID of the invoice

Examples (with IBAN and with PartyID)

Post incl IBAN CustomerPost incl PartyID

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-X016Private1",
 "OrderDate": "2025-12-08",
 "ExpiryDate": "2025-12-30",
  "Customer": {
    "PartyType": "Customer", //Receiver of the Sales Invoice
    "Nr": "449", //This is the functional customer number (not the technical ID of the Party)
    "Name": "Jean Deboeuf2",
    "IBAN" : "BE1352308128999",  //Valid IBAN and BIC important to avoid customer duplication when no PartyID is included
    "BIC" : "TRIOBEBB",  //Valid IBAN and BIC important to avoid customer duplication
    "VATLiable": false,  //flag on user interface will be set to false
    "VATDeductable" : false, //flag on user interface will be set to false
    "Language": "NL",
    "Street" : "Teststraat ",
    "Streetnumber" : "56",
    "box":"301", // Not mandatory
    "Zipcode" : "9001",
    "Phone" : "+3224600999",
    "City" : "Gent",
    "CountryCode" : "BE",
    "Email" : "Jean.deboeuf2@telenet.be"//unique email is recommended
   },
 "OrderLines": [\
  {\
   "Quantity": 1.02,\
   "UnitPriceExcl": 10.03,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-X016Private1",
 "OrderDate": "2025-12-08",
 "ExpiryDate": "2025-12-30",
  "Customer": {
    "PartyType": "Customer", //Receiver of the Sales Invoice
		"PartyID": 879263,  //This is the ID of the customer, so will be linked to this unique customer
    "Nr": "449", //This is the functional customer number (not the technical ID of the Party)
    "Name": "Jean Deboeuf2",
    "IBAN" : "BE1352308128999",
    "BIC" : "TRIOBEBB",
    "VATLiable": false,  //flag on user interface will be set to false
    "VATDeductable" : true, //flag on user interface will be set to false
    "Language": "NL",
    "Street" : "Teststraat ",
    "Streetnumber" : "56",
    "box":"301", // Not mandatory
    "Zipcode" : "9001",
    "Phone" : "+3224600364",
    "City" : "Gent",
    "CountryCode" : "BE",
    "Email" : "Jean.deboeuf2@telenet.be"
   },
 "OrderLines": [\
  {\
   "Quantity": 1.02,\
   "UnitPriceExcl": 10.03,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

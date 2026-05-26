---
title: "Companies"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/create-new-companies"
source_slug: "create-new-companies"
category: "reference-errors"
topics:
  - reference
  - errors
  - create
  - new
  - companies
---

## Create Company via API

You can created new companies:

- Via the MyBillit Interface
- Via the API endpoint v1/account

Creation via API can be useful:

- Many companies to create
- All data are available in you source system (ERP, accounting, invoicing)

Elements you can include in

About this POST command, URL and header level:

| Information Element | Value | Description |
| --- | --- | --- |
| Endpoint Sandbox | POST [https://api.sandbox.billit.be/v1/account/registercompany](https://api.sandbox.billit.be/v1/account/registercompany) | Register 1 company on Billit Sandbox |
| Endpoint Production | POST [https://api.sandbox.billit.be/v1/account/registercompany](https://api.sandbox.billit.be/v1/account/registercompany) | Register 1 company on Billit Production |
| PartyID | Example : "6547897" | The company you create is related to the partyID of that account. The user of that account has automatically access to the newly created account. |
| Endpoint Reference Documentation | [https://docs.billit.be/reference/account\_registercompany-1](https://docs.billit.be/reference/account_registercompany-1) | Overview of parameters with sample code |
| Endpoint Info Swagger | [https://api.billit.be/swagger/ui/index#!/Account/Account\_RegisterCompany](https://api.billit.be/swagger/ui/index#!/Account/Account_RegisterCompany) | Full swagger reference |
| Header extra | Accept: application/json |  |

Information Elements that can be included for the creation:

| Information | Description |
| --- | --- |
| Company/Name | Company Name is the main name to use |
| Company/CommercialName | Commercial name is for on PDF templates |
| Address/AddressType | Is mainly used for the Invoicing Address. Separate delivery address can be used. |
| Email | This email will be used to verify the company. |
| Contact First / Last Name | Name on the My company screen of Billit. |
| VAT Number of the Company | Company identification based on VAT number |
| Phone/Mobile | Main phone numbers of supplier : Phone (mandatory) and mobile. |
| VAT Liable / Deductible | If not included, then default value is yes for both. |
| Language | Language of the company |
| BankAccounts | Ability to add bankaccount |
| AccountSettings | Some default settings for the company. More info see below |

Below an example of a Json body for a company to create:

Create Company Basic

```json
{
  "Company": {
    "Name": "Testcompany5",
    "CommercialName": "Testcompany5",

 "Addresses": [\
      {\
        "AddressType": "InvoiceAddress",  //This appears in invoice address only\
        "Tav": "Piet",\
        "Name": "Pieters",\
        "Street": "Teststreet",\
        "StreetNumber": "117",\
        "Box": "2",\
        "Zipcode": "9000",\
        "City": "Gent",\
        "CountryCode": "BE",\
        "Phone": "+329999994"\
      }\
    ],
    "Email": "hector.plessers@company.eu",  //must be unique, is email in my company, not the user.
    "ContactFirstName": "Hector",
    "ContactLastName": "Plessers",  //Last name manager
    "VATNumber": "BE0758643532",
    "Phone": "+3292365981",
    "Mobile": "+32479589898",
    "VATLiable": true,
    "VATDeductable": true,
    "Language": "NL"
  },
  "BankAccounts": [\
        {\
          "IBAN": "BE2073405499956",\
          "BIC": "KREDBEBB"\
        }\
      ],
  "AccountSettings": {
    "BulkInputFastForward": true,
    "SendPeppolInvoiceReceivedMail": true,
    "BulkInputIncomeUBLFastForward": true
  }
}
```

## Set AccountSettings

With the POST command [https://api.sandbox.billit.be/v1/account/registercompany](https://api.sandbox.billit.be/v1/account/registercompany) account settings can be included. Info below.

| Element |  |
| --- | --- |
| BulkInputFastForward | Default : is disabled. |
| SendPeppolInvoiceReceivedMail | For all incomings supplier invoices, send email notification to user. Default : is disabled. |
| BulkInputIncomeUBLFastForward | When income documents are upload via user interface, Email or sFTP they come first in fast input. With this parameter, this is skipped. Default value : is disabled. When using API, this parameter has no importance. |

## GET Company Information

| Information Element | Value | Description |
| --- | --- | --- |
| Endpoint Sandbox | GET [https://api.sandbox.billit.be/v1/account/accountInformation](https://api.sandbox.billit.be/v1/account/accountInformation) | GET information of all companies |
| Endpoint Production | POST [https://api.sandbox.billit.be/v1/account/accountInformation](https://api.sandbox.billit.be/v1/account/accountInformation) | GET information of all companies |
| Endpoint Reference Documentation | [https://docs.billit.be/reference/account\_getaccountinformation-1](https://docs.billit.be/reference/account_getaccountinformation-1) | Overview of parameters with sample code |
| Endpoint Info Swagger | [https://api.billit.be/swagger/ui/index#!/Account/Account\_GetAccountInformation](https://api.billit.be/swagger/ui/index#!/Account/Account_GetAccountInformation) | Full swagger reference |
| Header extra | Accept: application/json |  |
| PartyID | Example : "6547897" | Include Party ID of one company in the header, as only information will be returned based on access control. When key linked to party ID is correct, then info for all companies with access for this user will be returned. |

Sample returned information:

```undefined
{
    "Email": "ivanv@billit.eu",
    "Companies": [\
        {\
            "TabNameAlias": "VILBOX",\
            "APIAllowed": true,\
            "APIEnabledFeatures": {\
                "TimeRegistration": true,\
                "Projects": true,\
                "DailyReceipts": false,\
                "FinancialReduction": false,\
                "GLAccounts": false,\
                "Cashbook": false\
            },\
            "UserLanguage": "EN",\
            "PartyID": 574991,\
            "BookYearStart": "2025-01-01T00:00:00",\
            "Name": "VILBOX BV",\
            "Addresses": [\
                {\
                    "AddressType": "InvoiceAddress",\
                    "Name": "VILBOX BV",\
                    "Street": "Linthoutstraat",\
                    "StreetNumber": "31",\
                    "Box": "box1",\
                    "Zipcode": "1785",\
                    "City": "Merchtem",\
                    "CountryCode": "BE"\
                },\
                {\
                    "AddressType": "DeliveryAddress",\
                    "Name": "VILBOX BV",\
                    "Street": "Linthoutstraat",\
                    "StreetNumber": "31",\
                    "Box": "box2",\
                    "Zipcode": "1785",\
                    "City": "Merchtem",\
                    "CountryCode": "BE"\
                }\
            ],\
            "VATNumber": "BE0437295202",\
            "VATLiable": true,\
            "Users": [],\
            "Role": "Professional",\
            "VATDeductable": true,\
            "Identifiers": [],\
            "DefaultCurrencyTC": "EUR",\
            "SendUBL": true,\
            "SendPDF": true\
        },\
        },\
}\
```\
\
Remarks:\
\
- The returned information does not contain other information.\
- Information about roles is included in the second part of the returned information.\
- User and Identifier section is always empty.\
\
## EDIT/Delete Company Information\
\
The following elements are currently not possible via API, it can be done via the MyBillit user interface:\
\
- Modification and deactivation of the company\
- Registration on einvoice network (Peppol and others)\
\
Updated 6 months ago\
\
* * *\
\
Did this page help you?\
\
Yes\
\
No\
\

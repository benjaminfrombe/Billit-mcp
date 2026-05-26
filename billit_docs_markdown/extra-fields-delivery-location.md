---
title: "Extra Fields : Delivery Location"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/extra-fields-delivery-location"
source_slug: "extra-fields-delivery-location"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - extra
  - fields
  - delivery
  - location
---

## Including Delivery Location in the Customer Segment

There are 2 methods for including the delivery location:

- Method 1: The delivery information is the Customer Segment
  - The AddressType must be "DeliveryAddress"
  - When the output file type is UBL: In order to have the delivery address included in the output UBL, at least one element must be different in the AddressType "DeliveryAddress" compared to the AddressType "InvoiceAddress".
- Method 2 : via separate Custom Fields (see next point)

Below an example with the data that can be used for delivery location.

Json body Post Customer Segment Including Delivery

```json
{
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Email" : "piet.pieters@telenet.be",
   "Language" : "NL",
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
        "Zipcode" : "9001",\
        "Box": "box1",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address.  In order to include Delivery location as a separate segment in the output UBL file, make sure that at least 1 element is different from Invoice Address, e.g. the delivery name.\
        "Name": "Billit Delivery",  //the name is different compared to InvoiceAddress : delivery location will be included\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",  // Optional, this can also be included in the street name.\
        "City": "Ghent",\
				"Zipcode": "9001",\
        "Box": "301",  // Postal box in the building, optional\
        "CountryCode": "BE"\
        }\
   ]
   }
```

## Including Delivery Location via separate Custom Fields

Use of these specific fields:

1. More Advanced Delivery Information

- Set a delivery location ID. This can be useful to give an specific numeric value known by the customer. In addition it can be a standardised value (GLN number for delivery location)
- Set the Name of the delivery location and the address details, result :
  - It will appear in a correct way in the output file (typically UBL)
  - It will not appear on MyBillit Screen or on Billit Human Readable and in the customer info

2. Do not link with delivery information in customer data of Billit
1. When Posting invoice, the customer data in Billit will not be updated (keep customer data unchanged)
2. Avoid when posting multiple invoices at the same time for the same customer, that delivery data are mixed.

Data structure:

| Key (Header) | Linked Info When Peppol | Extra Information |
| --- | --- | --- |
| Invoice.Delivery.DeliveryLocation.ID.Text | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cbc-ID/) | A number or reference for the delivery location |
| Invoice.Delivery.DeliveryLocation.ID.SchemeID | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cbc-ID/) | A structured value, for GLN number this is 0088 |
| Invoice.Delivery.DeliveryLocation.Address.StreetName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-StreetName/) | Street delivery location (Including street number) |
| Invoice.Delivery.DeliveryLocation.Address. AdditionalStreetName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-AdditionalStreetName/) | Second streed field |
| Invoice.Delivery.DeliveryLocation.Address.CityName | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-CityName/) | Delivery City |
| Invoice.Delivery.DeliveryLocation.Address.PostalZone | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-PostalZone/) | Delivery Zip |
| Invoice.Delivery.DeliveryLocation.Address.CountrySubentity | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cbc-CountrySubentity/) | Delivery country sub entity (e.g. province) |
| Invoice.Delivery.DeliveryLocation.Address.Country. IdentificationCode.Text | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryLocation/cac-Address/cac-Country/cbc-IdentificationCode/) | Delivery Country code (e.g. BE, FR, NL. Remark : when using this section, country is **mandatory** ! |
| Invoice.Delivery.DeliveryParty.PartyName.Name | [Link](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-Delivery/cac-DeliveryParty/cac-PartyName/cbc-Name/) | The Name of the Delivery Party. This is a free description. This must be included to make it valid. |

Exemples with only Delivery location identification. The other delivery data can be put in the Customer Segment. Two scenario's :

- first example: only added element is GLN number (the address via the address in the customer segment)
- Delivery location id added without GLN-number

Deliverylocation GLN NumberDeliverylocation not standardised

```json
"CustomFields"  : {
    "Invoice.Delivery.DeliveryLocation.ID.Text": "5430009861001", //(GLN number)
    "Invoice.Delivery.DeliveryLocation.ID.SchemeID": "0088" //0088 refers to GLN
    },
```

```text
"CustomFields"  : {
    "Invoice.Delivery.DeliveryLocation.ID.Text": "96587452", //This is a specific delivery location number, not according to a standard such as GLN)
    },
```

Example with full delivery address and a delivery location ID:

Full Delivery Address

```json
 "CustomFields"  : {
    "Invoice.Delivery.DeliveryLocation.ID.Text": "543000985477", //Delivery Location Number (GLN number)
    "Invoice.Delivery.DeliveryLocation.ID.SchemeID": "0088", //0088 is referring to scheme ID of type GLN
    "Invoice.Delivery.DeliveryLocation.Address.Country.IdentificationCode.Text": "BE",
    "Invoice.Delivery.DeliveryLocation.Address.PostalZone": "9000",
    "Invoice.Delivery.DeliveryLocation.Address.StreetName": "Octrooiplein 1b",
    "Invoice.Delivery.DeliveryLocation.Address.AdditionalStreetName": "Extra info street",
    "Invoice.Delivery.DeliveryLocation.Address.CityName": "Gent",
    "Invoice.Delivery.DeliveryLocation.Address.CountrySubentity": "Oost-Vlaanderen",
    "Invoice.Delivery.DeliveryParty.PartyName.Name": "Billit Reception of Goods Gent"
    },
```

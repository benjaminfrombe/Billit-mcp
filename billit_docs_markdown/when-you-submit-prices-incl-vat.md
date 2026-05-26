---
title: "When You Submit Prices incl VAT"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/when-you-submit-prices-incl-vat"
source_slug: "when-you-submit-prices-incl-vat"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - submit
  - prices
  - incl
  - vat
---

# When You Submit Prices incl VAT

When your invoicing is working basis on prices including VAT, you may be missing exact information about the pricing excl. VAT. In that case Billit will generate line prices excluding VAT.

Line Fields to use:

| Line Properties | Signification | Sample value | Mandatory |
| --- | --- | --- | --- |
| InclLeading | Parameter indicating that amounts on line should be calculated starting from the total line amount incl. VAT or not | true | yes |
| TotalIncl | Total Line Amount including VAT. Alternative is to include the "UnitPriceIncl" | 149.8 | yes |
| VATPercentage | VAT % on line used for calculating the price without VAT | 21 | yes |

Example of Json content:

InclLeading Json

```json
{
	"OrderNumber": "25458752",
	"OrderDate": "2025-09-03",
	"ExpiryDate": "2025-10-03",
	"OrderType": "Invoice",
  "OrderDirection": "Income",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE0563846944",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode" : "9001",\
        "Box": "box1",\
        "Language" : "NL",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
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
     "Customer": {
   "Name": "Customer Company Name",
   "VATNumber": "BE0759529999",
   "PartyType": "Customer",
   "Identifiers": [\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0759529999"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "NP Noord West Brabant",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1a",\
        "City": "Ghent",\
        "Box": "301",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "NP Noord West Brabant1",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "Zipcode" : "9001",\
        "Box": "b",\
        "CountryCode": "BE"\
        }\
   ]
   },
	"OrderLines": [\
		{\
			"Quantity": 10.0,\
			"Description": "Product Description",\
			"VATPercentage": 21.0,  // VAT Percentage\
      "InclLeading": true,  //Indicating the we start from price including VAT\
			"TotalIncl": 149.8  // Total Price of Line incl. VAT\
		}\
	]
}
```

Result in Peppol UBL (green : calculated by Billit)

![](https://files.readme.io/ddd5a24b6fd5a693ef1f61df76df92e2e96bfccfeefe8af2de27ca9aec82a650-2025-12-11_14-40-32.png)

Updated3 months ago

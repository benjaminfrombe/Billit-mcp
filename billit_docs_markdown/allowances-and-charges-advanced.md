---
title: "Allowances and Charges"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/allowances-and-charges-advanced"
source_slug: "allowances-and-charges-advanced"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - allowances
  - charges
  - advanced
---

## Concepts

For discounts, some easy to use allowances are pre-defined to make it easier, more info : [https://docs.billit.be/docs/discount-with-simple-billit-fields](discount-with-simple-billit-fields.md).

If you want to add other specific costs or discounts, then this is possible.

About allowances and charges:

- An allowance is a discount. A charge is an additional cost that is added.

- Use on Peppol, see Peppol documenation [https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/tree/](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/tree/).

- Are supported at Billit in Peppol on header level and on line level. Not on price level.

- Only supported when generated via API.

- Multiple allowances and/or charges can be included (multiple on header and multiple on line).

- Works for invoices and credit notes.

- Maximum number of digits/decimals in allowance / charge amounts is **2**.

- When you want to use an allowance : set it as an allowance, use positive amounts (the amount reduction is communicated as positive amount).

## How it works (Header Level)

You can add your own Allowances and Charges in the Json body payload. When using the Peppol network or when sending UBL files, Billit will then include the allowances and charges in the UBL file.

For each header based allowance/charge 5 information elements need to be filled:

| Tag | Description | Possible Values | Mandatory |
| --- | --- | --- | --- |
| Quantity | Typical value is 1, as on header level quantity is not included. If value is more than 1, Billit will use it to calculate the total amount. | 1 | yes |
| UnitPriceExcl | Unit Price, positive when specifying a charge, negative when specifying an allowance | Amount | yes |
| Description | This value will be used to fill the value "AllowanceChargeReason" in the Peppol UBL | Free text | yes |
| Code | This value will be used to fill the value "AllowanceChargeReasonCode" in the Peppol UBL. Must be present in the official Peppol list [https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5189/](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5189/) | Free text | no |
| VATPercentage | This is the VAT Percentage of the allowance / charge, it can be different from the other VAT percentages of the allowance / charge | eg. 21 | yes |
| AllowanceChargeIndicator | true is a charge, false is an allowance (discount) | true / false | yes |

Remarks about the use of Allowances and Charges at Billit on header level:

- [x]  Is placed as an additional line in the body. Due to the tag "AllowanceChargeIndicator" Billit knows it will be a header allowance charge.
- [x]  Tax rate when using allowance/charge on header level.
- [x]  Multiple allowances and charges on header level are supported.
- [x]  Maximum number of digits/decimals in allowance / charge amounts is 2.

Not allowed:

- [x]  Do not use TotalExcl, TotalVAT, TotalIncl on line level in a line with an allowance or a charge.
- [x]  Do not add other fields in the Allowance charge section.

## Examples Allowances and Charges on Header Level (Json)

1 Allowance on Header Json1 Allowance on Header UBL1 Charge on Header Json1 Allowance + 1 Charge Header Json

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-Chv2_1",
 "OrderDate": "2025-11-05",
 "OrderTitle": "Allowance on header",
 "ExpiryDate": "2025-11-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE05638469442",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 5, //\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
     {\
   "Quantity": 1, // Normal quantity is 1\
   "UnitPriceExcl": -2.00, //Amount, for allowance must be negative\
   "Description": "Global discount",  // This is the allowance reason (description)\
   "VATPercentage": 21, // VAT percentage can be different from the other lines\
   "AllowanceChargeIndicator" : false //Indicates this line has allowance/charge.  false : it is an allowance, not a charge.\
   }\
  ]
}
```

```xml
<?xml version="1.0"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>QS-Chv2_1</cbc:ID>
  <cbc:IssueDate>2025-11-05</cbc:IssueDate>
  <cbc:DueDate>2025-11-30</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>Allowance on header</cbc:BuyerReference>
  <cac:OrderReference>
    <cbc:ID>45lr7etz4784</cbc:ID>
  </cac:OrderReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0437295999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0437295999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>TESTSUPPLIER</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Kerkstraat 31 box1</cbc:StreetName>
        <cbc:CityName>Merchtem</cbc:CityName>
        <cbc:PostalZone>1785</cbc:PostalZone>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>BE0437295999</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>TESTSUPPLIER</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Piet Pieters</cbc:Name>
        <cbc:Telephone>+3224600999</cbc:Telephone>
        <cbc:ElectronicMail>Piet.Pieters999@gmail.com</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0563846944</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0563846944</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>Billit</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Oktrooiplein 1</cbc:StreetName>
        <cbc:CityName>Ghent</cbc:CityName>
        <cbc:PostalZone>9000</cbc:PostalZone>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>BE0563846944</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>Billit</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0563846944</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Billit</cbc:Name>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:Delivery>
    <cbc:ActualDeliveryDate>2025-11-05</cbc:ActualDeliveryDate>
    <cac:DeliveryLocation>
      <cac:Address>
        <cbc:StreetName>Oktrooiplein 1b</cbc:StreetName>
        <cbc:CityName>Ghent</cbc:CityName>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:Address>
    </cac:DeliveryLocation>
    <cac:DeliveryParty>
      <cac:PartyName>
        <cbc:Name>Vilbox</cbc:Name>
      </cac:PartyName>
    </cac:DeliveryParty>
  </cac:Delivery>
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    <cbc:PaymentID>+++218/2135/58110+++</cbc:PaymentID>
    <cac:PayeeFinancialAccount>
      <cbc:ID>BE20734054285956</cbc:ID>
      <cac:FinancialInstitutionBranch>
        <cbc:ID>KREDBEBB</cbc:ID>
      </cac:FinancialInstitutionBranch>
    </cac:PayeeFinancialAccount>
  </cac:PaymentMeans>
  <cac:AllowanceCharge>
    <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>Global discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="EUR">2.00</cbc:Amount>
    <cac:TaxCategory>
      <cbc:ID>S</cbc:ID>
      <cbc:Percent>21.00</cbc:Percent>
      <cac:TaxScheme>
        <cbc:ID>VAT</cbc:ID>
      </cac:TaxScheme>
    </cac:TaxCategory>
  </cac:AllowanceCharge>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">2.58</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">50.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">3.00</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>6.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">-2.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">-0.42</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
  </cac:TaxTotal>
  <cac:LegalMonetaryTotal>
    <cbc:LineExtensionAmount currencyID="EUR">50.00</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">48.00</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">50.58</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">2.00</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">50.58</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">5.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">50.00</cbc:LineExtensionAmount>
    <cac:OrderLineReference>
      <cbc:LineID>915025</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
      <cbc:Name>Box of cookies</cbc:Name>
      <cac:SellersItemIdentification>
        <cbc:ID>915025</cbc:ID>
      </cac:SellersItemIdentification>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>6.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">10.00000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
```

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-Charge1a",
 "OrderDate": "2025-11-05",
 "OrderTitle": "Charge on header",
 "ExpiryDate": "2025-11-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE05638469442",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 5,\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
     {\
   "Quantity": 1, // Assumed to be 1\
   "UnitPriceExcl": 4.00, //amount of the charge (must be positive)\
   "Description": "Fuel surcharge",  // This is the charge reason (description)\
   "VATPercentage": 21,\
   "AllowanceChargeIndicator" : true //Indicates this line has allowance/charge.  true : it is an charge\
   }\
  ]
}
```

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-AllChv2_11",
 "OrderDate": "2025-11-05",
 "OrderTitle": "kost lijn, kost+discount header multi vat",
 "Reference": "45lrv17z7784",
 "ExpiryDate": "2025-11-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE05638469442",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
    {\
   "Quantity": 5, //\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6\
   },\
     {\
   "Quantity": 1, // header charge\
   "UnitPriceExcl": 1.69,\
   "Description": "Fuel surcharge",\
   "VATPercentage": 21,\
   "AllowanceChargeIndicator" : true\
   },\
    {\
   "Quantity": 1, // header discount\
   "UnitPriceExcl": -1.61,\
   "Description": "Globaldiscount",\
   "VATPercentage": 6,\
   "AllowanceChargeIndicator" : false\
   }\
     ]
}
```

## How it works (Detail Line Level)

For each line based allowance/charge 6 information elements need to be filled:

| Tag | Description | Possible Values | Mandatory |
| --- | --- | --- | --- |
| Quantity | Typical value is 1, as on header level quantity is not included. If value is more than 1, Billit will use it to calculate the total amount. | 1 | yes |
| UnitPriceExcl | Unit Price, positive when specifying a charge, negative when specifying an allowance | Amount | yes |
| Description | This value will be used to fill the value "AllowanceChargeReason" in the Peppol UBL | Free text | yes |
| Code | This value will be used to fill the value "AllowanceChargeReasonCode" in the Peppol UBL. Must be present in the official Peppol list for allowances [https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5189/](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5189/) and for charges [https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL7161/](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL7161/) | From code list | no |
| VATPercentage | We reuse the VAT percentage of the linked product line | e.g. 21 | yes |
| AllowanceChargeIndicator | True is a charge, false is an allowance (discount) | true / false | yes |
| LinkedOrderLineID | This GUID is put in the allowance/charge line and in the corresponding product line. it allows to link both. Any link will work, but we recommend GUID for uniqueness. | ed786cb6-c21b-4421-b8d4-7d2e914b81d9 | yes |

Remarks about the use of Allowances and Charges at Billit on line level:

- [x]  Works in the Peppol network and when sending UBL files via email.
- [x]  Tax rate of allowance/charge on line is the **same** as the tax rate of the line.
- [x]  Multiple allowances and charges on line level are supported.

Not allowed:

- [x]  Do not use TotalExcl, TotalVAT, TotalIncl on line level in a line with an allowance or a charge.
- [x]  Do not add other fields in the Allowance charge section. It is limited to the fields mentioned in the documentation.
- [x]  when multiple line allowances and charges are linked to 1 invoice line, then VAT rate must be the same as the one on the line for all allowances/charges linked to that invoice line

## Special Case : 1 header Charge, no Invoice Lines

Special scenario:

- 1 header charge
- no other invoice lines

In that case, the invoice cannot be sent.

In order to fix this :

- keep the header charge
- add 1 dummy invoice line, with amount 0

```undefined
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-Charge_line0",
 "OrderDate": "2026-04-27",
 "ExpiryDate": "2026-06-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE05638469442",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "CountryCode": "BE"\
        },\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 0.00, //line with amount 0\
   "Reference": "915025",\
   "Description": "No regular products, just a fuel surcharge as cost",\
   "VATPercentage": 21\
   },\
     {\
   "Quantity": 1, //\
   "UnitPriceExcl": 4.00,\
   "Description": "Fuel surcharge",\
   "VATPercentage": 21,\
   "AllowanceChargeIndicator" : true\
   }\
  ]
}
```

## Examples Allowances and Charges on Line Level (Json)

Allowance Line JsonAllowanceLineUBLCharge line Json

```json
{
 "OrderType": "Invoice",
 "OrderDirection": "Income",
 "OrderNumber": "QS-Allow_1",
 "OrderDate": "2025-11-05",
 "OrderTitle": "discount on line",
 "ExpiryDate": "2025-11-30",
  "Customer": {
   "Name": "Billit",
   "VATNumber": "BE05638469442",
   "PartyType": "Customer",
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
 "OrderLines": [\
  {\
   "Quantity": 1, //\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 21,\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9"\
   },\
     {\
   "Quantity": 1, // Normal quantity is 1\
   "UnitPriceExcl": -2.00, //Amount, for allowance must be negative\
   "Description": "Global discount",  // This is the line allowance reason (description)\
   "VATPercentage": 21,  // Use same VAT % als the product line\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9",  // allows to link the line allowance with the product line\
   "AllowanceChargeIndicator" : false  //this is the Allowance charge part.  As it is false, it is an Allowance.\
   },\
}\
```\
\
```xml\
<?xml version="1.0"?>\
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">\
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>\
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>\
  <cbc:ID>QS-Allow_1</cbc:ID>\
  <cbc:IssueDate>2025-11-05</cbc:IssueDate>\
  <cbc:DueDate>2025-11-30</cbc:DueDate>\
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>\
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\
  <cbc:BuyerReference>discount on line</cbc:BuyerReference>\
  <cac:OrderReference>\
    <cbc:ID>QS-Allow_1</cbc:ID>\
  </cac:OrderReference>\
  <cac:AccountingSupplierParty>\
    <cac:Party>\
      <cbc:EndpointID schemeID="0208">0437295999</cbc:EndpointID>\
      <cac:PartyIdentification>\
        <cbc:ID schemeID="0208">0437295999</cbc:ID>\
      </cac:PartyIdentification>\
      <cac:PartyName>\
        <cbc:Name>TESTSUPPLIER</cbc:Name>\
      </cac:PartyName>\
      <cac:PostalAddress>\
        <cbc:StreetName>Kerkstraat 31 box1</cbc:StreetName>\
        <cbc:CityName>Merchtem</cbc:CityName>\
        <cbc:PostalZone>1785</cbc:PostalZone>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:PostalAddress>\
      <cac:PartyTaxScheme>\
        <cbc:CompanyID>BE0437295999</cbc:CompanyID>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:PartyTaxScheme>\
      <cac:PartyLegalEntity>\
        <cbc:RegistrationName>TESTSUPPLIER</cbc:RegistrationName>\
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>\
      </cac:PartyLegalEntity>\
      <cac:Contact>\
        <cbc:Name>Piet Pieters</cbc:Name>\
        <cbc:Telephone>+3224600999</cbc:Telephone>\
        <cbc:ElectronicMail>Piet.Pieters999@gmail.com</cbc:ElectronicMail>\
      </cac:Contact>\
    </cac:Party>\
  </cac:AccountingSupplierParty>\
  <cac:AccountingCustomerParty>\
    <cac:Party>\
      <cbc:EndpointID schemeID="0208">0563846944</cbc:EndpointID>\
      <cac:PartyIdentification>\
        <cbc:ID schemeID="0208">0563846944</cbc:ID>\
      </cac:PartyIdentification>\
      <cac:PartyName>\
        <cbc:Name>Billit</cbc:Name>\
      </cac:PartyName>\
      <cac:PostalAddress>\
        <cbc:StreetName>Oktrooiplein 1</cbc:StreetName>\
        <cbc:CityName>Ghent</cbc:CityName>\
        <cbc:PostalZone>9000</cbc:PostalZone>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:PostalAddress>\
      <cac:PartyTaxScheme>\
        <cbc:CompanyID>BE0563846944</cbc:CompanyID>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:PartyTaxScheme>\
      <cac:PartyLegalEntity>\
        <cbc:RegistrationName>Billit</cbc:RegistrationName>\
        <cbc:CompanyID schemeID="0208">0563846944</cbc:CompanyID>\
      </cac:PartyLegalEntity>\
      <cac:Contact>\
        <cbc:Name>Billit</cbc:Name>\
      </cac:Contact>\
    </cac:Party>\
  </cac:AccountingCustomerParty>\
  <cac:Delivery>\
    <cbc:ActualDeliveryDate>2025-11-05</cbc:ActualDeliveryDate>\
    <cac:DeliveryLocation>\
      <cac:Address>\
        <cbc:StreetName>Oktrooiplein 1b</cbc:StreetName>\
        <cbc:CityName>Ghent</cbc:CityName>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:Address>\
    </cac:DeliveryLocation>\
    <cac:DeliveryParty>\
      <cac:PartyName>\
        <cbc:Name>Vilbox</cbc:Name>\
      </cac:PartyName>\
    </cac:DeliveryParty>\
  </cac:Delivery>\
  <cac:PaymentMeans>\
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>\
    <cbc:PaymentID>+++152/4799/52874+++</cbc:PaymentID>\
    <cac:PayeeFinancialAccount>\
      <cbc:ID>BE20734054285956</cbc:ID>\
      <cac:FinancialInstitutionBranch>\
        <cbc:ID>KREDBEBB</cbc:ID>\
      </cac:FinancialInstitutionBranch>\
    </cac:PayeeFinancialAccount>\
  </cac:PaymentMeans>\
  <cac:TaxTotal>\
    <cbc:TaxAmount currencyID="EUR">1.68</cbc:TaxAmount>\
    <cac:TaxSubtotal>\
      <cbc:TaxableAmount currencyID="EUR">8.00</cbc:TaxableAmount>\
      <cbc:TaxAmount currencyID="EUR">1.68</cbc:TaxAmount>\
      <cac:TaxCategory>\
        <cbc:ID>S</cbc:ID>\
        <cbc:Percent>21.00</cbc:Percent>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:TaxCategory>\
    </cac:TaxSubtotal>\
  </cac:TaxTotal>\
  <cac:LegalMonetaryTotal>\
    <cbc:LineExtensionAmount currencyID="EUR">8.00</cbc:LineExtensionAmount>\
    <cbc:TaxExclusiveAmount currencyID="EUR">8.00</cbc:TaxExclusiveAmount>\
    <cbc:TaxInclusiveAmount currencyID="EUR">9.68</cbc:TaxInclusiveAmount>\
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>\
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>\
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>\
    <cbc:PayableAmount currencyID="EUR">9.68</cbc:PayableAmount>\
  </cac:LegalMonetaryTotal>\
  <cac:InvoiceLine>\
    <cbc:ID>1</cbc:ID>\
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>\
    <cbc:LineExtensionAmount currencyID="EUR">8.00</cbc:LineExtensionAmount>\
    <cac:AllowanceCharge>\
      <cbc:ChargeIndicator>false</cbc:ChargeIndicator>\
      <cbc:AllowanceChargeReason>Global discount</cbc:AllowanceChargeReason>\
      <cbc:Amount currencyID="EUR">2.00</cbc:Amount>\
    </cac:AllowanceCharge>\
    <cac:Item>\
      <cbc:Name>Box of cookies</cbc:Name>\
      <cac:SellersItemIdentification>\
        <cbc:ID>915025</cbc:ID>\
      </cac:SellersItemIdentification>\
      <cac:ClassifiedTaxCategory>\
        <cbc:ID>S</cbc:ID>\
        <cbc:Percent>21.00</cbc:Percent>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:ClassifiedTaxCategory>\
    </cac:Item>\
    <cac:Price>\
      <cbc:PriceAmount currencyID="EUR">10.00000</cbc:PriceAmount>\
      <cbc:BaseQuantity>1</cbc:BaseQuantity>\
    </cac:Price>\
  </cac:InvoiceLine>\
</Invoice>\
```\
\
```json\
{\
 "OrderType": "Invoice",\
 "OrderDirection": "Income",\
 "OrderNumber": "QS-Allow_1",\
 "OrderDate": "2025-11-05",\
 "OrderTitle": "discount on line",\
 "ExpiryDate": "2025-11-30",\
  "Customer": {\
   "Name": "Billit",\
   "VATNumber": "BE05638469442",\
   "PartyType": "Customer",\
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]\
   },\
 "OrderLines": [\
  {\
   "Quantity": 41,\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 21,\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9"\
   },\
     {\
   "Quantity": 1,\
   "UnitPriceExcl": 2.00,\
   "Description": "Global discount",\
   "VATPercentage": 21,\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9",\
   "AllowanceChargeIndicator" : true\
   }\
   ]\
}\
```\
\
## Examples Allowances and Charges Header + Line (Json)\
\
Charge Header - Allowance Line JsonCharge Header - Allowance Line UBL\
\
```json\
{\
 "OrderType": "Invoice",\
 "OrderDirection": "Income",\
 "OrderNumber": "QS-AllChv2_1",\
 "OrderDate": "2025-11-04",\
 "OrderTitle": "1 charge header and 1 discount line",\
  "Reference": "45lr7etz4784",\
 "ExpiryDate": "2025-11-30",\
  "Customer": {\
   "Name": "Billit",\
   "VATNumber": "BE05638469442",\
   "PartyType": "Customer",\
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Zipcode": "9000",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress",\
        "Name": "Billit",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]\
   },\
 "OrderLines": [\
  {\
   "Quantity": 1, //\
   "UnitPriceExcl": 10.00,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6,\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9"\
   },\
     {\
   "Quantity": 1,\
   "UnitPriceExcl": -2.00,\
   "Reference": "915025",\
   "Description": "Product Discount",\
   "VATPercentage": 6,\
   "LinkedOrderLineID" : "ed786cb6-c21b-4421-b8d4-7d2e914b81d9",\
   "AllowanceChargeIndicator" : false //Allowane on line\
   },\
     {\
   "Quantity": 1,\
   "UnitPriceExcl": 4.00,\
   "Reference": "915025",\
   "Description": "Fuel surcharge",\
   "VATPercentage": 21,\
   "AllowanceChargeIndicator" : true //Charge on header\
   }\
}\
```\
\
```xml\
<?xml version="1.0"?>\
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">\
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>\
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>\
  <cbc:ID>QS-AllCh12</cbc:ID>\
  <cbc:IssueDate>2025-11-05</cbc:IssueDate>\
  <cbc:DueDate>2025-11-30</cbc:DueDate>\
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>\
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\
  <cbc:BuyerReference>1 charge header and 1 discount line</cbc:BuyerReference>\
  <cac:OrderReference>\
    <cbc:ID>QS-AllCh12</cbc:ID>\
  </cac:OrderReference>\
   <cac:AccountingSupplierParty>\
    <cac:Party>\
      <cbc:EndpointID schemeID="0208">0437295999</cbc:EndpointID>\
      <cac:PartyIdentification>\
        <cbc:ID schemeID="0208">0437295999</cbc:ID>\
      </cac:PartyIdentification>\
      <cac:PartyName>\
        <cbc:Name>TESTSUPPLIER</cbc:Name>\
      </cac:PartyName>\
      <cac:PostalAddress>\
        <cbc:StreetName>Kerkstraat 31 box1</cbc:StreetName>\
        <cbc:CityName>Merchtem</cbc:CityName>\
        <cbc:PostalZone>1785</cbc:PostalZone>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:PostalAddress>\
      <cac:PartyTaxScheme>\
        <cbc:CompanyID>BE0437295999</cbc:CompanyID>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:PartyTaxScheme>\
      <cac:PartyLegalEntity>\
        <cbc:RegistrationName>TESTSUPPLIER</cbc:RegistrationName>\
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>\
      </cac:PartyLegalEntity>\
      <cac:Contact>\
        <cbc:Name>Piet Pieters</cbc:Name>\
        <cbc:Telephone>+3224600999</cbc:Telephone>\
        <cbc:ElectronicMail>Piet.Pieters999@gmail.com</cbc:ElectronicMail>\
      </cac:Contact>\
    </cac:Party>\
  </cac:AccountingSupplierParty>\
\
  <cac:AccountingCustomerParty>\
    <cac:Party>\
      <cbc:EndpointID schemeID="0208">0563846944</cbc:EndpointID>\
      <cac:PartyIdentification>\
        <cbc:ID schemeID="0208">0563846944</cbc:ID>\
      </cac:PartyIdentification>\
      <cac:PartyName>\
        <cbc:Name>Billit</cbc:Name>\
      </cac:PartyName>\
      <cac:PostalAddress>\
        <cbc:StreetName>Oktrooiplein 1</cbc:StreetName>\
        <cbc:CityName>Ghent</cbc:CityName>\
        <cbc:PostalZone>9000</cbc:PostalZone>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:PostalAddress>\
      <cac:PartyTaxScheme>\
        <cbc:CompanyID>BE0563846944</cbc:CompanyID>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:PartyTaxScheme>\
      <cac:PartyLegalEntity>\
        <cbc:RegistrationName>Billit</cbc:RegistrationName>\
        <cbc:CompanyID schemeID="0208">0563846944</cbc:CompanyID>\
      </cac:PartyLegalEntity>\
      <cac:Contact>\
        <cbc:Name>Billit</cbc:Name>\
      </cac:Contact>\
    </cac:Party>\
  </cac:AccountingCustomerParty>\
  <cac:Delivery>\
    <cbc:ActualDeliveryDate>2025-11-05</cbc:ActualDeliveryDate>\
    <cac:DeliveryLocation>\
      <cac:Address>\
        <cbc:StreetName>Oktrooiplein 1b</cbc:StreetName>\
        <cbc:CityName>Ghent</cbc:CityName>\
        <cac:Country>\
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>\
        </cac:Country>\
      </cac:Address>\
    </cac:DeliveryLocation>\
    <cac:DeliveryParty>\
      <cac:PartyName>\
        <cbc:Name>Billit</cbc:Name>\
      </cac:PartyName>\
    </cac:DeliveryParty>\
  </cac:Delivery>\
  <cac:PaymentMeans>\
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>\
    <cbc:PaymentID>+++128/4689/06718+++</cbc:PaymentID>\
    <cac:PayeeFinancialAccount>\
      <cbc:ID>BE20734054285956</cbc:ID>\
      <cac:FinancialInstitutionBranch>\
        <cbc:ID>KREDBEBB</cbc:ID>\
      </cac:FinancialInstitutionBranch>\
    </cac:PayeeFinancialAccount>\
  </cac:PaymentMeans>\
  <cac:AllowanceCharge>\
    <cbc:ChargeIndicator>true</cbc:ChargeIndicator>\
    <cbc:AllowanceChargeReason>Fuel surcharge</cbc:AllowanceChargeReason>\
    <cbc:Amount currencyID="EUR">4.00</cbc:Amount>\
    <cac:TaxCategory>\
      <cbc:ID>S</cbc:ID>\
      <cbc:Percent>21.00</cbc:Percent>\
      <cac:TaxScheme>\
        <cbc:ID>VAT</cbc:ID>\
      </cac:TaxScheme>\
    </cac:TaxCategory>\
  </cac:AllowanceCharge>\
  <cac:TaxTotal>\
    <cbc:TaxAmount currencyID="EUR">1.32</cbc:TaxAmount>\
    <cac:TaxSubtotal>\
      <cbc:TaxableAmount currencyID="EUR">8.00</cbc:TaxableAmount>\
      <cbc:TaxAmount currencyID="EUR">0.48</cbc:TaxAmount>\
      <cac:TaxCategory>\
        <cbc:ID>S</cbc:ID>\
        <cbc:Percent>6.00</cbc:Percent>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:TaxCategory>\
    </cac:TaxSubtotal>\
    <cac:TaxSubtotal>\
      <cbc:TaxableAmount currencyID="EUR">4.00</cbc:TaxableAmount>\
      <cbc:TaxAmount currencyID="EUR">0.84</cbc:TaxAmount>\
      <cac:TaxCategory>\
        <cbc:ID>S</cbc:ID>\
        <cbc:Percent>21.00</cbc:Percent>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:TaxCategory>\
    </cac:TaxSubtotal>\
  </cac:TaxTotal>\
  <cac:LegalMonetaryTotal>\
    <cbc:LineExtensionAmount currencyID="EUR">8.00</cbc:LineExtensionAmount>\
    <cbc:TaxExclusiveAmount currencyID="EUR">12.00</cbc:TaxExclusiveAmount>\
    <cbc:TaxInclusiveAmount currencyID="EUR">13.32</cbc:TaxInclusiveAmount>\
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>\
    <cbc:ChargeTotalAmount currencyID="EUR">4.00</cbc:ChargeTotalAmount>\
    <cbc:PrepaidAmount currencyID="EUR">4.00</cbc:PrepaidAmount>\
    <cbc:PayableAmount currencyID="EUR">9.32</cbc:PayableAmount>\
  </cac:LegalMonetaryTotal>\
  <cac:InvoiceLine>\
    <cbc:ID>1</cbc:ID>\
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>\
    <cbc:LineExtensionAmount currencyID="EUR">8.00</cbc:LineExtensionAmount>\
    <cac:AllowanceCharge>\
      <cbc:ChargeIndicator>false</cbc:ChargeIndicator>\
      <cbc:AllowanceChargeReason>Product Discount</cbc:AllowanceChargeReason>\
      <cbc:Amount currencyID="EUR">2.00</cbc:Amount>\
    </cac:AllowanceCharge>\
    <cac:Item>\
      <cbc:Name>Box of cookies</cbc:Name>\
      <cac:SellersItemIdentification>\
        <cbc:ID>915025</cbc:ID>\
      </cac:SellersItemIdentification>\
      <cac:ClassifiedTaxCategory>\
        <cbc:ID>S</cbc:ID>\
        <cbc:Percent>6.00</cbc:Percent>\
        <cac:TaxScheme>\
          <cbc:ID>VAT</cbc:ID>\
        </cac:TaxScheme>\
      </cac:ClassifiedTaxCategory>\
    </cac:Item>\
    <cac:Price>\
      <cbc:PriceAmount currencyID="EUR">10.00000</cbc:PriceAmount>\
      <cbc:BaseQuantity>1</cbc:BaseQuantity>\
    </cac:Price>\
  </cac:InvoiceLine>\
</Invoice>\
```\
\
Updated 29 days ago\
\
* * *\
\
- [Cash Discount with Allowances Charges](cash-discount-with-allowances-charges.md)\
\
Did this page help you?\
\
Yes\
\
No\
\

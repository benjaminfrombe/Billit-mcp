---
title: "Cash Discount with Allowances Charges"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/cash-discount-with-allowances-charges"
source_slug: "cash-discount-with-allowances-charges"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - cash
  - discount
  - allowances
  - charges
---

# Cash Discount with Allowances Charges

You can Calculate your own Financial Discount Using Allowances and Charges.

This allows:

- to set the amount of the cash discount (not based on a percent).
- to set the information depending on the cash discount rules in the country.

Information that can be set via the API, below example based on country Belgium.

| Charge/Discount | Description |
| --- | --- |
| Header Discount | Amount of the financial discount, with tax rate e.g. 21 % |
| Header Charge | The financial discount is also calculated as a charge, with tax rate of 0 %. This allows to set the tax base in a correct way. |

You can also add text descriptions about the financial discount in the API conten

| Field | Description |
| --- | --- |
| Comments | General Information Field : easy to read for the receiver / Included on th Billit human readble |
| Payment Terms (custom field) | Allows to include the information in the payment terms section |

Below the example:

API Json ExampleGenerated UBL

```json
{
   "OrderNumber": "19854812",
   "Comments": "Till 16.12.2025 you get 2,000  % payment discount - Till 06.02.2026 without discount",  //General Comment Field, will appear on human readable of Billit
   "Reference": "4500999013",
   "OrderDate": "2025-12-08T00:00:00",
   "ExpiryDate": "2026-02-06T00:00:00",
   "OrderType": "Invoice",
   "OrderDirection": "Income",
   "CustomFields": {
		"PaymentTerms": "Till 16.12.2025 you get 2,000  % payment discount - Till 06.02.2026 without discount"// Text description in the Payment segment
	},
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
			"Quantity": 1,\
			"UnitPriceExcl": 1317.43,\
			"Reference": "85468",\
			"Description": "Regular Product",\
			"VATPercentage": 21.0\
		},\
		{\
			"Quantity": 1.0,\
			"UnitPriceExcl": -26.35,\
			"Description": "Cash discount",\
			"VATPercentage": 21.0,\
			"AllowanceChargeIndicator": false  // this is a discount with 21 % VAT\
		},\
		{\
			"Quantity": 1.0,\
			"UnitPriceExcl": 26.35,\
			"Description": "Cash discount",\
			"VATPercentage": 0.0,\
			"AllowanceChargeIndicator": true // this is a charge with 0 % VAT\
		}\
	]
	}
```

```xml
<?xml version="1.0"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>19854812</cbc:ID>
  <cbc:IssueDate>2025-12-08</cbc:IssueDate>
  <cbc:DueDate>2026-02-06</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:Note>Till 16.12.2025 you get 2,000  % payment discount - Till 06.02.2026 without discount</cbc:Note>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>N/A</cbc:BuyerReference>
  <cac:OrderReference>
    <cbc:ID>4500999013</cbc:ID>
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
    <cbc:ActualDeliveryDate>2025-12-08</cbc:ActualDeliveryDate>
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
        <cbc:Name>Billit</cbc:Name>
      </cac:PartyName>
    </cac:DeliveryParty>
  </cac:Delivery>
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    <cbc:PaymentID>+++854/8121/55042+++</cbc:PaymentID>
    <cac:PayeeFinancialAccount>
      <cbc:ID>BE30310176357911</cbc:ID>
      <cac:FinancialInstitutionBranch>
        <cbc:ID>BBRUBEBB</cbc:ID>
      </cac:FinancialInstitutionBranch>
    </cac:PayeeFinancialAccount>
  </cac:PaymentMeans>
  <cac:PaymentTerms>
    <cbc:Note>Till 16.12.2025 you get 2,000  % payment discount - Till 06.02.2026 without discount</cbc:Note>
  </cac:PaymentTerms>
  <cac:AllowanceCharge>
    <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>Cash discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="EUR">26.35</cbc:Amount>
    <cac:TaxCategory>
      <cbc:ID>S</cbc:ID>
      <cbc:Percent>21.00</cbc:Percent>
      <cac:TaxScheme>
        <cbc:ID>VAT</cbc:ID>
      </cac:TaxScheme>
    </cac:TaxCategory>
  </cac:AllowanceCharge>
  <cac:AllowanceCharge>
    <cbc:ChargeIndicator>true</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>Cash discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="EUR">26.35</cbc:Amount>
    <cac:TaxCategory>
      <cbc:ID>Z</cbc:ID>
      <cbc:Percent>0.00</cbc:Percent>
      <cac:TaxScheme>
        <cbc:ID>VAT</cbc:ID>
      </cac:TaxScheme>
    </cac:TaxCategory>
  </cac:AllowanceCharge>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">271.13</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">1291.08</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">271.13</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">26.35</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>Z</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
  </cac:TaxTotal>
  <cac:LegalMonetaryTotal>
    <cbc:LineExtensionAmount currencyID="EUR">1317.43</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">1317.43</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">1588.56</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">26.35</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">26.35</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">1588.56</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">1317.43</cbc:LineExtensionAmount>
    <cac:OrderLineReference>
      <cbc:LineID>85468</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
      <cbc:Name>Regular Product</cbc:Name>
      <cac:SellersItemIdentification>
        <cbc:ID>85468</cbc:ID>
      </cac:SellersItemIdentification>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">1317.43000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
```

Updated2 months ago

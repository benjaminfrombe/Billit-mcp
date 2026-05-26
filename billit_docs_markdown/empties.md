---
title: "Empties"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/empties"
source_slug: "empties"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - empties
---

## About Empties

An invoice might contain Empties.

Some typical elements:

- might be a price increase (deliver more empties) or a price decrease (take empties back)
- is exempt from VAT

Recommended way to include in Json

- VATPercentage : 0 %
- Use ventilation code, Value : 24
- Use a separate invoice line, or an allowance/charge on header level

## Empties as an Invoice Line

Examples below:

- Example 1 mentions the API Json line with a negative amount (price reduction).
- Example 2 mentions the API Json line with a positive amount (price increase).
- Example 3 contains the UBL equivalent, with TAX subtotals (for empties E and for regular products) + 3 invoice lines, one of them is empties.

Json, Amount Reduction, LineJson, Amount Increase, LineUBL, Tax Subtotals, Result of Empties Reduction

```json
        {
            "Quantity": 1,
            "UnitPriceExcl": -4.5,
            "Description": "Empties",
            "VatPercentage": 0,
						"VentilationCode": "24",
			      "CustomFields"
    :
    {
               "InvoiceLine.Note": "Here you can add text info about the empties if needed"
        }
        }

```

```json
        {
            "Quantity": 1,
            "UnitPriceExcl": 4.5,
            "Description": "Empties",
            "VatPercentage": 0,
						"VentilationCode": "24",
			      "CustomFields"
    :
    {
               "InvoiceLine.Note": "Here you can add text info about the empties if needed"
        }
        }
```

```xml
<?xml version="1.0"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>2026.INV.225671a</cbc:ID>
  <cbc:IssueDate>2026-03-19</cbc:IssueDate>
  <cbc:DueDate>2026-04-19</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>NA</cbc:BuyerReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID="9925">BE0437295999</cbc:EndpointID>
      <cac:PartyName>
        <cbc:Name>VILBOX</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>straat 31 box1</cbc:StreetName>
        <cbc:CityName>City</cbc:CityName>
        <cbc:PostalZone>9999</cbc:PostalZone>
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
        <cbc:RegistrationName>SUPPLIER</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>
      </cac:PartyLegalEntity>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cbc:EndpointID schemeID="9925">BE0759529999</cbc:EndpointID>
      <cac:PartyName>
        <cbc:Name>CUSTOMER</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Oktrooiplein 1a 301</cbc:StreetName>
        <cbc:CityName>Ghent</cbc:CityName>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>BE0759529999</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>CUSTOMER</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0759529999</cbc:CompanyID>
      </cac:PartyLegalEntity>
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">4.55</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">-4.50</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>E</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cbc:TaxExemptionReason>Exempt from VAT</cbc:TaxExemptionReason>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">21.68</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">4.55</cbc:TaxAmount>
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
    <cbc:LineExtensionAmount currencyID="EUR">17.18</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">17.18</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">21.73</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">21.73</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:Note>Here you can add text info about the empties if needed</cbc:Note>
    <cbc:InvoicedQuantity unitCode="NAR">-1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">-4.50</cbc:LineExtensionAmount>
    <cbc:AccountingCost>125645</cbc:AccountingCost>
    <cac:Item>
      <cbc:Name>Empties</cbc:Name>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>E</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">4.50000</cbc:PriceAmount>
      <cbc:BaseQuantity>1.0</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
  <cac:InvoiceLine>
    <cbc:ID>2</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">20.48</cbc:LineExtensionAmount>
    <cbc:AccountingCost>125645</cbc:AccountingCost>
    <cac:Item>
      <cbc:Name>Product Info</cbc:Name>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">20.48000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
  <cac:InvoiceLine>
    <cbc:ID>3</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">1.20</cbc:LineExtensionAmount>
    <cbc:AccountingCost>125645</cbc:AccountingCost>
    <cac:Item>
      <cbc:Name>Product 2</cbc:Name>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">1.20000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
```

## Empties as a header Allowance/Charge

Json, Amount Reduction, AllowanceJson, Amount Increase, Charge

```json
        {
            "Quantity": 1,
            "UnitPriceExcl": 4.5,
            "Description": "Consignes",
            "VatPercentage": 0,
			"VentilationCode": "24",
			       "CustomFields"
    :
    {
               "InvoiceLine.Note": "Here you can add text info about the empties if needed",
        },
            "AllowanceChargeIndicator": false
        }
```

```json
        {
            "Quantity": 1,
            "UnitPriceExcl": 4.5,
            "Description": "Consignes",
            "VatPercentage": 0,
			"VentilationCode": "24",
			       "CustomFields"
    :
    {
               "InvoiceLine.Note": "Here you can add text info about the empties if needed",
        },
            "AllowanceChargeIndicator": true
        }
```

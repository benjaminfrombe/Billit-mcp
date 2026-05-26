---
title: "Ventilation Codes (VAT)"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ventilation-codes"
source_slug: "ventilation-codes"
category: "payments-accounting"
topics:
  - payments
  - accounting
  - ventilation
  - codes
  - vat
---

# Why Ventilation Codes

When creating orders it is possible to add a ventilation code to the invoice. This code represents VAT or tax information.

It can be used for multiple networks / transport types:

- Open/Peppol (information see below)
- Email with UBL attachment
- Other networks (see specific information pages or documentation)

# Income / Sales Invoices

When to use a ventilation code:

- When tax % greater than zero
  - No requirement to add ventilation code
  - It is allowed to add it
- When tax % is indicated in Json as 0 %:
  - no ventilation code is added : Peppol TaxcategoryID will be Z and Tax exemption reason will be empty
  - ventilation code is added :
    - use see table below, and no specific code or exemption reason is need.
    - When Tax includes lines of 0 % and Specific codes and exemption reasons are needed, then a specific ventilation code must be included. This applies to the Peppol Taxcategory ID AE, E, K, G. More info about the meaning : [Peppol CodeList](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5305/).

Below the overview for Sales Invoices (Income) :

| Billit Ventilation Code | Descr. Ventilation Code | Default Vat % | UBL TaxCategory ID | TaxExemptionReason in UBL | Peppol description | VAT % in Json |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0% (for BE) | 0.00 | Z |  | Zero rated goods<br>Code specifying that the goods are at a zero rate. | 0 |
| 2 | Low % (6% for BE) | 6.00 | S |  | Vat Reverse Charge. Code specifying that the standard VAT rate is levied from the invoicee. | 6 (BE) |
| 3 | Mid level (12% for BE) | 12.00 | S |  |  | 12 (BE) |
| 4 | High VAT (21% for BE) | 21.00 | S |  |  | 21 (BE) |
| 21 | BTW Verlegd (VAT shifted, VAT Reverse charges) + Cocontrator for BE/NL | 0.00 | AE | Reverse Charge | Vat Reverse Charge. Standard VAT rate is levied from the invoicee. |  |
| 22 | Div. Buiten BTW (Misc. Excluding VAT) | 0.00 | O | Miscellaneous non-VAT | Services outside scope of tax. Taxes are not applicable to the services. | No VAT percentage |
| 24 | Marge (Margin) | 0.00 | E | Exempt from VAT | Exempt from Tax.<br>Taxes are not applicable. |  |
| 51 | IC Goederen (IC Goods) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services | VAT exempt for EEA intra-community supply of goods and services |  |
| 55 | IC Diensten (IC Services) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services | VAT exempt for EEA intra-community supply of goods and services |  |
| 70 | Import / Export | 0.00 | G | Free export item, VAT not charged | Free export item, VAT not charged |  |
| 101 | International transport of People | 0.00 | E | Exempt from VAT | Exempt from Tax |  |
| 102 | Import via EU | 0.00 | E | Exempt from VAT | Exempt from Tax |  |
| 104 | OSS | 0.00 | E | Exempt from VAT | Exempt from Tax |  |

How to use it practically:

- Scenario 1 : No ventilation code is added (UBL Tax category ID will be Z)
- Scenario 2 : Ventilation code is included on **header** level (recommended on header)

  - All lines with VAT percentage 0 will use this ventilation code
- Scenario 3: Ventilation code is used on line level
  - Ventilation code is only needed when Taxcategory ID O, AE, E, K or G is used (in all other cases Billit does generate the correct UBL"
  - Each line with VAT percentage 0:
    - if ventilation code is present on line level : this ventiliation code will be used
    - if ventilation code is present on header level, not on line level : ventilation code on header will be used
    - If ventilation code is not present on header and on line : code Z will be used
    - do only use this if you have multiple VAT codes linked to VAT amount 0 on 1 invoice

Below an Example :

- scenario
  - line 1 and 2 have VAT % 0 (goal is Taxcategory ID = K)
  - line 3 VAT % 21 (goal is Taxcategory ID = S)
- Ventilation code
  - One ventilation code 55 is put on header level in order to get Taxcategory ID K

  - Peppol UBL File

    - Subtotals: TaxcategoryID K and TaxExemption Reason are present:

![](https://files.readme.io/763e6f94d2aa65e8e36c92ff012c033b13f007c62d49d130d9241fd3c4f6833d-afbeelding.png)
    - Detail line : ClassifiedTaxCategory is set to K for lines with 0 %:
- Below the example files (2)
  - 1 : Json Body with 1x ventilation code 55
  - 2 : Generated Peppol UBL by Billit with TaxCategoryID K

Json Ventilation Code 55Peppol UBL Taxcategory ID K

```json
{
    "OrderNumber": "month-41.100-5",
    "OrderTitle": "FC24000230",
    "VentilationCode": "55", //Ventilation code is defined IC Diensten (IC Services), will be used for all lines with VATpercentage 0 %. ), Result Peppol code is K.
    "Currency": "EUR",
    "PaymentTerms": "30 days",
    "Customer": {
        "Name": "TestCustomer",
        "CommercialName": "TestCustomer",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Street": "Oktrooiplein 1",\
                "Box": "Building B",\
                "Zipcode": "9000",\
                "City": "Gent",\
                "CountryCode": "BE"\
            },\
        ],
        "Contact": "Jean Delveaux",
        "VATNumber": "BE043729999",
        "PartyType": "Customer",
        "VATLiable": true,
        "VATDeductable": true,
        "Identifiers": [\
        ],
    },
    "OrderDate": "2025-05-05T11:25:00.4667841+02:00",
    "ExpiryDate": "2025-06-04T11:25:00.466804+02:00",
    "OrderType": "Invoice",
    "OrderDirection": "Income",
    "OrderLines": [\
        {\
            "Quantity": 1.0,\
            "UnitPriceExcl": 50.0,\
            "Reference": "Line.1.Reference",\
            "Description": "0/63 TDLSF",\
            "VATPercentage": 0.0,\
            "DescriptionExtended": "0/63 TDLSF Extended"\
        },\
        {\
            "Quantity": 1.0,\
            "UnitPriceExcl": 50.0,\
            "Reference": "Line.2.Reference",\
            "Description": "0/63 TDLSF",\
            "VATPercentage": 0.0,\
            "DescriptionExtended": "0/64 TDLSF Extended"\
        },\
            {\
            "Quantity": 2.0,\
            "UnitPriceExcl": 4.0,\
            "Reference": "Line.1.Reference",\
            "Description": "0/63 TDLSF",\
            "VATPercentage": 21.0,\
            "DescriptionExtended": "0/63 TDLSF Extended"\
        },\
    ],
}
```

```json
<?xml version="1.0"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>month-41.100-15</cbc:ID>
  <cbc:IssueDate>2025-05-05</cbc:IssueDate>
  <cbc:DueDate>2025-06-04</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>FC24000230</cbc:BuyerReference>
  <cac:OrderReference>
    <cbc:ID>FC24000230</cbc:ID>
  </cac:OrderReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0759529999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0759529999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>Testsupplier</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>straat 31</cbc:StreetName>
        <cbc:CityName>Gent</cbc:CityName>
        <cbc:PostalZone>9000</cbc:PostalZone>
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
        <cbc:RegistrationName>npnwbrabant</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0759529999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Jan Janssens</cbc:Name>
        <cbc:Telephone>+32479999999</cbc:Telephone>
        <cbc:ElectronicMail>ivanv@billit.eu</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0437295999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0437295999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>TestCustomer</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Oktrooiplein 1  Building B</cbc:StreetName>
        <cbc:CityName>Gent</cbc:CityName>
        <cbc:PostalZone>9000</cbc:PostalZone>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>BE0437295202</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>TestCustomer</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Jean Delveaux</cbc:Name>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:Delivery>
    <cac:DeliveryLocation>
      <cac:Address>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:Address>
    </cac:DeliveryLocation>
  </cac:Delivery>
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    <cbc:PaymentID>FC24000230</cbc:PaymentID>
    <cac:PayeeFinancialAccount>
      <cbc:ID>BE13523081289999</cbc:ID>
      <cac:FinancialInstitutionBranch>
        <cbc:ID>TRIOBEBB</cbc:ID>
      </cac:FinancialInstitutionBranch>
    </cac:PayeeFinancialAccount>
  </cac:PaymentMeans>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">1.68</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">100.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>K</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cbc:TaxExemptionReason>VAT exempt for EEA intra-community supply of goods and services</cbc:TaxExemptionReason>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">8.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">1.68</cbc:TaxAmount>
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
    <cbc:LineExtensionAmount currencyID="EUR">108.00</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">108.00</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">109.68</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">109.68</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">50.00</cbc:LineExtensionAmount>
    <cac:OrderLineReference>
      <cbc:LineID>Line.1.Reference</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
      <cbc:Description>0/63 TDLSF Extended</cbc:Description>
      <cbc:Name>0/63 TDLSF</cbc:Name>
      <cac:SellersItemIdentification>
        <cbc:ID>Line.1.Reference</cbc:ID>
      </cac:SellersItemIdentification>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>K</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">50.00000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
  <cac:InvoiceLine>
    <cbc:ID>2</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">50.00</cbc:LineExtensionAmount>
    <cac:OrderLineReference>
      <cbc:LineID>Line.2.Reference</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
      <cbc:Description>0/64 TDLSF Extended</cbc:Description>
      <cbc:Name>0/63 TDLSF</cbc:Name>
      <cac:SellersItemIdentification>
        <cbc:ID>Line.2.Reference</cbc:ID>
      </cac:SellersItemIdentification>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>K</cbc:ID>
        <cbc:Percent>0.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">50.00000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
  <cac:InvoiceLine>
    <cbc:ID>3</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">2.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">8.00</cbc:LineExtensionAmount>
    <cac:OrderLineReference>
      <cbc:LineID>Line.1.Reference</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
      <cbc:Description>0/63 TDLSF Extended</cbc:Description>
      <cbc:Name>0/63 TDLSF</cbc:Name>
      <cac:SellersItemIdentification>
        <cbc:ID>Line.1.Reference</cbc:ID>
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
      <cbc:PriceAmount currencyID="EUR">4.00000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
```

# About Tax Exemption Reason

The tax exemption reasons are automatically generated by Billit based on the ventilation code on header.

If you also want to include your own description 'e.g. legal clause' then you can include this as text in the "Comments" section of the Json.

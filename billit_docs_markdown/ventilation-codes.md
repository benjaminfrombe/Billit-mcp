---
title: "Billit API Source Docs - Ventilation Codes"
updated: 2026-05-26
---

# Ventilation Codes\n\nWhen creating orders it is possible to add a ventilation code to the invoice. These codes represents VAT information. Information below is elaborated when sending is to TransferType Peppol.

# Income / Sales Invoices   [Skip link to Income / Sales Invoices](https://docs.billit.be/docs/ventilation-codes\#income--sales-invoices)

There is no need to include a ventillation code in the API JSON Body:

- When tax % greater than zero (Ventillation Code is 2, 3, 4 , ...)
- When tax % is 0, and no specific code or exemption reason is need. Peppol TaxcategoryID will be Z and Tax exemption reason will be empty.

When Tax includes lines of 0 % and Specific codes and exemption reasons are needed, then a specific ventilation code must be included. This applies to the Peppol Taxcategory ID AE, E, K, G. More info about the meaning : [Peppol CodeList](https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5305/).

Below the overview for Sales Invoices:

| Billit Ventilation Code | Description Ventilation Code | Default Vat % | Peppol UBL TaxCategory ID | TaxExemptionReason Text in Peppol UBL |
| --- | --- | --- | --- | --- |
| 1 | 0% | 0.00 | Z | - |
| 2 | 6% | 6.00 | S | - |
| 3 | 12% | 12.00 | S | - |
| 4 | 21% | 21.00 | S | - |
| 21 | BTW Verlegd (VAT shifted, VAT Reverse charges) | 0.00 | AE | Reverse Charge |
| 22 | Div. Buiten BTW (Misc. Excluding VAT) | 0.00 | E | Exempt from VAT |
| 24 | Marge (Margin) | 0.00 | E | Exempt from VAT |
| 51 | IC Goederen (IC Goods) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services |
| 55 | IC Diensten (IC Services) | 0.00 | K | VAT exempt for EEA intra-community supply of goods and services |
| 70 | Import / Export | 0.00 | G | Free export item, VAT not charged |

How to use it practically:

- Ventilation code is included on header level (no need to include it on line level)
- Ventilation code is only needed when Taxcategory ID AE, E, K or G is used
- Per invoice, only 1 Ventillation Code is mentioned

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

![](https://files.readme.io/c5c4752b5edc33ac8d8f0f1e24f5f22bff8574fe0d6a05e5c47d1e1308eea480-afbeelding.png)

- Below the example files:
  - Json Body with ventillation code 55
  - Peppol UBL with TaxCategoryID K

Json Ventilation Code 55Peppol UBL Taxcategory ID K

```\1

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
        "VATNumber": "BE0437295202",
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

```\1

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

# Cost   [Skip link to Cost](https://docs.billit.be/docs/ventilation-codes\#cost)

| Code | Description | Default Vat Amount |
| --- | --- | --- |
| 1 | Binnenland (Inland) | NULL |
| 21 | BTW Verlegd (VAT shifted) | 0.00 |
| 22 | Div. Buiten BTW (Misc. Excluding VAT) | NULL |
| 111 | Marge (Margin) | 0.00 |
| 51 | IC Goederen (IC Goods) | 0.00 |
| 55 | IC Diensten (IC Services) | 0.00 |
| 102 | Import Via EU | NULL |

Updated15 days ago

* * *

Did this page help you?

Yes

No
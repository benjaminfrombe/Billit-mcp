---
title: "Send UBL to Peppol"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/send-ubl-to-peppol-1"
source_slug: "send-ubl-to-peppol-1"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - send
  - ubl
---

# Preparation

Endpoint to use:

| Information Element | Info |
| --- | --- |
| Post Command on Sandbox | POST [https://api.sandbox.billit.be/v1/peppol/sendxml](https://api.sandbox.billit.be/v1/peppol/sendxml) |
| Post Command on Production | POST [https://api.billit.be/v1/peppol/sendxml](https://api.billit.be/v1/peppol/sendxml) |
| Create a Company | More info : [https://docs.billit.be/docs/sandbox-vs-production-1](sandbox-vs-production.md) |
| Include Party and Secret key in the header | More info : [https://docs.billit.be/docs/authentication](authentication.md) |

About the UBL file:

- Preparation: make sure that your UBL files are valid. When the POST [https://api.sandbox.billit.be/v1/peppol/sendxml](https://api.sandbox.billit.be/v1/peppol/sendxml) is done, then the Peppol validation rules will be checked. If not compliant, then an error will be returned and the document will not be sent.
- The UBL file will be included in the Json body.
- Requirement : All structured ID's get a backslash before and after the value.
  - The structured ID types are : schemeID, unit code, currency ID
  - Make sure that you do not forget any

# UBL Example

Below example of Json body with the UBL content embedded:

UBL Invoice in API

```xml
{
  "XML": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Invoice xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\" xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\" xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\">
    <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>2025000002-31</cbc:ID>
    <cbc:IssueDate>2025-06-23</cbc:IssueDate>
    <cbc:DueDate>2025-08-24</cbc:DueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    <cbc:Note>Testcase 2</cbc:Note>
    <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
    <cac:OrderReference>
        <cbc:ID>YR127130</cbc:ID>
    </cac:OrderReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID=\"0208\">0437295999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID>0437295999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>Supplier Namex</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Teststraat 31</cbc:StreetName>
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
        <cbc:RegistrationName>Vilbox</cbc:RegistrationName>
        <cbc:CompanyID schemeID=\"0208\">0437295999</cbc:CompanyID>
        <cbc:CompanyLegalForm>RPR Gent</cbc:CompanyLegalForm>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Ivan Vanhaecht</cbc:Name>
        <cbc:Telephone>+32(0)2589321</cbc:Telephone>
        <cbc:ElectronicMail>ivan.vanhaecht@testemail.com</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
       <cac:Party>
      <cbc:EndpointID schemeID=\"0208\">0759529999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID>0759529999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>Testcustomername</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Oktrooiplein 1/bus 302</cbc:StreetName>
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
        <cbc:RegistrationName>Testcustomername</cbc:RegistrationName>
        <cbc:CompanyID schemeID=\"0208\">0759529999</cbc:CompanyID>
        <cbc:CompanyLegalForm>RPR Gent</cbc:CompanyLegalForm>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Jan Plessers</cbc:Name>
         <cbc:ElectronicMail>jplessers@billit.eu</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:Delivery>
        <cbc:ActualDeliveryDate>2025-04-01</cbc:ActualDeliveryDate>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>30</cbc:PaymentMeansCode>
        <cbc:PaymentID>2023000001</cbc:PaymentID>
        <cac:PayeeFinancialAccount>
            <cbc:ID>BE54000000099997</cbc:ID>
            <cac:FinancialInstitutionBranch>
                <cbc:ID>BPOTBEB1</cbc:ID>
            </cac:FinancialInstitutionBranch>
        </cac:PayeeFinancialAccount>
    </cac:PaymentMeans>
    <cac:PaymentTerms>
        <cbc:Note>30 days after invoice date</cbc:Note>
    </cac:PaymentTerms>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID=\"EUR\">516</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID=\"EUR\">2400</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID=\"EUR\">504</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>21</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID=\"EUR\">200</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID=\"EUR\">12</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>6</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID=\"EUR\">2600</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID=\"EUR\">2600</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID=\"EUR\">3116</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID=\"EUR\">3116</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode=\"C62\">40</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID=\"EUR\">2400</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Name>Good Y</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>21</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID=\"EUR\">60</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
    <cac:InvoiceLine>
        <cbc:ID>2</cbc:ID>
        <cbc:InvoicedQuantity unitCode=\"C62\">10</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID=\"EUR\">200</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Name>Good X</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>6</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID=\"EUR\">20</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>"
}
```

# Feedback after post

Feedback in case of success:

| Feedback | Production environment |
| --- | --- |
| Status Code | Status Code 200 is success. This means that 1) Data are submitted with success to Billit. 2) Is compliant with Peppol validation rules and formatted in correct way for Billit 3) Has been inserted with success in the Peppol network. |
| InboxItemID | When Status Code is 200, the InboxItemID is returned. This is used for further action. |

For Errors, see [https://docs.billit.be/docs/possible-errors](possible-errors.md)

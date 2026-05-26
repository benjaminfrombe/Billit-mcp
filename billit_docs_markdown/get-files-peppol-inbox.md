---
title: "Get the Invoice and CreditNote Files"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/get-files-peppol-inbox"
source_slug: "get-files-peppol-inbox"
category: "files-documents"
topics:
  - files
  - documents
  - get
  - peppol
  - inbox
  - invoice
  - creditnote
---

### GET Command of the Files

| Endpoint | Method | Response | Extra Info |
| --- | --- | --- | --- |
| /v1/files/FileID | GET | 1 file | Includes full data and file references |

### Reference and Content of the Files

The FileID is the unique Reference.

Example

| Info | Example |
| --- | --- |
| GET of a specific file on the Sandbox | GET [https://api.sandbox.billit.be/v1/files/cc41ebf6-974c-4f32-8ef2-04d78836d1de](https://api.sandbox.billit.be/v1/files/cc41ebf6-974c-4f32-8ef2-04d78836d1de) |

### Result of GET File - Invoice or Creditnote

Json IMR XML Sample

```json
{
    "FileID": "b155ec2e-a74c-4972-928b-f87d6056fd9d",
    "FileName": "133003-460773-60472634-d626-4e8d-870e-7b2e171ad8eb.xml",
    "MimeType": "text/xml",
    "FileContent": "PD94bWwgdmVyc2lvbj ................ hbmRhcmRCdXNpbmVzc0RvY3VtZW50Pg=="
}
```

### How to Process from Base64

The FileContent is a Base64 version. This will then be converted to a file.

Examples of tools

- Base64 to data or file: [https://onlinebase64tools.com/base64-decode](https://onlinebase64tools.com/base64-decode) ,

  - [https://www.base64decode.net/base64-to-file](https://www.base64decode.net/base64-to-file)
- Base64 to PDF:
- Base64 to XML: [https://onlinexmltools.com/convert-base64-to-xml](https://onlinexmltools.com/convert-base64-to-xml)

### About the Content of the UBL

Structure of the received UBL (XML):

- The UBL consists of two parts:
  - the invoice or credit note
  - the Standard Business Document header (SDBH): this part is used for Peppol routing purpose. You can remove this part from the UBL if needed.
- No transformation:
  - The UBL Is the complete XML received from the supplier, without transformation by Billit.
  - No HumanReadable generation is done by Billit.
  - File attachments delivered by the supplier are included in the UBL

Below an example of an invoice received.

UBL Invoice

```xml
<?xml version="1.0"?>
<StandardBusinessDocument xmlns="http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader">
    <StandardBusinessDocumentHeader>
    <HeaderVersion>1.0</HeaderVersion>
    <Sender>
        <Identifier Authority="iso6523-actorid-upis">0208:0759529999</Identifier>
    </Sender>
    <Receiver>
        <Identifier Authority="iso6523-actorid-upis">9925:BE0437295202</Identifier>
    </Receiver>
    <DocumentIdentification>
        <Standard>urn:oasis:names:specification:ubl:schema:xsd:Invoice-2</Standard>
        <TypeVersion>2.1</TypeVersion>
        <InstanceIdentifier>f59bf651-2024-47b6-9a66-9476ad2d0a1c</InstanceIdentifier>
        <Type>Invoice</Type>
        <CreationDateAndTime>2025-04-09T15:21:20.5099272+02:00</CreationDateAndTime>
    </DocumentIdentification>
    <BusinessScope>
        <Scope>
            <Type>DOCUMENTID</Type>
            <InstanceIdentifier>urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1</InstanceIdentifier>
            <Identifier>busdox-docid-qns</Identifier>
        </Scope>
        <Scope>
            <Type>PROCESSID</Type>
            <InstanceIdentifier>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</InstanceIdentifier>
            <Identifier>cenbii-procid-ubl</Identifier>
        </Scope>
        <Scope>
            <Type>COUNTRY_C1</Type>
            <InstanceIdentifier>BE</InstanceIdentifier>
        </Scope>
    </BusinessScope>
    </StandardBusinessDocumentHeader>

<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>QS-099</cbc:ID>
  <cbc:IssueDate>2025-04-09</cbc:IssueDate>
  <cbc:DueDate>2025-05-30</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cac:OrderReference>
    <cbc:ID>QS-099</cbc:ID>
  </cac:OrderReference>
  <cac:AdditionalDocumentReference>
    <cbc:ID>BE0759529999_850220_QS-099.pdf</cbc:ID>
    <cac:Attachment>
      <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="BE0759529999_850220_QS-099.pdf">JVBERi0xvRmlsdGVyIC9GbGF0Z.............................FT0YK</cbc:EmbeddedDocumentBinaryObject>
    </cac:Attachment>
  </cac:AdditionalDocumentReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0759529999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0759529999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>TestCustomer</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Teststraat 31</cbc:StreetName>
        <cbc:CityName>merchtem</cbc:CityName>
        <cbc:PostalZone>1785</cbc:PostalZone>
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
        <cbc:RegistrationName>TestCustomer</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0759529999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>npnwbrabant</cbc:Name>
        <cbc:Telephone>+32479991999</cbc:Telephone>
        <cbc:ElectronicMail>user@billit.eu</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cbc:EndpointID schemeID="9925">BE0437295999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID>BE0437295999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>TestSupplier</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>Oktrooiplein 1 301</cbc:StreetName>
        <cbc:CityName>Ghent</cbc:CityName>
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
        <cbc:RegistrationName>TestSupplier</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Vilbox</cbc:Name>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:Delivery>
    <cbc:ActualDeliveryDate>2025-04-09</cbc:ActualDeliveryDate>
  </cac:Delivery>
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    <cbc:PaymentID>+++099/5150/14279+++</cbc:PaymentID>
    <cac:PayeeFinancialAccount>
      <cbc:ID>BE13523081282439</cbc:ID>
      <cac:FinancialInstitutionBranch>
        <cbc:ID>TRIOBEBB</cbc:ID>
      </cac:FinancialInstitutionBranch>
    </cac:PayeeFinancialAccount>
  </cac:PaymentMeans>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">2.18</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">10.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">0.60</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>6.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">7.50</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">1.58</cbc:TaxAmount>
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
    <cbc:LineExtensionAmount currencyID="EUR">17.50</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">17.50</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">19.68</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">0</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">19.68</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">10.00</cbc:LineExtensionAmount>
    <cac:Item>
      <cbc:Name>Box of cookies</cbc:Name>
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
  <cac:InvoiceLine>
    <cbc:ID>2</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">2.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">7.50</cbc:LineExtensionAmount>
    <cac:Item>
      <cbc:Name>Sticks</cbc:Name>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>21.00</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">3.75000</cbc:PriceAmount>
      <cbc:BaseQuantity>1</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
</StandardBusinessDocument>
```

### About the Optional Attached Files of the UBL

How can I check that the supplier did include attachments ?

The UBL can contain one or multiple attachments

- in the AdditionalDocumentReference section under EmbeddedDocumentBinaryObject
- more info on: [https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AdditionalDocumentReference/](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-AdditionalDocumentReference/)
- Base decoding is needed for each object.
- The main file type is PDF, other types can occur, more info : [https://docs.peppol.eu/poacc/billing/3.0/codelist/MimeCode/](https://docs.peppol.eu/poacc/billing/3.0/codelist/MimeCode/)

Below an example of an AdditionalDocumentReference:

UBL Invoice

```xml
  <cac:AdditionalDocumentReference>
    <cbc:ID>BE0759529202_850220_QS-099.pdf</cbc:ID>
    <cac:Attachment>
      <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="BE0759529202_850220_QS-099.pdf">JVBERi0xvRmlsdGVyIC9GbGF0Z.............................FT0YK</cbc:EmbeddedDocumentBinaryObject>
    </cac:Attachment>
  </cac:AdditionalDocumentReference>
```

---
title: "Processing MLR and IMR files"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/processing-mlr-and-imr-files"
source_slug: "processing-mlr-and-imr-files"
category: "files-documents"
topics:
  - files
  - documents
  - processing
  - mlr
  - imr
---

## IMR and MLR Concept and Use

MLR and IMR files are optional messages, they can be returned by the receivers of your invoices and credit notes. The main volume will be IMR, as MLR is an older standard and IMR is the promoted variant. The file contains the references of the sender and the receiver, as well as the invoice number.

So you can parse the relevant information of the MLR and IMR and store it in your application.

## Information to Process in IMR and MLR

Background information on IMR : [https://www.billit.eu/en-int/help-page/expenditure/invoices/where-can-i-see-imr-messages-from-invoices-sent-via-peppol/](https://www.billit.eu/en-int/help-page/expenditure/invoices/where-can-i-see-imr-messages-from-invoices-sent-via-peppol/) This information does also contain the possible business responses.

The main information elements to process are:

| Value (example) | Type | Sample value |
| --- | --- | --- |
| SenderParty/EndpointID | Your identifier as sender of the invoice. The schemeID indicates the type of identifier. | 0446725999 |
| SenderParty/RegistrationName | The company name of the Invoice sender | Invoice Customer Company Name |
| ReceiverParty/EndpointID | The identifier of the customer, the sender of the IMR message. | 0454298899 |
| ReceiverParty/PartyLegalEntity | The name of the company receiving the invoice. This is the sender of the IMR | Invoice Sender - Supplier Company Name |
| DocumentResponse/ResponseCode | The is the coded response. | "IMR" |
| DocumentResponse/StatusReason | This is a free description text | The document has been received |
| DocumentReference/ID | The Invoice Number this IMR is refering to | QS-29569874 |
| DocumentTypeCode | Typecode of the document, e.g. 380 is Invoice | 380 |

## List of ResponseCode values

| Value (example) | Type |
| --- | --- |
| AB | Message Acknowledgement. To consider as a receipt confirmation. |
| AP | Accepted. The receiver is accepting the invoice (next stap could be the payment) |
| RE | Rejected. The invoice is rejected. |
| IP | In process. Treatment at Customer level is ongoing. |
| UQ | Under Query. Treatment will continue when the question is answered. This is typically a question from buyer to seller. |
| CA | Conditionally Accepted. Condition is in description, the customer is assuming that the supplier accepts the condition. |
| PD | Paid. The customer has intiated the payment process. |

## Example

Below an example of the IMR UBL file (excluding the SDBH : Standard Business Document Header):

IMR

```xml
<?xml version="1.0"?>
<ApplicationResponse xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2">
  <cbc:CustomizationID>urn:fdc:peppol.eu:poacc:trns:invoice_response:3</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:poacc:bis:invoice_response:3</cbc:ProfileID>
  <cbc:ID>660921ad-6579-4c45-90e9-92bbfe6b336d</cbc:ID>
  <cbc:IssueDate>2025-07-25</cbc:IssueDate>
  <cac:SenderParty>
    <cbc:EndpointID schemeID="0208">0446725999</cbc:EndpointID>
    <cac:PartyLegalEntity>
      <cbc:RegistrationName>Invoice Customer Company Name</cbc:RegistrationName>
    </cac:PartyLegalEntity>
  </cac:SenderParty>
  <cac:ReceiverParty>
    <cbc:EndpointID schemeID="0208">0454298999</cbc:EndpointID>
    <cac:PartyLegalEntity>
      <cbc:RegistrationName>Invoice Sender - Supplier Company Name</cbc:RegistrationName>
    </cac:PartyLegalEntity>
  </cac:ReceiverParty>
  <cac:DocumentResponse>
    <cac:Response>
      <cbc:ResponseCode>AB</cbc:ResponseCode>
      <cac:Status>
        <cbc:StatusReasonCode listID="OPStatusReason">NON</cbc:StatusReasonCode>
        <cbc:StatusReason>The document has been successfully received.</cbc:StatusReason>
      </cac:Status>
    </cac:Response>
    <cac:DocumentReference>
      <cbc:ID>QS-29569874</cbc:ID>
      <cbc:DocumentTypeCode>380</cbc:DocumentTypeCode>
    </cac:DocumentReference>
  </cac:DocumentResponse>
</ApplicationResponse>
```

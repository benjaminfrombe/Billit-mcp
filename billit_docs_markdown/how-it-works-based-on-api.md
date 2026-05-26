---
title: "How it works in Billit via API"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-it-works-based-on-api"
source_slug: "how-it-works-based-on-api"
category: "reference-errors"
topics:
  - reference
  - errors
  - works
  - based
  - billit
---

## Overview - Role of the Parties in Billit

In Billit when posting as a customer/buyer with the API, this will be started from your company in Billit. You act then as the customer/buyer.

In the Json body, the party that will be included is the Supplier.

![](https://files.readme.io/191d63f7501e68790874024cefc1edb1cb7b8f8a36b745dfe7548c87a959d564-2026-03-16_10-36-28.png)

Remarks:

- If you want to test in the sandbox environment, you need a receiver (acting as supplier/seller) who is registered with the document type Self-billing on the sandbox.
- If you do not have a test receiver, consider adding an additional test company with these receiving capabilities.

## Customer Posting a Self-Bill Invoice via Orders API

| Element | Value / Description | Example / Options | Mandatory |
| --- | --- | --- | --- |
| **POST URL** | Identical to other invoice types | `v1/orders` | ✅ Yes |
| **Party ID in header** | PartyID of the Customer/Buyer |  | ✅ Yes |
| **OrderType** | The document type | `Invoice` or `CreditNote` | ✅ Yes |
| **OrderSubType** | Use `"SelfBilling"` to trigger processing as a self-bill | `Invoice` or `CreditNote` | ✅ Yes |
| **OrderDirection** | Must be set to `Cost` | `Cost` | ✅ Yes |
| **OrderPDF** | Include your own PDF, if no OrderPDF present, Billit generates PDF |  | ❌ No |
| **Custom Field: Invoice.ContractDocumentReference.ID.Text** | Optional reference to the self-bill related contract |  | ❌ No |

## Sample API v1/order Json content of a Self-Bill (for Customer/Buyer)

Self-Bill Json API InvoiceSelf-Bill CreditNote

```json
{
 "OrderType": "Invoice",  // Self-bill invoice
 "OrderSubType": "SelfBilling",  // Indicating that it is a self-bill
 "OrderDirection": "Cost",  // Fixed value when self-bill
 "OrderNumber": "QS-25687857",  // the Self-bill document number
 "OrderDate": "2025-10-01",
 "OrderTitle": "test buyer reference selfbill",  // an optional reference of the buyer (different from Purchase Order)
  "Reference": "45376987784", //Purchase Order Reference of the buyer (if existing), not needed do not include it
 "ExpiryDate": "2025-10-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
        "FileContent": "JVBERi0xLjUKJb662+go8PC9UeXBlIC9YT2J.....D4dB0kKZW5kc3RyZZWYKMTQ2NzkKJSVFT0YK"
  },
  // Remark : Customer info is not included in the Json body, as it is automatically filled by the customer data filled in the MyBillit portal.
  "Supplier": {  // Receiver of the Self-bill
   "Name": "Vilbox",
   "VATNumber": "BE0437295999",
   //"PartyType": "Supplier", //Receiver of the Invoice
   "Identifiers": [ //Optional Additional Identifiers only if needed\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0437295999"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Company1Supplier",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
    "CustomFields"  : {
    "Invoice.Note": "header note free text ",   //If you want to add more info about self-bill or other info
    "Invoice.ContractDocumentReference.ID.Text": "contract allowing Self-Billing reference number 456999"
    },  // reference of the contract can be added (not mandatory)
 "OrderLines": [ //Remark totals per line are calculated, no need to add it.  Below is minimum information.\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.03,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

```json
{
 "OrderType": "CreditNote",  // Self-bill creditnote
 "OrderSubType": "SelfBilling",  // Indicating that it is a self-bill
 "OrderDirection": "Cost",  // Fixed value when self-bill when you are the issuer, also for CreditNote
 "OrderNumber": "QS-SelfBill_CN1",
 "OrderDate": "2025-10-01",
 "AboutInvoiceNumber": "QS-SelfBill1",  // Optional reference to an Invoice number, this invoice must exist in Billit.
 "OrderTitle": "test buyer self-bill",
 "OrderTitle": "25544525",  // buyer reference
 "Reference": "45376987784", //PO Reference of the buyer
 "ExpiryDate": "2025-10-30",
 "OrderPDF": {
        "FileName": "QS_001_SalesInvoice.pdf",
        "FileContent": "JVBERi0xLjUKJb662+4KOCAwI/...............yZWFtCmVudHhyZWYKMTQ2NzkKJSVFT0YK"
    },
  "Supplier": {
   "Name": "Supplier Company Name",
   "VATNumber": "BE0437999202",
   //"PartyType": "Supplier", //Receiver of the Sales Invoice
   "Identifiers": [ //Optional Additional Identifiers if needed\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0437999202"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "xyz",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "xyz2",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
    "CustomFields"  : {
    "Invoice.Note": "header note free text ",
    "Invoice.ContractDocumentReference.ID.Text": "contract allowing Self-Billing reference number 456999"
    },
 "OrderLines": [\
  {\
   "Quantity": 1,\
   "UnitPriceExcl": 10.03,\
   "Reference": "915025",\
   "Description": "Box of cookies",\
   "VATPercentage": 6.0\
   },\
    {\
   "Quantity": 2,\
   "UnitPriceExcl": 3.75,\
   "Description": "Sticks",\
   "VATPercentage": 21.0\
   }\
 ]
}
```

## The Parties in API v1/Json

The Seller/Supplier (= Self-Bill Receiver) is mentioned in the API Json body as Supplier. Customer info is coming from the Billit My Company Section.

Supplier in API Json

```json
"Supplier": {  //Supplier is the Receiver.  Info of the Customer/Buyer is in the MyBillit interface.
   "Name": "Vilbox",
   "VATNumber": "BE0437295999",
   "Identifiers": [ //Optional Additional Identifiers if needed\
        {\
        "IdentifierType": "CBE",\
        "Identifier": "0437295999"\
        }\
    ],
   "Addresses": [\
        {\
        "AddressType": "InvoiceAddress",\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1",\
        "City": "Ghent",\
        "Box": "301",\
        "Phone": "099991877",\
        "CountryCode": "BE"\
        },\
        {\
        "AddressType": "DeliveryAddress", //The delivery address, if not provided will be automatically the same as invoice address\
        "Name": "Vilbox",\
        "Street": "Oktrooiplein",\
        "StreetNumber": "1b",\
        "City": "Ghent",\
        "CountryCode": "BE"\
        }\
   ]
   },
```

The Customer/Buyer info is coming from the MyBillit My Company section:

![](https://files.readme.io/095f5f75631fb8ec4b721f0942728e2b19003b1135240e84f2cd2f4cc40aad73-2025-10-10_09-05-21.png)

## Where to find the Self-Bill in the MyBillit User Interface

When you are the customer/buyer = sender of the Self-Bill, the Self-Bill will appear in Expenditure in the MyBillit interface:

![](https://files.readme.io/8a9f60be39b04f516cb00448ea37836b75648b62bf0c4d041cf40cf7eb879096-2025-10-01_17-30-13.png)

When you are the supplier/seller = receiver of the Self-Bill, it will appear in Income in the My Billit interface.

![](https://files.readme.io/791dbc3827b3d0f64ed031783db4b06d2fb238150bf34003c770f1aa95f55d48-2025-10-01_17-33-22_income.png)

If the receiver is using another AccessPoint than Billit, then the displayed information will depend on capabilities of that Access Point.

## What is specific to the Self-Bill UBL

Some specific elements are:

- InvoiceTypeCode :
  - is 389 for invoice and
  - 261 for CreditNote
  - (the code is generated by Billit)
- The Peppol routing envelope (this is technical)

Example of a Self-Billing UBL generated by Billit:

Self Billing Invoice UBL Example

```xml
<?xml version="1.0"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:selfbilling:3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:selfbilling:01:1.0</cbc:ProfileID>  // specific for self-bill
  <cbc:ID>QS-SelfBill4</cbc:ID>  // document number
  <cbc:IssueDate>2025-10-10</cbc:IssueDate>
  <cbc:DueDate>2025-10-30</cbc:DueDate>
  <cbc:InvoiceTypeCode>389</cbc:InvoiceTypeCode>  // Self-Bill Inovice
  <cbc:Note>header note free text </cbc:Note> // Free Info
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>test buyer selfbill</cbc:BuyerReference>  // other reference by Buyer/Customer
  <cac:OrderReference>
    <cbc:ID>4537698i784</cbc:ID>   // purchase order reference by Buyer/Customer
  </cac:OrderReference>
  <cac:ContractDocumentReference>
    <cbc:ID>contract allowing Self-Billing reference number 456999</cbc:ID>  //optional reference to the contract
  </cac:ContractDocumentReference>
  <cac:AdditionalDocumentReference>
    <cbc:ID>BE0437295202_2028456_QS-SelfBill4.pdf</cbc:ID>
    <cac:Attachment>
      <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="BE0437295202_2028456_QS-SelfBill4.pdf">JVBERi0xLjUKJb662..................iagpzdGFydHhyZWYKMTQ2NzkKJSVFT0YK</cbc:EmbeddedDocumentBinaryObject>
    </cac:Attachment>
  </cac:AdditionalDocumentReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0437295999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0437295999</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>Vilbox</cbc:Name>
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
        <cbc:RegistrationName>Vilbox</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0437295999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Vilbox</cbc:Name>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cbc:EndpointID schemeID="0208">0759529999</cbc:EndpointID>
      <cac:PartyIdentification>
        <cbc:ID schemeID="0208">0759529299</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>npnwbrabant</cbc:Name>
      </cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>linthoutstraat 31</cbc:StreetName>
        <cbc:CityName>merchtem</cbc:CityName>
        <cbc:PostalZone>1785</cbc:PostalZone>
        <cac:Country>
          <cbc:IdentificationCode>BE</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>BE0759529202</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>npnwbrabant</cbc:RegistrationName>
        <cbc:CompanyID schemeID="0208">0759529999</cbc:CompanyID>
      </cac:PartyLegalEntity>
      <cac:Contact>
        <cbc:Name>Ivan Vanhaecht</cbc:Name>
        <cbc:Telephone>+32479991877</cbc:Telephone>
        <cbc:ElectronicMail>firstname.lastname@gmail.com</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:Delivery>
    <cbc:ActualDeliveryDate>2025-10-10</cbc:ActualDeliveryDate>
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
  </cac:PaymentMeans>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">2.18</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">10.03</cbc:TaxableAmount>
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
    <cbc:LineExtensionAmount currencyID="EUR">17.53</cbc:LineExtensionAmount>
    <cbc:TaxExclusiveAmount currencyID="EUR">17.53</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="EUR">19.71</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="EUR">0.0</cbc:AllowanceTotalAmount>
    <cbc:ChargeTotalAmount currencyID="EUR">0.0</cbc:ChargeTotalAmount>
    <cbc:PrepaidAmount currencyID="EUR">0.00</cbc:PrepaidAmount>
    <cbc:PayableAmount currencyID="EUR">19.71</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="NAR">1.00000</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">10.03</cbc:LineExtensionAmount>
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
      <cbc:PriceAmount currencyID="EUR">10.03000</cbc:PriceAmount>
      <cbc:BaseQuantity>1.0</cbc:BaseQuantity>
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
      <cbc:BaseQuantity>1.0</cbc:BaseQuantity>
    </cac:Price>
  </cac:InvoiceLine>
</Invoice>
```

## Ventilation Codes in Billit API Content when sending Self-Bill

When sending a Self-Bill, you are sending a cost (expenditure) document. Allowed ventilation codes come from the list of Expenditure ventilation codes, more info: [https://docs.billit.be/update/docs/ventilation-codes-for-cost-invoices](https://docs.billit.be/update/docs/ventilation-codes-for-cost-invoices) .

Recommendation : when you generate a Self-Bill with a positive VAT amount, do not include a ventilation code.

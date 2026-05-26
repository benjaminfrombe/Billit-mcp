---
title: "Billit API Source Docs - QMD Reference Index"
updated: 2026-05-26
category: "source-index"
topics:
  - billit
  - api-reference
  - qmd
---

# Billit API Source Docs - QMD Reference Index

This directory contains cleaned Markdown snapshots from the upstream Billit documentation dump in `/Users/olivierdebeufderijcker/Downloads/billit_docs`.
Use these files as Billit API source references for endpoint semantics, payload fields, authentication, e-invoicing behavior, status handling, and integration edge cases. Use `../docs/` for this repository's implementation architecture and local runtime guidance.

This QMD-ready snapshot contains 164 source pages grouped into 10 categories. The import skipped 14 crawler artifacts: upstream 404 pages and duplicate `.md` captures.

## Category Hubs

- [Getting Started, Authentication, and Environments](category-getting-started-authentication.md) - 19 docs. OAuth, API keys, sandbox versus production, onboarding, support, versioning, request headers, and first setup.
- [Orders, Invoices, and Invoice Payloads](category-orders-invoices.md) - 34 docs. Sales invoices, credit notes, order lifecycle, invoice fields, calculations, discounts, VAT, customers, products, and invoice payload variants.
- [Payments and Accounting](category-payments-accounting.md) - 12 docs. Payment terms, payment methods, payment IDs, direct debit, ventilation codes, accounting exports, and financial accounting metadata.
- [Files, PDFs, Attachments, and Documents](category-files-documents.md) - 9 docs. Billit file downloads, uploaded PDFs, attachments, generated PDFs, document storage, and file validation behavior.
- [Receiving, Inbox, and Supplier Documents](category-receiving-inbox.md) - 17 docs. Incoming supplier invoices, purchase inbox flows, invoice responses, inbox confirmation, and receiving feedback.
- [Peppol and E-Invoicing Networks](category-peppol-e-invoicing.md) - 13 docs. Peppol receiver lookup, receiving capabilities, network behavior, UBL delivery, MLR/IMR, and transport fallback.
- [Webhooks, Status, and Feedback](category-webhooks-status.md) - 14 docs. Webhook setup, signature verification, e-invoice status callbacks, delivery feedback, invoice responses, and export status.
- [Partner Automation and France PA](category-partner-france.md) - 13 docs. French PA/e-reporting integration, receiver discovery in France, PA identifiers, tax codes, and testing procedures.
- [KSeF Poland](category-ksef-poland.md) - 16 docs. KSeF send/receive flows, KSeF payload data model, tax codes, corrective invoices, bank accounts, and Polish invoice variants.
- [Reference, Errors, OData, and Type Codes](category-reference-errors.md) - 17 docs. OData syntax, type code references, Swagger/OpenAPI pointers, HTTP errors, idempotency, changelogs, and generic API reference material.

## All Source Pages by Category

### Getting Started, Authentication, and Environments

- [Activate on Production](activate-on-production-environment.md)
- [API QuickStart Sending Invoices](api-quickstart-sending-invoices.md)
- [Authentication](authentication.md)
- [Contact Support](contact-support.md)
- [Create / Verify Account](create-your-account.md)
- [Developer Onboarding Flow](developer-onboarding-workflow.md)
- [General Conditions](general-conditions.md)
- [Header values](header-values.md)
- [How do I request a demo for my integration?](how-do-i-request-a-demo-for-my-integration.md)
- [Identity Verification BE](verifications-be.md)
- [OAuth](how-do-i-get-started-with-oauth.md)
- [OAuth Client ID & Secret?](how-do-i-request-oauth-client-id-and-secret.md)
- [OAuth FAQ](oauth-faq.md)
- [Other User must Verify](create-user-to-verify.md)
- [PartyID and Key](where-can-i-find-my-companyid-or-a-partyid.md)
- [Sandbox VS Production](sandbox-vs-production.md)
- [Verification of a non-Belgian Company](verification-of-a-non-belgian-company.md)
- [Verification of non-Belgian Person](verification-to-non-belgian-user.md)
- [When You are an Integration Partner](when-you-are-an-integration-partner.md)

### Orders, Invoices, and Invoice Payloads

- [Allowances and Charges](allowances-and-charges-advanced.md)
- [Basic Data](basic-data.md)
- [Billit Template Data Fields](billit-template.md)
- [Calculation Method](calculations.md)
- [Cash Discount with Allowances Charges](cash-discount-with-allowances-charges.md)
- [Cash Discount with simple Billit Fields](discount-with-simple-billit-fields.md)
- [Commercial Discount with simple Billit Fields](commercial-discount-with-simple-billit-fields.md)
- [Company has no VAT number](customer-no-vat.md)
- [Creating Sales Invoices](creating-sales-invoices.md)
- [Credit Note](sending-a-credit-note.md)
- [Custom Fields - Credit Note](custom-fields-credit-note.md)
- [Customer has Special Identifiers](customer-has-special-identifiers.md)
- [Customer is Private Person](customer-is-private-person.md)
- [Data Model Billit](data-model.md)
- [Discounts, Charges](discounts.md)
- [Empties](empties.md)
- [Extra Fields : Delivery Location](extra-fields-delivery-location.md)
- [Extra Fields : Extend Content (Line)](extra-fields-extend-content-with-extra-values-line.md)
- [Get Information About 1 Invoice/CreditNote](get-information-about-1-invoice-creditnote.md)
- [Negative Lines on an Invoice](negative-lines.md)
- [Patchable Properties](patchable-properties.md)
- [Prepaid Invoice](prepaid.md)
- [Prepaid Invoices](prepaid-invoices.md)
- [Products](products.md)
- [Retrieve Invoice Info and Status](retrieve-invoice-info-and-status.md)
- [Retrieve List of invoices](retrieve-list-of-invoices.md)
- [Self-Billing Sending on My Billit Portal](self-billing-on-my-billit-portal.md)
- [Send Sales Invoices](send-sales-invoices.md)
- [Sending the Sales Invoice](sending-your-first-invoice.md)
- [sFTP Example for Sales Invoices](sftp-setup-example-salesinvoice.md)
- [Use more than 2 digits for Unit Price](use-more-than-2-digits-for-unit-price.md)
- [VAT one Country, Address second Country](vat-one-country-address-second-country.md)
- [What is Self-Billing](what-is-self-billing.md)
- [When You Submit Prices incl VAT](when-you-submit-prices-incl-vat.md)

### Payments and Accounting

- [Direct Debit](direct-debit-domicili-ring-automatisch-incasso.md)
- [External Data](external-data.md)
- [ExternalProvider data](externalprovider-data.md)
- [IBAN/BIC](ibanbic.md)
- [Payment Reference](payment-id.md)
- [PaymentMethod](paymentmethod.md)
- [PaymentTerms Note](payment-terms-note.md)
- [Retrieve or Set Invoice Number](set-invoice-number-how-can-i-retrieve-the-next-sequence.md)
- [Set other PaymentMeansCode](set-other-paymentmeanscode.md)
- [Split Payment / Reverse Charge](split-payment-reverse-charge.md)
- [Ventilation Codes (VAT)](ventilation-codes.md)
- [Ventilation Codes for Expenditure Invoices](ventilation-codes-for-cost-invoices.md)

### Files, PDFs, Attachments, and Documents

- [Billit Generated PDF](billit-generated-pdf.md)
- [Check Validity of UBL file](check-validity-of-ubl-file.md)
- [Get Files](get-files-related-to-sales-invoices.md)
- [Get Files](get-files.md)
- [Get the Inbox List for IMR and MLR files](get-the-inbox.md)
- [Get the Invoice and CreditNote Files](get-files-peppol-inbox.md)
- [Include your Own PDF and Attachments](include-own-pdf-and-attachments-in-invoice-to-deliver.md)
- [PDF and Attachments](how-can-i-save-a-file2.md)
- [Processing MLR and IMR files](processing-mlr-and-imr-files.md)

### Receiving, Inbox, and Supplier Documents

- [Billit just for sending, not receiving](billit-just-for-sending-not-receiving.md)
- [Check on the MyBillit User Interface](receiving-check-on-the-mybillit-user-interface.md)
- [Check Peppol Receiving Capabilities via API](check-via-api.md)
- [Extra Fields : Supplier and Customer Contacts](extra-fields-supplier-and-customer-contacts.md)
- [Get List of Incoming Invoices](get-list-of-incoming-invoices.md)
- [How you receive your Invoices from Billit](how-you-receive-your-billit-invoice.md)
- [Info Receiving PA](info-receiving.md)
- [Mark Inbox as Read/Confirmed (Purchase)](mark-inbox-as-readconfirmed-copy.md)
- [Mark Inbox as Read/Confirmed (Sales)](mark-inbox-as-read.md)
- [No Need to Receive via Billit](no-need-to-receive-via-billit.md)
- [Peppol Receiving Capabilities](peppol-receiving-capabilities.md)
- [Preparation](preparation-of-invoice-receiving-via-peppol.md)
- [Self-Billing Receiver Registered on Peppol](registered-for-self-billing-receiving.md)
- [sFTP Example for Purchase Invoices](sftp-example-for-purchase-invoices.md)
- [sFTP Example Sales and Purchase Invoices](sftp-example-for-sales-and-purchase-invoices.md)
- [sFTP Setup](sftp-setup.md)
- [Who is a Einvoice Receiver](who-is-a-einvoice-receiver.md)

### Peppol and E-Invoicing Networks

- [About v1/Peppol](specific-for-v1peppol-sendxml.md)
- [Approval Process](approval-process.md)
- [Einvoice Network environments](network-environments.md)
- [Extra Fields : Extend Content (Header)](how-can-i-add-certain-peppol-values-that-billit-json-does-not-support.md)
- [How can I send to a specific Company Numer ?](how-can-i-send-to-a-specific-company-number.md)
- [IMR : More Information](imr.md)
- [Methods for sending DE](methods-for-sending-de.md)
- [Peppol Registration](peppol-other-networks.md)
- [Send to Customer with GLN Number](send-to-customer-with-gln-number.md)
- [Send UBL to Peppol](send-ubl-to-peppol-1.md)
- [Send via Email : Capabilities / Deactivate if needed](email-sending-enable-disable.md)
- [When sending per E-mail DE](when-sending-per-e-mail-de.md)
- [When sending via Peppol DE](when-sending-via-peppol.md)

### Webhooks, Status, and Feedback

- [Check Verification Status](check-verification-status.md)
- [Delivery Status Info in User Interface](status-info-in-user-interface.md)
- [Get and Delete Webhook](get-and-delete.md)
- [Get Status Info via API](status-content-of-a-sales-invoice.md)
- [Get the Inbox List for Supplier Invoices](get-supplier-invoices-and-responses-from-sales-invoices.md)
- [Invoice Responses to the Sender](invoice-responses-to-the-sender.md)
- [Messages and Status](communication-from-receiver-to-sender-pa.md)
- [Non API methods for Export](other-methods-of-receiving-invoices.md)
- [Set Billit Payment Status after Sending](set-billit-payment-status-after-sending.md)
- [Status of Export](status-of-export.md)
- [Use webhooks to catch E-Invoice statuses](use-webhooks-to-catch-e-invoice-statuses.md)
- [Verify Signature Webhook](verify-signature.md)
- [Webhooks](webhooks.md)
- [Webhooks for pushing e-invoice statuses](retrieving-your-first-e-invoice-statuses.md)

### Partner Automation and France PA

- [APIs supported for PA](apis-supported-for-pa-france.md)
- [B2B Sending Flows](b2b-sending-flows-pa.md)
- [Content Requirements PA](customer-data.md)
- [E-Reporting PA](e-reporting-pa.md)
- [FAQ France PA](pa-france-faq.md)
- [General Info on PA](general-info-on-pa.md)
- [How to Find a Receiver in France](how-to-find-a-receiver-in-france.md)
- [Identifiers in France](identifiers-france-pa.md)
- [Setup the Companies for France](create-account-and-french-integration.md)
- [Special Used Cases - Overview - PA](special-used-cases-overview-pa.md)
- [Special Used Cases - Overview - PA](special-used-cases-pa.md)
- [Tax Codes PA in France](tax-codes-pa-france.md)
- [Testing Procedures](testing-procedures-pa.md)

### KSeF Poland

- [Advanced/Settlement Invoices](ksef-advancedsettlement-invoices.md)
- [APIs supported for KSeF](apis-supported-for-ksef.md)
- [Bank Accounts](ksef-bank-accounts.md)
- [Billit Data model for KSeF](billit-data-model-for-ksef.md)
- [Billit Generated PDF with KSeF Info](ksef-billit-generated-pdf-with-ksef-info.md)
- [Corrective Invoice - KOR - KSeF](ksef-corrective-invoice-kor.md)
- [Create KSeF Sales Invoices](ksef-send-sales-invoices-1.md)
- [Extra KSeF Fields (Advanced)](extra-kse-fields-advanced.md)
- [FAQ KSeF](ksef-faq.md)
- [General Info on KSeF](ksef-general-info.md)
- [GET Feedback KSeF Sales Invoices](ksef-get-feedback-sales-invoices.md)
- [Other currency than PLN](ksef-other-currency-than-pln.md)
- [Receive KSeF Purchase Invoices](ksef-receive-purchase-invoices.md)
- [Send to Country outside Poland](ksef-send-to-country-outside-poland.md)
- [Sending to KSeF](sending-to-ksef.md)
- [Tax Codes KSeF](ksef-tax-codes.md)

### Reference, Errors, OData, and Type Codes

- [400](400.md)
- [401 - Unauthorized](401.md)
- [500](500.md)
- [API Change Log](api-change-log.md)
- [Companies](create-new-companies.md)
- [Curl Command Line interface](curl.md)
- [How it works in Billit via API](how-it-works-based-on-api.md)
- [Idempotent Tokens](idempotent-tokens.md)
- [Identifiers DE](identifiers.md)
- [Identifiers for Multiple Countries](identifiers-for-multiple-countries.md)
- [OData for Filtering](odata.md)
- [Party Identifiers](allowed-identifiers.md)
- [PO number : 1 or multiple PO-numbers](how-can-i-add-a-po-number.md)
- [Possible Errors](possible-errors.md)
- [Swagger / Readme / Datamodel](swagger.md)
- [Types](types.md)
- [Versioning](versioning.md)

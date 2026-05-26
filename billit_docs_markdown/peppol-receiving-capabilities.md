---
title: "Peppol Receiving Capabilities"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/peppol-receiving-capabilities"
source_slug: "peppol-receiving-capabilities"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - peppol
  - capabilities
---

## A Receiver Must be Registered for Receiving

A receiver must be registered on the Peppol network:

- with one ore more identifiers (e.g. VAT Number, Company Number)
- with correct document types: minimum Invoice and CreditNote must be registered

## Why is a Company Registered with more than 1 Identifier ?

- Using more than 1 identifier is allowed, you only send to one identifier per invoice/creditnote.
- In Belgium government indicates that minimum company number is required. In practice, companies with VAT number also register the VAT-number.

## Receiving on Peppol test versus Peppol Production

- The Peppol test environment is for test purposes only. The Peppol production environment handles real invoices.
- Test and production are completely isolated environments. A mixture between both is not possible.
- Relationship between environments in Billit and Peppol:

| What | Test environment | Production environment |
| --- | --- | --- |
| Peppol | Peppol test | Peppol production |
| Billit | Billit Sandbox (portal : [https://my.sandbox.billit.be](https://my.sandbox.billit.be/) ) | (portal : [https://my.billit.be](https://my.billit.be/)) |

## Internal and External End-User tools to Verify Peppol Receiving Capabilities

Billit end user tool:

- tpe URL + VAT or KBO number.
  - Peppol test : use [https://api.sandbox.billit.be/v1/peppol/participantInformation](https://api.sandbox.billit.be/v1/peppol/participantInformation)
  - Peppol production : use [https://api.billit.be/v1/peppol/participantInformation](https://api.billit.be/v1/peppol/participantInformation)
- VAT number search (on test) : [https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0563846944](https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0563846944)
- KBO search (on production) : [https://api.sandbox.billit.be/v1/peppol/participantInformation/0563846944](https://api.sandbox.billit.be/v1/peppol/participantInformation/0563846944)

Simple tool for rapid verification:

- Link:
  - Peppol Test : [https://test-directory.peppol.eu/public](https://test-directory.peppol.eu/public)
  - Peppol Production : [https://directory.peppol.eu/public](https://directory.peppol.eu/public)
- Allows to simply fill in the identifier (VAT-number, company number, ...) to launch te search
- Result displays basic data in a simple way. In case of doubt, use advanced tool.

Advanced tool based on Helger:

- Link : [https://peppol.helger.com/public/locale-en\_US/menuitem-tools-participant](https://peppol.helger.com/public/locale-en_US/menuitem-tools-participant)
- Necessity to fill in specific data
- Below example:

![](https://files.readme.io/b6895b142a78e91d1c92a051714892d9d950d283004ea0ebb5a14d22cee30f5d-2025-11-27_08-44-08.png)

Explanation:

- this is search based on Belgian VAT number of Billit
- search is in Peppol test network

## Specific Cases why Receiving might not be possible

Sometimes there are other specific reasons why a Peppol document cannot be sent to the receiver:

- The receiver is registered, with missing documents:
  - no documents registered at all
  - only registered for receiving IMR/MLR, not Invoice Credit Notes
- The certificate is not valid any more
- Other advanced reasons

## Verification in the My Billit User Interface

1. Launch the Invoice Sending via the MyBillit User Interface

When you launch the sending, the Pop-Up screen with put "Send via Peppol" in green, if sending to this receiver is OK

![](https://files.readme.io/d5b6566723252daffdf095ce39f626d2638520c3eda50f85d8bd4628030a9523-2025-11-27_08-52-09.png)

2. View from Customer List in MyBillit

Via the customer menu, linked to the list of customers the Peppol receiving capability is displayed:

![](https://files.readme.io/0dde66c0fb61c3267fa92d2dc7ca79928bb00fe43ffdf009d7cadb05686692c4-2025-11-27_08-56-00.png)

Remark:

- This is the general Peppol registration capability. In certain cases sending might not be possible, e.g. when customer is only registered for IMR/MLR receiving, and not for Invoices / Credit Notes

- [Peppol Receiving Capabilities](peppol-receiving-capabilities.md)

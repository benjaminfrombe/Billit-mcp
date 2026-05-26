---
title: "Self-Billing Sending on My Billit Portal"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/self-billing-on-my-billit-portal"
source_slug: "self-billing-on-my-billit-portal"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - self
  - billing
  - billit
  - portal
  - sending
---

## General Billit Help information:

- Creating: [https://www.billit.eu/en-int/help-page/expenditure/self-billing/?q=self-billing#f-5](https://www.billit.eu/en-int/help-page/expenditure/self-billing/?q=self-billing#f-5)
- Receiving : [https://www.billit.eu/en-int/help-page/income/receiving-self-billing-invoices-from-customers/](https://www.billit.eu/en-int/help-page/income/receiving-self-billing-invoices-from-customers/)

## Supplier/Seller Registers for Self-Billing Receiving

The supplier/seller is the receiver of the self-bill, and has to register the Self-bill invoice receiving capability on Peppol.

This can be Launched from the Settings/General screen: (only needed when **sending**)

![](https://files.readme.io/446fe3e1197178cf75adba519f4106891450dd056b37c56ce538e1df3da9e797-2025-12-17_17-55-29.png)

This allows :

- To launch the Peppol registration for the document type Self-bill
  - When your Peppol registration is via Billit : Self-bill document types will be added to the registration
  - When your Peppol registration is not via Billit :
    - Self-bill document types will not be added to the registration by Billit as there is no registration at Billit
    - Self-bill will be sent, and can be displayed in Billit. Via API you can GET the UBL file.
- To activatie Self-Billing on the Billit user interface

## Supplier/Seller Registers for Self-Billing Receiving : Alternative Method on sandbox

If the supplier is using Billit, the receiving registration can be done in MyBillit via Settings / Integrations / Peppol Acces Point. On the sandbox the Self-Bill document types can be selected:

![](https://files.readme.io/a3e8e14a3d8f640e729391594e15d5c7496fd9acb4a58255f77efb227cc1b394-2025-10-01_15-56-46.png)

On production the Self-Bill document types are automatically set when you are registered on Peppol and the Self-Billing setting is active.

## View on the Screen - Self-Bill Invoice - Customer/Buyer

The Customer can view in the detail screen (Expenditure, Invoice) that it is a Self-bill Invoice:

![](https://files.readme.io/ab11bc21c6fd989e74165a78fa0c8453bfa6deef518cfb71b7fd7810b78a76e3-2025-12-23_16-12-59.png)

The List of Expenditure Invoices contains a view to only view the Self-Bill invoices:

![](https://files.readme.io/1623c405491e15dc347e6e7cbed36ba2d4f465bcc9834a0fa1cf857500610212-2026-02-04_10-15-34.png)

This filter is also existing for issued self-bill credit notes:

![](https://files.readme.io/23ede152e39b365b478150e55fadf81b81ee34c0539b0911155c7891959893ae-2026-02-04_10-18-03.png)

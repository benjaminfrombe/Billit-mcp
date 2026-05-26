---
title: "When You are an Integration Partner"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/when-you-are-an-integration-partner"
source_slug: "when-you-are-an-integration-partner"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - integration
  - partner
---

## High volume, Large Amount of Customers

A white label version is available, documentation [https://docs.accesspoint.billit.eu/docs/who-can-be-an-access-point-partner](https://docs.accesspoint.billit.eu/docs/who-can-be-an-access-point-partner) . For this setup you must be authorised by the enterprise sales team. If this is not applicable to you, the method below can be followed.

## Normal Method for Partners

- Make your integration ready on the Billit sandbox environment:
  - You can create minimum 1 company (e.g. your own company)
  - Follow the steps in the development onboarding flow : [https://docs.billit.be/docs/developer-onboarding-workflow](developer-onboarding-workflow.md).
  - Check whether you application can/must be reviewed via an Appreview.
- How to proceed on the production environment:
  - Make sure that you master account is created on production. This is typically based on your own company details.
  - Billit will deliver you a Reseller link on request . Example [https://my.billit.be/account/YourCompanyName/Register](https://my.billit.be/account/YourCompanyName/Register).
  - This link can be used by your customers:
    - The customer can directly register its company from the Reseller link. And get acces to MyBillit. Info [https://docs.billit.be/docs/basic-data](basic-data.md).
    - The customer gives you information for access : Party id and secret key [https://docs.billit.be/docs/partyid-and-key](where-can-i-find-my-companyid-or-a-partyid.md).
    - With this information you can access the accounts of the customer via API.
  - Invoicing
    - When the invoices are to be paid by the customer, nothing must be done.
    - When the global invoice is to be paid by the Integration Partner, then you send the list of created accounts to Billit. Billit sets the 'Invoice to' field to the partner.

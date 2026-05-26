---
title: "Billit API Source Docs - Preparation"
updated: 2026-05-26
---

# Preparation\n\n### Check before you start   [Skip link to Check before you start](https://docs.billit.be/docs/preparation-of-invoice-receiving-via-peppol\#check-before-you-start)

(identical as for Sales Invoices)

- A Billit sandbox Account. Any license can be taken, no costs will be charged for Sandbox use.
- The generated API key (found under your profile in the Billit application)
- The base URL used for all API calls. For the test environment, this is " [https://api.sandbox.billit.be"](https://api.sandbox.billit.be"/)
- Installed Postman or a similar tool for making API request

### Peppol registration   [Skip link to Peppol registration](https://docs.billit.be/docs/preparation-of-invoice-receiving-via-peppol\#peppol-registration)

Make Sure that Registration for Invoice Receiving on Open/Peppol is Active:

- The Open/Peppol receiving must be active. When using the v1/Order API, the activation is done via the Billit User Interface. Registration is done per Company, and per environment. When you register a company for Peppol receiving on the Sandbox environment, you can only receive invoices via the Open/Peppol test environment, so mixing with production is not possible.
- Simplest way to check activation status: via My Company, Tab E-Invoicing. Below example where Peppol registration is not yet Active:

![](https://files.readme.io/459f5455e42037c2e174ec94b8c42e06abc7a06b27dd8d04fa77edb22c4f2427-2025-05-06_11-46-13.png)

- Click on register. Below example where Peppol registration is Active:

![](https://files.readme.io/11b9396843941d9147449d03515bdf06f31ec0c4f557c1e41a1357b132e471ea-afbeelding.png)

### Activate Automatic Receiving   [Skip link to Activate Automatic Receiving](https://docs.billit.be/docs/preparation-of-invoice-receiving-via-peppol\#activate-automatic-receiving)

Processing of UBL invoices is set to Automatic

- When Open/Peppol invoices are received, by default they are stopped manually in Fast Input.
  - This is only needed when manual reviews are preferred at the level of the Billit Platform.
    - In addition, approval workflows on the Billit level are possible (more info : [Approval](https://www.billit.eu/en-int/help-page/fast-input/processing-files-in-fast-input/approve-files-before-processing/)).
  - If not, this manual stop can be disabled.
- When full automated transfer is desired, In settings the automated processing can be activated. Screenshot:

![](https://files.readme.io/6b1e7cafe96fb6e02774acce25ae2873590a1179fffebbb7fada58b4e3631d05-2025-05-06_12-41-44.png)

### How can I receive Invoices via test environment on Peppol ?   [Skip link to How can I receive Invoices via test environment on Peppol ?](https://docs.billit.be/docs/preparation-of-invoice-receiving-via-peppol\#how-can-i-receive-invoices-via-test-environment-on-peppol-)

- Option 1: Send and Receive : Register 2 companies on the Sandbox (if possible) and Send from Company 1 to Company 2. You can then organise the test scenario's yourself.
- Option 2: Request your suppliers to send test invoices. Remark: many suppliers are only willing to send in the production environment, so this may be more difficult.

Updated30 days ago

* * *

Did this page help you?

Yes

No
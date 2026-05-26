---
title: "Send to Country outside Poland"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ksef-send-to-country-outside-poland"
source_slug: "ksef-send-to-country-outside-poland"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - send
  - country
  - outside
---

## Step 1 : Send Invoice to KSeF

What to do:

- Post your invoice to Billit with the correct data
- Send the invoice to KSeF
- When success : you will get the same feedback as for sending to a Polish customer. Your invoice is now reported to KSeF and considered as issued, with a KSeF ID and an issue date.
- KSeF will **not** send the invoice to the customer.

## Step 2 : Sending to the Customer

- You can now send the invoice to the customer
- For sending, the options are:
  - System used : can be send via Billit, or via your own systems.
  - TransportType used with Email and Open/Peppol as most popular methods. Open/Peppol is not mandatory for EU cross-border E-invoicing.
- Does the KSeF information have to be included ?
  - There is no legal requirement
  - It is in general considered as recommended for full transparency
- If you want to send via Billit and include the KSeF information:
  - Via Billit :
    - Email :
      - send the same document a second type via TransportType SMTP.
      - The PDF will be send, if needed you can include an UBL (more info see the email section).
      - The KSeF ID will be on the PDF.
    - Open/Peppol :
      - When the same document is sent a second time with TransportType Peppol, it will be send as an UBL without the KSeF ID.
      - If you want to include the KSeF ID in the UBL:
        - GET the KSeF ID via the return info
        - Post a new document, with TransportType Peppol and include the KSeF ID in Additional Document Reference, or a text field.

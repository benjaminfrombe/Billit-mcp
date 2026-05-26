---
title: "Check on the MyBillit User Interface"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/receiving-check-on-the-mybillit-user-interface"
source_slug: "receiving-check-on-the-mybillit-user-interface"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - check
  - mybillit
  - user
  - interface
---

# Check on the MyBillit User Interface

In addition to feedback via the API, you can also check the receiving details on the MyBillit user interface.

## What info is available via the MyBillit Portal ?

Information on the My Billit Portal, in the Messages segment:

![](https://files.readme.io/8edf9272e08638fc79ccced4d80bad687a30cd921c3b977f573906177a79a7c4-invoice_receiving.jpg)

About the numbered items on the screenshot:

1. Peppol Icon : the TransferType is Open/Peppol
2. Date and time : when clicking on it, the download of the outgoing UBL-file is started
3. Endpoint scheme ID (example 0208 is for company number) and the ID : this is the identification to where it is sent
4. Date and time : when clicking on it, the **evidence file** is downloaded (MDN). This is your proof that the file is inserted with success in the Peppol network (so the UBL file is valid, the receiver does exist in the Peppol network)
5. **Optional** business communication from the Receiver to the sender (IMR/MLR)

## What if the receivers claims not to have received the Invoice or CreditNote ?

- Are both parties clear that transaction is on test environment or production environment ?
- When delivered with success:
  - Communicate to what identifier you have sent (example above to 0208:0446725877)
  - Responsibility for receiver (and access point of the receiver) is to extract the received invoice and to process it correctly in the flow.
  - In case of doubt you can send the evidence file to the receiver. The receiver can then check with its technical support (internally and support of the AccessPoint).

## Audit Info at Billit

Detailed audit is stored at Billit.

User can display the main data in the My Billit interface :

![](https://files.readme.io/b8f7a3aa7936333019d3a54a7ed7d0d000615b0eb8d84a5fb4b69a37aa9afc0f-audit.png)

---
title: "Delivery Status Info in User Interface"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/status-info-in-user-interface"
source_slug: "status-info-in-user-interface"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - info
  - user
  - interface
  - delivery
---

## View Status in the MyBillit portal

Status and feedback info can be gathered via API, it is also visible on the MyBillit Portal. Status in MyBillit Portal:

![](https://files.readme.io/7fc974efdd549320fff5b14a3c76facc33de0e5a4a72aa31292a67a7eab7443f-2025-09-22_16-21-14.png)

About the numbered items on the screenshot:

1. Information Sent
1. Peppol Icon : the TransferType is Open/Peppol
2. Date and time : when clicking on it, the download of the outgoing UBL-file is started
3. Endpoint scheme ID (example 0208 is for company number) and the ID : this is the identification to where it is sent
2. Date and time : when clicking on it, the **evidence file** is downloaded (MDN). This is your proof that the file is inserted with success in the Peppol network (so the UBL file is valid, the receiver does exist in the Peppol network)
3. **Optional** business communication from the Receiver to the sender (IMR/MLR). In this case one optional IMR-message has been received. Many receivers do **not** send IMR messages.

Below Example of Succesful sending without the return of an optional IMR message:

![](https://files.readme.io/17b743f433585187bf762f3f4ac782b587110e4757fe42eebde8bd220120878e-2026-02-09_10-55-19.png)

## What if the receivers claims not to have received the Invoice or CreditNote ?

- Check environment: Are both parties clear that transaction is sent via the test environment (Billit sandbox) or production environment ?
- Responsibilities :
  - for receiver (and access point of the receiver) is to extract the received invoice and to process it correctly in the flow.
  - This is not your responsibility as a sender. More information below.
- When you have delivered with success but the receiver claims that it is not received, then the actions are:
  - Communicate to what **identifier** you have sent (example above to 0208:0446729999 = company number of 9925:BE0446729999 is VAT-number)
  - In case of doubt / discussion:
    - send to the receiver 2 files:
      - the **evidence file** to the receiver (see above screenshot point2).
      - the **peppol XML**
    - The receiver can then check with its technical support (internally and support of the AccessPoint). This should **not** be checked by **end-users**, but by **technical support.**

Overview of the Peppol 4-corner model:

![](https://files.readme.io/eef3509b02e6722a33157f2dd06dafbde3e25c4be452f67651453cc40beacaaa-2025-12-03_13-29-59.png)

Responsibilities:

- Access Point of the Sender (Corner 2) puts Invoice/CreditNote in the network. After successful insertion, an evidence file is gathered.
- Access Point of the Receiver (Corner 3) gathers the file, and delivers to the Receiver (Corner 4). When Sender (corner 1) can deliver an evidence file, it is up to Access Point of Receiver (Corner 3) and Receiver (Corner 4) to examine the further processing of the Invoice/CreditNote.

## What if there are Issues with the delivery ?

- When the sending is launched, items will go in status In queue. Compliance check on content and registration of the receiver have been check prior to launching. User Interface:

![](https://files.readme.io/74eb926845bb202694b5e140fb727eaad80cdba75e1273fda018bcd808b2800e-2025-12-10_14-14-52.png)

- If issues would occur:

  - system will retry for a while
  - will finally go in error
  - error will be displayed on user interface in messages:

![](https://files.readme.io/e67de03082508e0caffb707bb988f581f95a6314e904fd472fe3423506672c6a-2025-12-10_14-19-11.png)
  - an email will be sent if the settings are active (see further)

## Audit Info at Billit

Detailed audit is stored at Billit.

User can display a summary of the data in the My Billit interface :

![](https://files.readme.io/6917044bdeb6130b7fd390218295a76908b3decbfae326fc72eebddc882c5fc8-audit.png)

## Get Notified per Email

When email status notifications are activated (setting per user), then status updates will be sent via email

- per status update one email
- positive statuses and negative statuses

Below example of an email referring to the receiving of an IMR (status PD : Paid)

The email:

![](https://files.readme.io/f1407a39237f28ffa1d130a0c275b8856cd72cb66678ad3fe05dabaec466a3fa-2025-09-22_15-56-29.png)

How to activate / deactivate the email notification setting for sales invoices:

- Menu : Settings / General / Advanced :

![](https://files.readme.io/9d79de476817185892a68b42c23e18c28866bbd1ac0da3c6d0f642b1fa4235c4-2025-12-10_14-11-25.png)

The second option will activate/deactivate the email notification in general.

If you want to add an email receiver who is not a Billit user:

![](https://files.readme.io/87fd1192908663181800dd5d58173f955390f96ef92fafec02213bf7a57033f9-2025-12-10_14-09-40.png)

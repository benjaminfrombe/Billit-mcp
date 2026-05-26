---
title: "About v1/Peppol"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/specific-for-v1peppol-sendxml"
source_slug: "specific-for-v1peppol-sendxml"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - specific
  - v1peppol
  - sendxml
  - about
  - v1
---

# About v1/Peppol

Options when sending to Open/Peppol:

- Main goal : include your UBL in the API and send via Billit to a Open/Peppol Receiver.
- Alternative :
  - You can also json tags without UBL (info : [https://api.billit.be/swagger/ui/index#/Peppol](https://api.billit.be/swagger/ui/index#/Peppol)).
  - In case of Json tags, the API v1/order endpoint is the recommended solution and not v1/Peppol - Send XML, for more info : [https://docs.billit.be/docs/quick-start#/](api-quickstart-sending-invoices.md#/)

Specific for this v1/Peppol API endpoint:

- Basic requirement : The sender is able to include a **valid Peppol UBL** file :

  - The file complies with the **Open/Peppol validation rules**. During setup the sender will test the UBL content separately for the relevant invoicing scenario's.
  - The **customer** and **supplier** are correctly mentioned in the UBL.
- The transport type is **Open/Peppol** only (not other channels such as Email or non-Peppol einvoicing networks). If the receiver is not registered on Open/Peppol, then an alternative channel cannot be used via Billit.
- The "MyBillit" User Interface is not used for user tracking the success of the delivery, so you will not be able to view the invoices sent or received in My Billit. Status is obtained via API and can be integrated in the invoicing software of the sender.
- About attachments:
  - If no attachment is included as encoded object, then UBL will be sent via Peppol without any attachment (no Billit human readable generated).
  - If you want to include one or more attachments, then include them in your source UBL.

> ⚠️
>
> ### **Important Notice**   [Skip link to ,[object Object]](https://docs.billit.be/docs/specific-for-v1peppol-sendxml\#important-notice)
>
> Billit does **not** provide support for creating or validating UBL files.
>
> Integrators are fully responsible for generating valid UBL according to the applicable standards.

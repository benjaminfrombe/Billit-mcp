---
title: "Billit API Source Docs - Other Information"
updated: 2026-05-26
---

# Other Information\n\n### Incoming Invoice is Processed in Target System   [Skip link to Incoming Invoice is Processed in Target System](https://docs.billit.be/docs/other-information\#incoming-invoice-is-processed-in-target-system)

Simple ways to make sure that Incoming Invoice/Credit note is processed:

- Filter on modification date with Odata
- Store the processed OrderID's. This allows to check that the OrderID is new or not.

### When Document is Received, do we send response to the Sender ?   [Skip link to When Document is Received, do we send response to the Sender ?](https://docs.billit.be/docs/other-information\#when-document-is-received-do-we-send-response-to-the-sender-)

When document is received with success at the level of Billit, an Invoice response is back to the sender:

- This will happen when TransferType is Peppol and when the receiver is registered for receiving Invoice Responses
- Information that will be sent back : AB: The document has been successfully received.
- More information about IMR : [IMR](https://www.billit.eu/en-int/help-page/expenditure/invoices/where-can-i-see-imr-messages-from-invoices-sent-via-peppol/)

Updatedabout 1 month ago

* * *

Did this page help you?

Yes

No
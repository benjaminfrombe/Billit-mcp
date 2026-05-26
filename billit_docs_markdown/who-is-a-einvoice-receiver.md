---
title: "Billit API Source Docs - Who Is A Einvoice Receiver"
updated: 2026-05-26
---

# Who is a Einvoice Receiver\n\n## Receiving capabilities for Peppol   [Skip link to Receiving capabilities for Peppol](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#receiving-capabilities-for-peppol)

### Why ?   [Skip link to Why ?](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#why-)

It might be interesting to get information about the receiving capabilities of a customer on Peppol.

This search could be done via API for the following reasons:

- You want to store this information in the ERP or accounting software. This allows you to view the customer receiving information directly in the customer information.
- You only want to use Billit only for sending to a Peppol (or other einvoicing network). So you will only deliver to Billit when the result is positive.
  - Remark : When receiver is not on Peppol, Billit can launch email sending or postal delivery as an alternative (by default) or you can exclude it. More info : [Link](https://docs.billit.be/docs/how-can-i-restrict-transport-types)

### How : Get information   [Skip link to How : Get information](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#how--get-information)

In order to launch a request about receiving capabilities, below examples.

- VAT-based: For many countries, results for a customer VAT number can be retrieved with endpoint:

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/BE0437299999)

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/NL002059999B90](https://api.sandbox.billit.be/v1/peppol/participantInformation/NL002059999B90)

- Company number: For Belgium, company number can be retrieved in a similar way:

GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0437299999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0437299999)

### Check Receiving capabilities via specific schemeID   [Skip link to Check Receiving capabilities via specific schemeID](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#check-receiving-capabilities-via-specific-schemeid)

There are several other schemeID's that might be relevant (country specific, GLN-numbers, other). It might also be needed to use them to get a full insight of receiving capabilities.

For the full list of Billit identifiers : [https://docs.billit.be/docs/allowed-identifiers](https://docs.billit.be/docs/allowed-identifiers)

Examples how to get the information:

- GLN number
  - Certain organisations are registered with GLN numbers. You cannot search the correct GLN number via a VAT number. But once you know the GLN number, you can check the receiving capabilities.
  - Example of a search via the GLN number : GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0088:5430003799999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0088:5430003799999)
- Search a VAT number with the country specific scheme ID
  - Belgium, VAT : GET [<https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999>](https://api.sandbox.billit.be/v1/peppol/participantInformation/9925:BE0437299999)
  - Netherlands, VAT GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/9944:NL00205999B90](https://api.sandbox.billit.be/v1/peppol/participantInformation/9944:NL002059999B90)
  - Germany, VAT: GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/9930:NL00205999B90](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver)
- Other country specific endpoint schemeID's
  - Netherlands, KvK : GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0106:27379999](https://api.sandbox.billit.be/v1/peppol/participantInformation/0106:27379999)
  - Netherlands, OIN (government): GET [https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:00000001008078452000](https://api.sandbox.billit.be/v1/peppol/participantInformation/0190:00000001008078452000)

### What Information do I get back ?   [Skip link to What Information do I get back ?](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#what-information-do-i-get-back-)

| IdentifierType | Example | Information |
| --- | --- | --- |
| Registered | true, false | This is the main element : Registration is true or false |
| Identifier | 0190:0000000100807999000 | Confirmation of scheme ID and identifier used for the search |
| DocumentTypes | "BISv3Invoice",<br>"IMR",<br>"BISv3CreditNote"<br>"MLR", | Registered true/false is not enough, support must be for the document types invoice and CreditNote for being able to send these documents. BISv3Invoice and BISv3CreditNote is most common, some variants are possible. |
| ServiceDetails | More advanced information on Peppol details |  |

## Other networks then Peppol\#\#   [Skip link to Other networks then Peppol\#\#](https://docs.billit.be/docs/how-do-i-know-who-is-a-peppol-receiver\#other-networks-then-peppol)

Other networks cannot be searched via the same endpoint. Country specific websites and tools are available to get the required information.

Updated21 days ago

* * *

Did this page help you?

Yes

No

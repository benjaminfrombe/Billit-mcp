---
title: "Billit API Source Docs - Header Values"
updated: 2026-05-26
---

# Header values\n\n# To Billit   [Skip link to To Billit](https://docs.billit.be/docs/header-values\#to-billit)

Below you can find all accepted header values that have a usage with the API

| Header Name | Header Value | Header Usage |
| --- | --- | --- |
| PartyID | INT - A party ID | To define the context |
| ContextPartyID | INT - A party ID | To define the context |
| ApiKey | "Secret ID' | To be authenticated with the API |
| Authorization | "Access token" | To be authenticated with the API |
| Idempotent-Key | "Unique client generated string" | To make unique requests |
| StrictTransportType | "true" | To make transportTypes strict |

# From Billit   [Skip link to From Billit](https://docs.billit.be/docs/header-values\#from-billit)

| Header Name | Header Value | Header Usage |
| --- | --- | --- |
| Billit-Signature | String (Time +Encrypted) | To verify the webhook |

Updated12 months ago

* * *

Did this page help you?

Yes

No
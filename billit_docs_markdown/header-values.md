---
title: "Header values"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/header-values"
source_slug: "header-values"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - header
  - values
---

# To Billit

Below you can find all accepted header values that have a usage with the API

| Header Name | Header Value | Header Usage |
| --- | --- | --- |
| PartyID | INT - A party ID | To define the context, the ID of your company. When you use multiple companies, then make sure that in the header of your API the correct company is addressed. |
| ContextPartyID | INT - A party ID | To combine when you are using application as an accountant |
| ApiKey | "Secret ID' | To be authenticated with the API |
| Authorization | "Access token" | To be authenticated with the API |
| Idempotent-Key | "Unique client generated string" | To make unique requests |
| StrictTransportType | "true" | To make transportTypes strict (no fallback to alternative method if the primary method is not available) |

# From Billit

| Header Name | Header Value | Header Usage |
| --- | --- | --- |
| Billit-Signature | String (Time +Encrypted) | To verify the webhook |

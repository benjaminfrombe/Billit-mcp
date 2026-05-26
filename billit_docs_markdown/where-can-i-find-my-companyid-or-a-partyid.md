---
title: "PartyID and Key"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/partyid-and-key"
source_slug: "partyid-and-key"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - where
  - find
  - companyid
  - partyid
  - key
---

## Finding your PartyID

- PartyID can be view via the MyBillit user interface.
- PartyID on sandbox and PartyID on production are different
- Below example for a company on the sandbox:

![](https://files.readme.io/7383339e044dce021b7d5fd061f7c59318b7f7f82c20ad819c0056a739029286-2025-10-10_07-34-09.png)

## Finding your API Key - Only allowed for non-commercial integrations.

A non-commercial integration is a personal integration developed and used exclusively by an individual or organization to automate their own administration. It is not shared, distributed, sold, or otherwise made available to third parties, and it has no commercial purpose or business model attached.

Do not share your API-key with others, Billit will never ask for your API key.

![](https://files.readme.io/749a68dd01b871f2776a68df0eabd00aa4a181e42ad7b19331f6d00802e478c3-Afbeelding2.png)

## How to use it in your API-Integration

Secret API Key and PartyID are put in the header.

Below example with Postman.

**PartyID in Postman Header:**

![](https://files.readme.io/d794c886f5712d7596c7689c8210d5f991fc4b70696ee0acea27b5513d754028-partyID_real.png)

> ⚠️
>
> **When Using Multiple Companies**
>
> When you send/receive for multiple companies, make sure you always use the **partyID of the specific company**.
>
> The secret key can be the same for all companies because it is linked to a user who has access rights to all companies.

**API key in Postman Header Authorisation:**

![](https://files.readme.io/0a2a04a9269f328c91cffb4fa428ae83726e927ea4b19d472b4b809eaf9cc116-ap_key.png)

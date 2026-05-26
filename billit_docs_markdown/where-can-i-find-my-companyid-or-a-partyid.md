---
title: "Billit API Source Docs - Where Can I Find My Companyid Or A Partyid"
updated: 2026-05-26
---

# Where can I find my CompanyID or a PartyID\n\nEach company, customer, supplier in Billit has its own ID. This ID is separate from a custom ID you give. This ID allows you to use them in request without having to provide all the data in the request.

**There are a few ways on how to get these IDs**

- By creating a Party via de API [/v1/parties](https://docs.billit.be/reference/party_postparty-1))


When you create a party via this endpoint a unique ID will be returned.

- By retrieving a Party via de API [/v1/parties/{partyID}](https://docs.billit.be/reference/party_getparty-1)

- By going to the page of the Party


1. If you need your own company ID you can find it by going to the my company page in Billit and copying the Unique ID from the URL
2. If you need the Unique ID from a customer or supplier you can go to the edit screen for that party and get the ID from the URL.

Note: when no party is specified in the request headers, the Billit API will use the oldest existing company that can be linked to the user's API key. Provide the partyid header and a companyid to select which company needs to be used.

Updatedalmost 2 years ago

* * *

Did this page help you?

Yes

No
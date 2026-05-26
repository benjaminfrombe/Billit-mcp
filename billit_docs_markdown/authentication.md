---
title: "Billit API Source Docs - Authentication"
updated: 2026-05-26
---

# Authentication\n\n# 🔒 Authentication (OAuth or API key?)   [Skip link to 🔒 Authentication (OAuth or API key?)](https://docs.billit.be/docs/authentication\#-authentication-oauth-or-api-key)

> ## 🚧  Secret Keys
>
> Billit places paramount importance on the security of your authentication keys. **Under no circumstances will Billit request your secret keys**.
>
> Sharing these keys poses a significant security risk. If you suspect that your keys have been compromised, please reach out to Billit immediately so we can take the necessary steps to secure your account.

# Authentication Methods: API Key vs. OAuth   [Skip link to Authentication Methods: API Key vs. OAuth](https://docs.billit.be/docs/authentication\#authentication-methods-api-key-vs-oauth)

* * *

**API Key**

Upon creating a Billit account, you gain immediate access to API authentication through an API Key, easily located in the Billit Application under your profile. This key is unique to your account and is not limited to a single company within Billit, allowing for versatile use across multiple entities associated with your account. It's crucial to keep this key confidential and store it securely.

**OAuth Authentication**

Billit advocates for the use of OAuth for enhanced security and scalability, particularly for integrations intended for multiple users. While OAuth is not obligatory for individual use, it becomes a requirement for live integrations serving numerous users.

- **Getting Started with Oauth:**
  - More information on Oauth: [https://docs.billit.be/docs/how-do-i-get-started-with-oauth](https://docs.billit.be/docs/how-do-i-get-started-with-oauth)
  - To initiate OAuth authentication, contact Billit support at [support@billit.be](mailto:support@billit.be) requesting OAuth credentials. You'll need to provide a Redirect URL and the name of your integration.
  - Upon review, Billit support will furnish the OAuth Client ID and Secret for sandbox testing. To obtain credentials for the production environment, your application must first be approved for production use.

# API Key Practical Use   [Skip link to API Key Practical Use](https://docs.billit.be/docs/authentication\#api-key-practical-use)

**Usage instructions:**

- For general API calls, include your API Key in the request header.
- To specify the company for the API call, include the Company/PartyID in the request. This detail is essential when your account is linked to multiple companies.
- For accountants managing multiple companies, include both the ContextCompanyID (accountant's ID) and the PartyID (company's ID) in the request headers.

**Summary**

| Requried | Header field name | Example Value |
| --- | --- | --- |
| Yes | apiKey | "YourAPIKey" |
| As Needed | partyID | Company ID |
| For accountants cases | ContextPartyID | Accountant's Company ID |

**Where to find**

Your API Key is found under 'Profile' -> 'Users & API Key'.

My profile:

![](https://files.readme.io/95e8b5c677c1a71df44bf45505debc0abd153715b54d264ccb4f57c59d1a7427-afbeelding.png)

API key in Detail Screen My Profile

![](https://files.readme.io/bcd7b562facdfd5a90650f1d2af6f79a68e92ce63596590e38ad19d385e92bff-afbeelding.png)

Party ID: click on My company, and in the URL the company ID will appears (numeric):

![](https://files.readme.io/d4d29056b8a9ed04cb1e18a349eb6494eb8c4267f3d072f8b1f407a4f22f958f-afbeelding.png)

**Usage instructions:**

The Base URL in the Endpoint should refer to Sandbox or Production : [https://docs.billit.be/docs/sandbox-vs-production-1](https://docs.billit.be/docs/sandbox-vs-production-1)

When you start with sandbox, this is: [https://my.sandbox.billit.be](https://my.sandbox.billit.be/).

Updated11 days ago

* * *

Did this page help you?

Yes

No
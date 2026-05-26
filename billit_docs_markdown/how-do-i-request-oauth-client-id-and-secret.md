---
title: "OAuth Client ID & Secret?"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-do-i-request-oauth-client-id-and-secret"
source_slug: "how-do-i-request-oauth-client-id-and-secret"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - request
  - oauth
  - client
  - id
  - secret
---

# OAuth Client ID & Secret?

**Client ID and Secret for the sandbox environment**

When wanting to have a ClientID and Secret create a support ticket (info : [https://docs.billit.be/docs/contact-support](contact-support.md)).

Make sure to provide all **4** parameters are communicated _(If 1 is missing, we cannot proceed)_ :

- **1\. Billit Party ID** example "729999" _(where to find party ID_ : [Party ID](where-can-i-find-my-companyid-or-a-partyid.md))
- **2\. Redirect URI** example \[ [https://your.app/oauth/callback](https://your.app/oauth/callback)\] _(we always need a redirect URL, not localhost)_
- **3\. Application Name** : \[YOUR APPLICATION NAME\] _( we need a name)_
- **4\. Environment** : Sandbox or Production _(step1 sandbox, step 2 production)_

> ❗️
>
> ### API Key - Allowed for non-commercial integrations.
>
> A non-commercial integration is a personal integration developed and used exclusively by an individual or organization to automate their own administration. It is not shared, distributed, sold, or otherwise made available to third parties, and it has no commercial purpose or business model attached. You can then use API ey without oauth : [https://docs.billit.be/docs/partyid-and-key](where-can-i-find-my-companyid-or-a-partyid.md).

> 🚧
>
> ### Never Share!
>
> Please do not share your ID and Secret to any 3rd party. When Billit sends the data they will remove it from the thread.
>
> **Billit will never ask you to share the Secret or ID again**

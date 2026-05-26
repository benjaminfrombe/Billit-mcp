---
title: "OAuth FAQ"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/oauth-faq"
source_slug: "oauth-faq"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - oauth
  - faq
---

## Why OAuth?

Security incidents and fraud are rising fast.

E-invoices must be protected. OAuth 2.0 adds security by:

- Using **access tokens** instead of passwords
- Limiting scope and lifetime of access
- Preventing password sharing with third parties
- Reducing the risk if a token or app is compromised

## When do I need OAuth?

- **Required**: Using the Billit API
- **Not required**: SFTP integrations or direct login to the MyBillit portal

## Logging in to MyBillit

Normal user login to the portal does **not change** when OAuth is active.

- Production: [https://my.billit.eu](https://my.billit.eu/)
- Sandbox: [https://my.sandbox.billit.eu](https://my.sandbox.billit.eu/)

## Sandbox vs Production

- Sandbox and Production have **separate**`client_id` and `client_secret`
- Credentials are **not interchangeable**

## Finding your PartyID

- PartyID must be retrieved via the Account EndPoint:

![](https://files.readme.io/7383339e044dce021b7d5fd061f7c59318b7f7f82c20ad819c0056a739029286-2025-10-10_07-34-09.png)

## API Key - Only allowed for non-commercial integrations.

A non-commercial integration is a personal integration developed and used exclusively by an individual or organization to automate their own administration. It is not shared, distributed, sold, or otherwise made available to third parties, and it has no commercial purpose or business model attached.

Do not share your API-key with others, Billit will never ask for your API key.

![](https://files.readme.io/749a68dd01b871f2776a68df0eabd00aa4a181e42ad7b19331f6d00802e478c3-Afbeelding2.png)

## Redirect URI

- A redirect URI is **always required**, even if you do not require it for your internal purposes
- A redirect URI with `https://localhost/...` is not allowed on the production environment
- Multiple redirect URIs are supported if needed
- **Dynamic redirect URIs are not supported**
- When using the redirect URI for the first time and you get the error " : no access : check that the redirect URI allows communication with the outside world. If you need to whitelist Billit based on IP-addresses, contact Billit.

## Why an initial login?

The first login collects **user identity** and **consent**.

Tokens are issued based on this context.

## Supported - Not Supported OAuth Flows

- Supported: **Authorization Code Flow** (with refresh tokens) → for user-facing apps
- Not supported: **Client Credentials Flow** → for server-to-server integrations

## Token lifetime & refresh

- Access tokens are valid for **60 minutes**
- Always refresh before expiry using the **refresh token**
- If expired, request a new access token with no user interaction

## User login frequency

- Users log in **once** to authorize
- After that, refresh tokens keep the API connection alive

## Revoked tokens

If a token is revoked:

- The user removed your app’s access to their Billit account
- Your app must request authorization again

## Redirect URI changes

If you need to update your redirect URI:

- Contact Billit Support to change it in your client registration

## Key rules

- 🔑 Tokens expire in 60 minutes
- 🔄 Refresh tokens keep sessions alive
- 🔒 No password sharing, only token-based access
- 🛑 Dynamic redirect URIs are not supported

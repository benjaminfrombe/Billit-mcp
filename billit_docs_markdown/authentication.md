---
title: "Authentication"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/authentication"
source_slug: "authentication"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
---

# OAuth Authentication

Billit uses **OAuth 2.0** as the standard authentication method to ensure security, scalability, and user control.

## Why OAuth?

- Stronger security than API keys
- Users explicitly grant and revoke access by logging in
- Users can disconnect integrations at any time

## Getting Started

1. Review the [Getting Started with OAuth guide](how-do-i-get-started-with-oauth.md).
2. Contact **Billit Support** to request OAuth credentials.

   - You will receive a **Client ID** and **Client Secret** for sandbox testing.
3. Once your integration is ready for production, submit it for approval.
   - After approval, production credentials will be issued.

```
BillitDeveloperBillitDevelopersend mail to support@billit.eu to to request Client ID and Secret for AppName and Redirect URL on Sandbox.confirms with Client ID & Secret	for Sandbox
```

## OAuth 2.0 Flow

```
BackendBillit Auth ServerAppUserBackendBillit Auth ServerAppUserClick "Login with Billit"Redirect (client_id, redirect_uri, scopes)Login & consent screenCredentials + consentRedirect with auth_code → redirect_uriSend auth_codeExchange code for tokens (client_id, secret)Access_token + refresh_tokenSession established
```

- [OAuth](how-do-i-get-started-with-oauth.md)

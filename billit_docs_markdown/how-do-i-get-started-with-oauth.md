---
title: "OAuth"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/how-do-i-get-started-with-oauth"
source_slug: "how-do-i-get-started-with-oauth"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - get
  - oauth
---

## What is OAuth and How is it used at Billit

OAuth is a way of letting a customer grant you access to their Billit account and allowing you to perform actions in their name. For this you need to have an OAuth client which needs to be requested, how can be found here [How do I request OAuth Client ID and Secret?](how-do-i-request-oauth-client-id-and-secret.md).

Every user you want to get access to as an integrator is required to login using the credentials of your client. After a successful login you can perform actions using the access token in the name of the corresponding user. As the tokens are linked to the client used in the authentication process in Billit. This means that trying to refresh an access token using another client will fail.

Since every user will login using the same client, it is advised to add a unique identifier in the URL used to send the users to the Billit login page to keep track of who is who. This can be achieved by either adding it in the redirect\_uri (a wildcard will need to be set on the Billit side first) or by adding the identifier to the state parameter as these values will be returned after logging in.

The redirect URL provided when requesting an OAuth client is used to send the result to after a login attempt. Thus the place where users are returned to in your website when the authentication was successful or unsuccessful.

> 📘
>
> ### One client to rule them all!
>
> Only you as an integrator need a client, your users do not. They will make use of your client to grant you access.

```
BillitAppBillitAppsend mail to support@billit.eu to to request Client ID and Secret for PartyID, AppName and Redirect URL on Sandbox.confirms with Client ID & Secret for Sandboxredirect user to Bililt Logon page with ClientID (required) & RedirectURL(required) & State (optional)redirects user to redirectURL and AuthorizationCodecalls Billit OAuth2/token with Client ID(required), Secret ID(required), AuthorizationCode(required) & Grant_type(required) & RedirectURL(required)returns the Bearer token needed by the app to call the Account,Order, Document or File API
```

## is Oauth Required ?

> ⚠️
>
> **Non-Commercial Integration** A non-commercial integration is a personal integration developed and used exclusively by an individual or organization to automate their own administration. It is not shared, distributed, sold, or otherwise made available to third parties, and it has no commercial purpose or business model attached.
>
> **Do not share your API-key with others, Billit will never ask for your API key**.

## Requesting Oauth Access

Info : [https://docs.billit.be/docs/how-do-i-request-oauth-client-id-and-secret](how-do-i-request-oauth-client-id-and-secret.md)

Feedback by Billit : Confirmation that your Oauth setup is activated at Billit, with the following details (example) :

> 📘
>
> Sample feedback:
>
> - **clientID**: QPCDzzzKtPI99QzzEVzz
> - **clientSecret**: U9GbSzz3sirizzQWEzzz.

### What is State? (Optional)

- This parameter is **optional**
- This is typically used to prevent cross-site request forgery attacks.
- The state can be a **GUID** or **any other type of content**
- The value will also be present in the redirectURI after a successful login attempt as the state query param.
- The usage of state is required when providing own query params as these are not allowed in the redirect\_uri.
- Multiple parameters will have to be split with any character other than "&" as parameters following the "&" will not be returned in the state after logging in.

### Your Https request - Examples

https without statehttps without state productionhttps with variableshttps with state

```http
https://my.sandbox.billit.be/Account/Logon?client_id=wfefxuglsdolsijqsidjfqsml|kjfiemeimqljf&redirect_uri=https://companyxyz.com/redirect
```

```http
https://my.billit.be/Account/Logon?client_id=wfefxuglsdolsijqsidjfqsml|kjfiemeimqljf&redirect_uri=https://companyxyz.com/redirect
```

```http
https://my.sandbox.billit.be/Account/Logon?client_id={CLIENTID}&redirect_uri={REDIRECTURI}
```

```text
https://my.sandbox.billit.be/Account/Logon?client_id={CLIENTID}&redirect_uri={REDIRECTURI}&state={STATE}
```

### Next step is login by the user: (at least one time)

![](https://files.readme.io/673ddd48ccf10dc72a71c20493cfa0efd42b9b64e248efb822f7796a7038a774-login.png)

The user must have sufficient access to the account of the specific company.

Result after successful login: see below.

### The Redirect Result

The result after a user is redirected back to your site has 2 states, being:

1. When the access is given, the user is allowed temporary access (10 minutes) and is redirected. The redirectURI will contain a query param (starting with ?) -> "code={authorization\_code}"
1. Example : [https://eolauth.xpozzz.be:9999/billit/live/redirect?code=123456789](https://eolauth.xpozzz.be:9999/billit/live/redirect?code=123456789)
2. Next step : request the access and refresh tokens. The access token has en expiry time frame allowing you access as long as it's active, when this token expires you will have to refresh it using the refresh token.
3. Limitations :
      1. use this code only once.
      2. If you did not get and store the redirected information within 10 minutes, you have to start the login again.
2. If the access was denied, the user is redirected and the redirectURI will contain a query param -> "error=access\_denied"

In case of technical problems an error will appear on the screen no feedback will appear in redirectURI.

## Token Requisitioning

POST

```http
https://api.sandbox.billit.be/OAuth2/token
```

### Required POST parameters in Json Body

| Param name | Definition |
| --- | --- |
| client\_id | You received this from Billit at the start |
| client\_secret | You received this from Billit at the start |
| code | The authorization code that came back after login with the query paramater in the redirectURI |
| grant\_type | Fixed value "authorization\_code" |
| redirect\_uri | The URL you provided to Billit when asking for ID and Secret |

When sending the data to Billit make sure that: 1) body type is set to Application/json 2) Do not include authorisation in header 3) Parameters are in Json body (see example below)

Example of a POST [https://api.sandbox.billit.be/OAuth2/token](https://api.sandbox.billit.be/OAuth2/token) content:

JSON body of POST

```json
{
  "grant_type": "authorization_code",
  "code": "545658745",  //{AUTHORIZATION_CODE}
  "client_id": "QPCDzzzKtPI99QzzEVzz",
  "client_secret": "U9GbSzz3sirizzQWEzzz",
  "redirect_uri": "https://staging.companyname.eu/apps/billit_callback"
}
```

### Token requisitioning response

When correctly posting to the Billit API you will have a JSON response coming back. This will look similar to what you see below.

JSON Response

```json
{
  "token_type": "Bearer",
  "expires_in": 3600, //seconds
  "access_token": "{ACCESS_TOKEN}",
  "refresh_token":"{REFRESH_TOKEN}"
}
```

These tokens are also known as bearer tokens, allowing you to call the API in name of the person (login user) who **granted permission** via the OAuth connection.

Text

```text
GET https://api.sandbox.billit.be/v1/orders HTTP/1.1
Authorization: Bearer {ACCESS_TOKEN}
Accept: application/json
```

Expires in : this is always 3600 seconds (1 hour) (fixed value).

## Refresh the Access Token

Access tokens expire, so you need to refresh them. After the time provided in the returned JSON ("Expires\_In") the token will not be valid anymore. If you keep on using it after expiration, you will get the error responsebody : "Code": "AccessTokenExpired". Luckily this does **not** mean the user has to re-authenticate, the API can refresh the access (Refresh can be done without login, also when the previous token has expired).

> 📘
>
> ### Use the correct grant\_type!
>
> Make sure to use the grant\_type "refresh\_token" instead of "authorization\_code" when trying to refresh an expired access token.

### Required POST Parameters

| Param name | Definition |
| --- | --- |
| client\_id | You received this from Billit at the start |
| client\_secret | You received this from Billit at the start |
| grant\_type | Fixed value "refresh\_token" |
| refresh\_token | The refresh token does **not expire** and can only be used **once**. |

This will return a new token which you can use to execute API calls. The result will have the same content as the initial token request, except with different values.

Example of Request URL:

HTTP

```http
POST https://api.sandbox.billit.be/OAuth2/token
```

With Json body:

JSON body of POST

```json
{
  "client_id": "QPCDzzzKtPI99QzzEVzz",
  "client_secret": "U9GbSzz3sirizzQWEzzz",
  "grant_type": "refresh_token",
  "refresh_token": "{The request token from the initial Json response}"
}
```

## Error states

Below examples of error return information for 3 scenario's:

Invalid access tokenAccess token expiredAccess token revoked

```json
{
  "errors": [\
    {\
      "Code": "InvalidAccessToken"\
    }\
  ]
}
```

```json
{
  "errors": [\
    {\
      "Code": "AccessTokenExpired"\
    }\
  ]
}
```

```json
{
  "errors": [\
    {\
      "Code": "AccessTokenRevoked"\
    }\
  ]
}
```

> 🚧
>
> ### Never Share!
>
> Please do not share your ID and Secret to any 3rd party. When Billit sends the data they will remove it from the thread.
>
> **Billit will never ask you to share the Secret or ID again**

Updated13 days ago

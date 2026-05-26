---
title: "Billit API Source Docs - How Do I Get Started With Oauth"
updated: 2026-05-26
---

# How do I get started with OAuth?\n\n**We will try and help you on your way in a few simple steps. If you have any questions please ask us at [support@billit.be](mailto:support@billit.be).**

## What is OAuth   [Skip link to What is OAuth](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#what-is-oauth)

OAuth is a way of letting a customer grant you access to their Billit account and allowing you to perform actions in their name. For this you need to have an OAuth client which needs to be requested, how can be found here [How do I request OAuth Client ID and Secret?](https://docs.billit.be/docs/how-do-i-request-oauth-client-id-and-secret).

Every user you want to get access to as an integrator is required to login using the credentials of your client. After a successful login you can perform actions using the access token in the name of the corresponding user. As the tokens are linked to the client used in the authentication process in Billit. This means that trying to refresh an access token using another client will fail.

Since every user will login using the same client, it is advised to add a unique identifier in the URL used to send the users to the Billit login page to keep track of who is who. This can be achieved by either adding it in the redirect\_uri (a wildcard will need to be set on the Billit side first) or by adding the identifier to the state parameter as these values will be returned after logging in.

The redirect URL provided when requesting an OAuth client is used to send the result to after a login attempt. Thus the place where users are returned to in your website when the authentication was successful or unsuccessful.

> ## 📘  One client to rule them all!
>
> Only you as an integrator need a client, your users do not. They will make use of your client to grant you access.

## Requesting access   [Skip link to Requesting access](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#requesting-access)

Access to a user's profile and companies is requested via the OAuth login, here users can give their consent and grant you the necessary rigths as an integrator. To do this, redirect them to the Billit login with the example link below and fill in the required parameters.

(Required) The client\_id and redirect\_uri are required parameters, if one or both are missing the request will result in an Invalid OAuth2 request and the default Billit login page respectively.

(Optional) The state can be a GUID or any other type of content, the value will also be present in the redirectURI after a successful login attempt as the state query param. This is typically used to prevent cross-site request forgery attacks.

Note: the usage of state is required when providing own query params as these are not allowed in the redirect\_uri. Multiple parameters will have to be split with any character other than "&" as parameters following the "&" will not be returned in the state after logging in.

HTTP

```\1

https://my.sandbox.billit.be/Account/Logon?client_id={CLIENTID}&redirect_uri={REDIRECTURI}&state={STATE}

```

### The redirect result   [Skip link to The redirect result](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#the-redirect-result)

The result after a user is redirected back to your site has 2 states, being:

1. The access was given, the user is allowed temporary access and is redirected. The redirectURI will contain a query param -> "code={authorization\_code}"

2. The access was denied, the user is redirected and the redirectURI will contain a query param -> "error=access\_denied"


If the result is the first option, meaning access has been granted, then you can move on to the next step of requesting the access and refresh tokens. The access token has en expiry time frame allowing you access as long as it's active, when this token expires you will have to refresh it using the refresh token.

## Token requisitioning   [Skip link to Token requisitioning](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#token-requisitioning)

HTTP

```\1

https://api.sandbox.billit.be/OAuth2/token

```

### Required POST parameters   [Skip link to Required POST parameters](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#required-post-parameters)

| Param name | Definition |
| --- | --- |
| client\_id | You received this from Billit |
| client\_secret | You received this from Billit |
| code | The authorization code |
| grant\_type | This has to be "authorization\_code" |
| redirect\_uri | The URL you provided to Billit when asking for ID and Secret |

When sending the data to Billit make sure to set body type to Application/json.

### Token requisitioning response   [Skip link to Token requisitioning response](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#token-requisitioning-response)

When correctly posting to the Billit API you will have a JSON response coming back. This will look similar to what you see below.

JSON

```\1

{
  "token_type": "Bearer",
  "expires_in": 3600,
  "access_token": "{ACCESS_TOKEN}",
  "refresh_token":"{REFRESH_TOKEN}"
}

```

These tokens are also known as bearer tokens, allowing you to call the API in name of the person who granted permission via the OAuth connection.

Text

```\1

GET https://api.sandbox.billit.be/v1/orders HTTP/1.1
Authorization: Bearer {ACCESS_TOKEN}
Accept: application/json

```

Access tokens expire, so you might have to refresh them.

After the time provided in the returned JSON ("Expires\_In") the token will not be valid anymore. Luckily this does not mean the user has to re authenticate but the API can refresh the access.

## Refresh the access token   [Skip link to Refresh the access token](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#refresh-the-access-token)

HTTP

```\1

https://api.sandbox.billit.be/OAuth2/token

```

> ## 📘  Use the correct grant\_type!
>
> Make sure to use the grant\_type "refresh\_token" instead of "authorization\_code" when trying to refresh an expired access token.

### Required POST parameters   [Skip link to Required POST parameters](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#required-post-parameters-1)

| Param name | Definition |
| --- | --- |
| client\_id | You received this from Billit |
| client\_secret | You received this from Billit |
| grant\_type | This has to be "refresh\_token" |
| refresh\_token | The refresh token from the initial JSON response |

This will return a new token which you can use to execute API calls. The result will have the same content as the initial token request, except with different values.

## Error states   [Skip link to Error states](https://docs.billit.be/docs/how-do-i-get-started-with-oauth\#error-states)

Invalid access tokenAccess token expiredAccess token revoked

```\1

{
  "errors": [\
    {\
      "Code": "InvalidAccessToken"\
    }\
  ]
}

```

```\1

{
  "errors": [\
    {\
      "Code": "AccessTokenExpired"\
    }\
  ]
}

```

```\1

{
  "errors": [\
    {\
      "Code": "AccessTokenRevoked"\
    }\
  ]
}

```

Updatedover 1 year ago

* * *

- [How do I request Oauth Client ID and Secret?](https://docs.billit.be/docs/how-do-i-request-oauth-client-id-and-secret)
- [When am I required to use Oauth?](https://docs.billit.be/docs/when-am-i-required-to-use-oauth)

Did this page help you?

Yes

No
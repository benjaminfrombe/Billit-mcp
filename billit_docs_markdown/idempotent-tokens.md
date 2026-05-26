---
title: "Billit API Source Docs - Idempotent Tokens"
updated: 2026-05-26
---

# Idempotent Tokens\n\nOur API supports [Idempotency](https://en.wikipedia.org/wiki/Idempotence). This allow you to safely retry an operation without performing the action twice. This might be useful when something in the process goes wrong.

Lets say you are sending an invoice over the Peppol network. Something goes wrong and the action is not executed. Meaning we did not store the Idempotency token either. This allows you to retry the action. Until the action is successful, since the Idempotency token was not used before.

An idempotency token is a unique key created by the Client which the server uses to recognize subsequent retries of the same request. Allowing us to make sure its unique.

The key is only stored on the server side when the action is successfully executed.

**Usage**

If you want to use the Idempotency token in the API you can by simply adding it to the header of the request.

| Header field name | Header field value |
| --- | --- |
| Idempotency-Key | "Unique value created by the client" |

# How It Works   [Skip link to How It Works](https://docs.billit.be/docs/idempotent-tokens\#how-it-works)

- **Token Generation:** The client generates a unique idempotency token for each operation.
- **Initial Request:** The client includes the idempotency token in the header of the API request.
- **Server Recognition:** The server checks if the token has been used before. If not, it processes the request and stores the token.
- **Retry Attempts:** If the request fails and the client retries, it uses the same token. Since the server recognizes the token, it ensures that the operation is not performed more than once.
- **Token Storage:** The idempotency token is stored on the server side only after a successful operation. If the operation fails and the token is not stored, the client can safely retry without risking duplicate actions.

Updatedabout 1 year ago

* * *

Did this page help you?

Yes

No
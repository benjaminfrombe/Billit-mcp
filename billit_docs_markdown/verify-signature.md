---
title: "Billit API Source Docs - Verify Signature"
updated: 2026-05-26
---

# Verify Signature\n\n## Webhook Signatures   [Skip link to Webhook Signatures](https://docs.billit.be/docs/verify-signature\#webhook-signatures)

We sign all webhooks we send out with a signature. This Signature can be decrypted by using the Secret we provided you when creating the webhook.

### Verifying signatures   [Skip link to Verifying signatures](https://docs.billit.be/docs/verify-signature\#verifying-signatures)

The Billit-Signature header included in each webhook event contains a timestamp and a signature. The timestamp is prefixed by t= and the signature by s=.

Text

```\1

t=1657133145,s=479f86b8baa181b97281b767b8db125cc312d18b3e611d6157571abcd539f09f

```

### 1\. Extract the timestamp and signature from the signature header   [Skip link to 1. Extract the timestamp and signature from the signature header](https://docs.billit.be/docs/verify-signature\#1-extract-the-timestamp-and-signature-from-the-signature-header)

Get the timestamp and signature value by splitting the string by ",".

Next you can split by "=" to get the value of the parameter.

### 2\. Build the signature payload string   [Skip link to 2. Build the signature payload string](https://docs.billit.be/docs/verify-signature\#2-build-the-signature-payload-string)

The signature payload is created by concatenating:

- The timestamp
- The character "."
- The received payload as a JSON string

For example:

Text

```\1

1657133145.{"OrderID":12345,"EntityType":"Order", ...}

```

### 3\. Compare the hash   [Skip link to 3. Compare the hash](https://docs.billit.be/docs/verify-signature\#3-compare-the-hash)

SHA-256 hash the signature payload with the signing secret key as key. Verify the generated hash with the signature extracted from the signature header.

Optionally, you can check if the difference between the current timestamp and the extracted timestamp is within your tolerance.

Updatedover 2 years ago

* * *

Did this page help you?

Yes

No
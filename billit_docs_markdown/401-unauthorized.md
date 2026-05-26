---
title: "Billit API Source Docs - 401 Unauthorized"
updated: 2026-05-26
---

# 401 - Unauthorized\n\nWhen the following 401 error is thrown you do not have access to perform that command. This error can be generated from multiple endpoins. Below you can see some examples.

**Wrong OrderID**

So you are trying to retrieve an order. But the API key or OAuth credentials used do not have access to retrieve that invoice.

**Wrong Party ID**

When creating an order you might use the wrong Customer ID in the Object this could also throw the error since the account does not have permission to use that ID.

Updatedover 2 years ago

* * *

Did this page help you?

Yes

No
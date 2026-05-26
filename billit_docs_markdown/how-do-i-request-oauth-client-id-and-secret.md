---
title: "Billit API Source Docs - How Do I Request Oauth Client ID And Secret"
updated: 2026-05-26
---

# How do I request OAuth Client ID and Secret?\n\nAt Billit we support the usage of OAuth. We would even go as far as having it as a requirement for certain integrations. [When am I required to use Oauth?](https://docs.billit.be/docs/when-am-i-required-to-use-oauth)

**Client ID and Secret for the sandbox environment**

When wanting to have a ClientID and Secret generated on sandbox you can simply send an email to [support@billit.be.](mailto:support@billit.be.) Please also provide the name of the integration and the Redirect URI.

Keep in mind that the URI provided in the redirect\_uri query parameter will be validated and strict matching is used in said process. But don't worry, you're not stuck with the same URI forever, the redirect can be changed when requested.

If you are planning on using your OAuth client in multiple projects then let us know in the request. This way we can allow the different domains to use the same client.

Alternatively, a dynamic redirect URI can be set, for cases such as the same domain in different countries e.g. billit.eu, billit.be and billit.nl. Or when you have similar domains but the relative paths to your callback are different.

If looks applicable to your case, then send us the path and which parts need to be dynamic and we'll set it up for you.

> ## 🚧  Never Share!
>
> Please do not share your ID and Secret to any 3rd party. When Billit sends the data they will remove it from the thread.
>
> **Billit will never ask you to share the Secret or ID again**

Updated25 days ago

* * *

- [When am I required to use Oauth?](https://docs.billit.be/docs/when-am-i-required-to-use-oauth)

Did this page help you?

Yes

No
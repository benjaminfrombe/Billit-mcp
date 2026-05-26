---
title: "Activate on Production"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/activate-on-production-environment"
source_slug: "activate-on-production-environment"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - activate
  - production
  - environment
---

# Activate on Production

When you are ready with testing on the sandbox environment, you are ready to move to production.

Elements to keep in mind:

- Do you need an approval ? See [https://docs.billit.be/docs/approved-process](approval-process.md)
- Create your company or companies on My Billit production and make sure are validations are done [https://docs.billit.be/docs/create-your-account](create-your-account.md)
- Authorisation:
  - Do you use oauth ? Request your client ID and secret for production : [https://docs.billit.be/docs/how-do-i-request-oauth-client-id-and-secret](how-do-i-request-oauth-client-id-and-secret.md)
  - No oauth ? Get your party ID and key : [https://docs.billit.be/docs/partyid-and-key](where-can-i-find-my-companyid-or-a-partyid.md)
- Activate your development on your production software and link it to the Billit Production environment [https://docs.billit.be/docs/sandbox-vs-production-1](sandbox-vs-production.md)
- If you did change some parameters in the Settings of My Billit, apply these settings on My Billit Production.
- Integrations:
  - If Peppol registration/receiving is needed, make sure it is active
  - If registration in a non Peppol network is needed, execute the integration
  - If you require other integrations (sFTP, Accounting Software, BillMail, ...) execute integration on the production environment

You are now ready to start the production !

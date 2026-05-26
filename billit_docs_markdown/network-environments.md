---
title: "Einvoice Network environments"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/network-environments"
source_slug: "network-environments"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - network
  - environments
  - einvoice
---

# Einvoice Network environments

**When I send an invoice will they be delivered?**

It depends on the transport type chosen. There are different networks which we use on our 2 environments

1. Production network = They will be delivered as an official invoice
2. Test network = They will be delivered to the test network of the chosen network type. (If receiver is registered)

| Transport Type | Sandbox | Production |
| --- | --- | --- |
| Peppol | Test network | Production network |
| SDI | Test network | Production network |
| Chorus | Test network | Production network |
| KSeF | Test network | Production network |
| OSA | Test network | Production network |
| Email | Production network | Production network |
| Letter | Disabled on Test | Production network |

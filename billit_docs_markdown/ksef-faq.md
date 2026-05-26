---
title: "FAQ KSeF"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ksef-faq"
source_slug: "ksef-faq"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - faq
---

## Since when KSeF-integration on Production at Billit?

This is possible based on newest FA(3) format since February 1, 2026. Billit does support it in production and on sandbox.

## What About Validation Rules in KSeF ?

- The content of the KSeF XML is verified with an xsd. This verifies the most important rules, but not all. So you can send or receive KSeF XML files with minor errors.
- Duplicate invoices cannot be send : the second (duplicate) will not get a KSeF number.

## What about the KSeF invoice Date ?

- When the invoice is issued at KSeF and a KSeF ID is generated, the official issue data becomes the date of the KSeF registration.
- The invoice should be issued to KSeF at the day of the creation of the invoice
- When KSeF is unavailable, the invoice must be issued within 7 days afther when KSeF becomes available again
  - Note : since February 1, KSeF was always available.

## Sending and Receiving

When activating your KSeF integration:

- You can send invoices to KSeF
- The receiving is also active

You cannot choose just one of both.

## Two Service Providers are active ?

For invoice receiving : When 2 service providers, they will both do the receiving of invoices.

For invoice sending : Sending can also be done by 2 service providers.

## Does API Communication with KSeF have a rate limit ?

Yes, per VAT number (NIP number) there is a limit. Billit communicates per invoice, so per invoice there is a Create Session and a Send Invoice.

The limits:

| Activity | Limit per second | Limit per minute | Limit per hour |
| --- | --- | --- | --- |
| Create Session | 10 | 30 | 120 |
| Send Invoice | 10 | 30 | 180 |
| Get Status | 10 | 120 | 1200 |

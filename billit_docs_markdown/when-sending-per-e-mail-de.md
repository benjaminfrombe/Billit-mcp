---
title: "When sending per E-mail DE"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/when-sending-per-e-mail-de"
source_slug: "when-sending-per-e-mail-de"
category: "peppol-e-invoicing"
topics:
  - peppol
  - invoicing
  - sending
  - per
  - mail
  - de
---

## Define the standard file format to use for customers

When sending per email, you can set a preferred/default file format for all customers. This is in settings, general. Before changing, it has a standard value:

![](https://files.readme.io/d9a0f0baedce2acc6d3a602aba95ab8c304902adaeb4823b4e4f830d2d3ae332-default_ubl_format.png)

You can set this to ZugFeRD (most common format)

![](https://files.readme.io/42d11262b89c4a4800d8fd8bf03c312106343ae6cc35ea16d780de582948708d-zugferd.png)

Or to XRechnung:

![](https://files.readme.io/27d08ae547f56f971a398f3278313d44c383588ba64deabd841004d2c9bfc783-xrechnung.png)

## Settings per customer

The **language** of the Email can be set:

- in the API content, e.g. "Language" : "DE"
- in the MyBillit user interface, in the Customers Section. Set "Language" to the currect value

The File format for the customer can be set:

- not specified, then the default file format will be used
- set a specific file format (other then the default) :
  - in the MyBillit user interface, in the Customers Section, the specific file format can be chosen

Summary of the screen element in the MyBillit user interface

![](https://files.readme.io/6cad46835438f434f1fc53ef77401c6f0cdb6753ea6014ebd614e25bc79ae1ba-2026-04-22_11-40-03.png)

Extra info:

1. Customer Email Address (can also be delivered via API)
2. Language of the customer (can also be delivered via API)
3. Sending method (can also be delivered via API)
4. XML format : If a format is set, this will be used (default in settings not taken into account). (cannot be delivered via API)
5. Send PDF:
1. If yes : Email will contain an XML and and PDF
2. If no: only an XML (remark : when format is ZUGFeRD, it will only be a PDF)

## About Email setup

- make sure that your email adress in MyBillt / My company is verified
- If you want to send from your own email address: see info : [https://www.billit.eu/en-int/help-page/settings/email-settings/sending-from-your-own-email-address/](https://www.billit.eu/en-int/help-page/settings/email-settings/sending-from-your-own-email-address/)

Updatedabout 1 month ago

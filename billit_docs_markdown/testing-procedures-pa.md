---
title: "Testing Procedures"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/testing-procedures-pa"
source_slug: "testing-procedures-pa"
category: "partner-france"
topics:
  - partner
  - france
  - testing
  - procedures
  - pa
---

## What can be tested on the sandbox environment

What can be tested:

- Billit environment sandbox
- Sender : your own company
- When launching the sending via Billit
  - Step 1 : Communication with the French Tax Authority :
    - Method : this will be mocked.
    - What does it mean : Billit simulates this communcation with the French Authority, as communication capabilities in the test environment is limited.
    - Value of this operation : You will be able to understand what are the types of messages and status information you can get back
  - Step 2 : send via Open/Peppol : real sending to the restrictied number of receivers available on the test network.

## Which receivers are available on the test network

Only a very limited number of receivers are available on the French test network, as the allowed use is very limited.

Below the options:

- You can upload your customer list in the Billit sandbox and check which customers are on the Peppol network. Ideally, they are also registered with the CTC extension (identifier scheme 0225) and with correct document types.
- You can send to Billit test receivers. Info see below.

### Billit test receiver simulating a positive delivery

- Data about the company
  - Name : FR demo receive
  - VAT : FR37127362116
  - Siren : 127362116
  - CTC : 127362116\_DEMO
- Make sure that the CTC is used as customer endpoint ID. You can set this in the following way:

![](https://files.readme.io/3be84dcc50fba225d5b338c1611cc60d32ad2488062adc79ee283902b723b66b-customer.png)

### Billit test receiver simulating a negative feedback from the French Authority

You can crrate a test customer with following data

- Name : free to choose
- VAT : a valid French VAT number of choice (must be filled in)
- Siren : derived from the VAT number (VAT number excluding FR)
- CTC : this must be 227010068\_ERROR
- Address : fill in the French address with test data of choice

Updated7 days ago

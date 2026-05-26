---
title: "B2B Sending Flows"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/b2b-sending-flows-pa"
source_slug: "b2b-sending-flows-pa"
category: "partner-france"
topics:
  - partner
  - france
  - b2b
  - sending
  - flows
  - pa
---

## Which Flows are involved for Domestic B2G invoicing

For French domestic B2B einvoicing, 3 flows are concerned:

| Flux | Description |
| --- | --- |
| Flux 1 | Report invoice to French tax authorities |
| Flux 2 | Create and deliver invoice to the receiver |
| Flux 6 | Status exchanges between the parties |

## Communications between Seller and Billit for Domestic B2B

As a Seller/Supplier working with Billit, you only need to activate a limited number of communications.

Schematic overview of 3 types of Communication when using Billit API's:

![](https://files.readme.io/50eb536c41c8885ee2e24d5ee8a7ba809667b8c8d20ef1c9cef1427df761e893-2026-03-23_08-17-50.png)

Explanation of the Billit activities:

- A. API Submit / Send Invoice
  - Submit API content to Billit
    - positive result : status code 200 and OrderID are returned
  - Launch the sending of the Invoice : via API or automatic sending next day
- B. Capture feedback messages, options:
  - Perform API GET of the messages on a regular base
  - Activate webhooks
  - Or no integration needed, just view the messages on the MyBillit Billit user interface
- C. Send status back : payment received
  - When payment is received, this status is returned to the network via API

## Global Process Overview B2B Domestic

When sending B2B domestic invoices from a French supplier to a French B2B customer, the the following 3 flows are involved:

| Flow/Flux | What |
| --- | --- |
| Flux 2 | Submit Invoice and Credit Note |
| Flux 1 | E-reporting to Government |
| Flux 6 | Status Exchange |

As a Seller/Supplier, the communications with Billit are limited to the 3 communications above.

Below a diagram of the Global Flow allowing a more global understanding (sales invoice).

![](https://files.readme.io/9c8b7a7c65e8d2b1d41ebe1c51119f7bfa31e789a14795d335f3c6806683c8bb-2026-03-26_14-13-17.png)

More information:

1. PPF
   - 1 : start with status exchange between Billit and PPF (Flux 6):
     - send status 200 (automatically done by Billit)
     - get status 500, 250 (stored by Billit in messages)
   - 2 : Ereporting Flux 1 (automatically done by Billit)
     - Billit ereport to PPF
     - Get return statusses 500, 250, 280, 281 (stored via Billit - messages segment)
   - 3 : Sending
     - 3a Sending (by Billit)
       - Sending of the notification 201 to the service provider of the buyer (flux 6)
       - Sending of the invoice Flux 2
     - 3b Return statusses
       1. Get return statusses 202, 203 (stored via Billit - messages segment)
   - 4 : Communication between Service Provider Buyer and Customer
     - 4a Service Providers delivers invoice to Customer (Flux 2)
     - 4b Service Provider Customer gets status from Customer (Flux6),
       - can be one or multiple status messages as there are several optional statusses
   - 5 : Payment
     - 5a Payment received by Seller notifications (Flux 6)
       - Notification sent to the Service Provider Buyer
       - +Notification sent to the PPF (status code 250)

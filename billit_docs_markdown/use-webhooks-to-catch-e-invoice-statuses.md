---
title: "Billit API Source Docs - Use Webhooks To Catch E Invoice Statuses"
updated: 2026-05-26
---

# Use webhooks to catch E-Invoice statuses\n\nWhen setting up an E-Invoice project the statuses are even important then sending the invoice it self. With the webhook on the messages you can a Ping-Pong like setup which allows you to retrieve E-Invoice statuses without having to poll the API.

Below we will demonstrate a low level webhook setup that allows you to easily read the invoice statuses without having retrieve the invoice.

> ## 🚧  This will only work if you store the unique OrderID's when creating an invoice

### Step 1 - Create the webhook [Create Webhook](https://docs.billit.be/reference/v1webhooks-2)   [Skip link to Step 1 - Create the webhook ](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses\#step-1---create-the-webhook-create-webhook)

First you start by creating the webhook. This one will be registered on the Message entity.

Create Message webhook

```\1

{
     "EntityType": "Message",
     "EntityUpdateType": "I",
     "WebhookURL": "Your webhook url"
}

```

### Step 2 - Setup the backend   [Skip link to Step 2 - Setup the backend](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses\#step-2---setup-the-backend)

When you have created the Webhook you should have received a Secret. Please store this secret and do not share this with anyone. (Not even with Billit employees!)

You can then setup the listener and Signature validator (Optional, but recomended). [Verify Signature](https://docs.billit.be/docs/verify-signature)

### Step 3 - Receive webhooks   [Skip link to Step 3 - Receive webhooks](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses\#step-3---receive-webhooks)

From this point you can receive webhooks. Every time you send an invoice and the message object is filled with new information you will be notified. This can be a new IMR (Invoice message response from Peppol) or a status file from the SDI network.

A response can look like the following.

Webhook response

```\1

{
    "UpdatedEntityID": 100, //(MessageID)
    "UpdatedEntityType": "Message",
    "WebhookUpdateTypeTC": "U",
    "EntityDetail" :
    {
        "OrderID" : 2000,
        "Description" : "Description",
        "FileID" : "GUID-GUID-GUID",
        "CreationDate" : "31/01/2000",
        "TransportType" : "Peppol", //(Peppol, SDI, Email,...),
        "Destination" : "BE1234568",
        "MessageDirection" : "Incoming",
        "MessageAdditionalInformation" :
        {
            "EInvoiceFlowState": "Refused", //Sent,Delivered,Accepted,Refused
            "AdditionalFlowStateInformation": "No Valid VAT"
        }
    }
}

```

Above you can see that the messageID is 100, but the corresponding invoice is 2000. We have added the description and also the FileID. This allows you to instantly retrieve the Original file sent or received if you would like to use this in a further flow.

But probably the most important one is the EInvoiceFlowState. This state allows you to see the status of the invoice with out reading the files or description. So if desired you can only use this state and be ready.

### The states are the following:   [Skip link to The states are the following:](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses\#the-states-are-the-following)

" **Sent**" is the first one. the moment the queue picks up the invoice you will receive this webhook.

Followed by " **Accepted**" this means the Accespoint or network as succesfully acknowledged the invoice.

then there are 2 final states:

" **Delivered**" the invoice is Delivered at the end customer and this is the final state of this E-Invoice life cycle.

" **Refused**" the invoice is refused by the customer or government system. The information might be avaible in the API. If not fully clear you can download the file with the refusal reason attached.

Updatedabout 2 years ago

* * *

Did this page help you?

Yes

No
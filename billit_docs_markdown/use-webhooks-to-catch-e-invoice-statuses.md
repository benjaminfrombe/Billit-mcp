---
title: "Use webhooks to catch E-Invoice statuses"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses"
source_slug: "use-webhooks-to-catch-e-invoice-statuses"
category: "webhooks-status"
topics:
  - webhooks
  - status
  - use
  - catch
  - invoice
  - statuses
---

# Use webhooks to catch E-Invoice statuses

When setting up an E-Invoice project the statuses are even important then sending the invoice it self. With the webhook on the messages you can a Ping-Pong like setup which allows you to retrieve E-Invoice statuses without having to poll the API.

Below we will demonstrate a low level webhook setup that allows you to easily read the invoice statuses without having retrieve the invoice.

> 🚧
>
> ### This will only work if you store the unique OrderID's when creating an invoice

### Step 1 - Create the webhook [Create Webhook](https://docs.billit.be/reference/v1webhooks-2)   [Skip link to Step 1 - Create the webhook ,[object Object]](https://docs.billit.be/docs/use-webhooks-to-catch-e-invoice-statuses\#step-1---create-the-webhook-create-webhook)

First you start by creating the webhook. You have the ability to create 4 webhooks for one PartyID.

When you create the Webhook, a Message confirmation will be be sent as a webhook. This message does contain the secret.

Via a GET Webhook command you can GET the information also (does not include the secret).

You could setup 4 types of webhooks per party ID:

| Type | Action Code | Action Description |
| --- | --- | --- |
| Order | I | Insert : at initial creation of the document |
| Order | U | Update : any update after creation |
| Message | I | Insert : at initial creation |
| Message | U | Update : any update (Messages are mostly updates) |

Below 4 examples of Webhooks :

Create Message webhook IUpdate Message WebhookCreate Document WebhookUpdate Document Webhook

```json
{
     "EntityType": "Message",
     "EntityUpdateType": "I",  // I for Insert
     "WebhookURL": "https://xyz.com/zaSyDdI0hCZtE6vy"
}
```

```json
{
     "EntityType": "Message",
     "EntityUpdateType": "U",  // U for Update
     "WebhookURL": "https://xyz.com/zaSyDdI0hCZ78oy1"
}
```

```json
{
     "EntityType": "Order",
     "EntityUpdateType": "I",  // I for Insert
     "WebhookURL": "https://xyz.com/zaSyDdI0hCZtE6vy"
}
```

```json
{
     "EntityType": "Order",
     "EntityUpdateType": "U",  // U for Update
     "WebhookURL": "https://xyz.com/zaSyDdI0hCZ78oy1"
}
```

### Step 2 - Setup the backend

When you have created the Webhook you should have received a Secret. Please store this secret and do not share this with anyone in the outside world. (Not even with Billit employees)

You can then setup the listener and Signature validator to increase the reliability (Optional). [Verify Signature](verify-signature.md)

### Step 3 - Receive webhooks

From this point you can receive webhooks. Every time you send an invoice and the message object is filled with new information you will be notified. This can be a new IMR (Invoice message response from Peppol) or a status file from the SDI network.

Below examples of webhook feedbacks (type : Message) when posting an invoice via API and sending via open/Peppol. Summary of the messages for this scenario:

| Message | Available Information |
| --- | --- |
| First Message (Insert) | OrderID, Destionation, CreationDate |
| Second Message (Update) | +Success, Trials, EinvoiceFlowState, FileID |
| Third Message (Optional / Insert) | +Description with IMR, fileID of IMR, Destination is Incoming |
| When Invoice is refused | EinvoiceFlowState / AdditionalFlowStateInformation / FileID of IMR |

Examples:

Webhook 1 : Creation MessageWebhook 2 : Status Update MessageWebhook 3 : Update Message IMRRefused

```json
{
  "UpdatedEntityID": 690998,
  "UpdatedEntityType": "Message",
  "WebhookUpdateTypeTC": "I",  //First message for this OrderID
  "EntityDetail": {
    "OrderMessage": {
      "OrderID": 2615999, //Unique Key for the matching
      "CreationDate": "2026-05-04T09:55:34.063",  //Time stamp of creation of the order
      "TransportType": "Peppol",
      "Trials": 0,
      "Destination": "9925:BE0759529999",
      "MessageDirection": "Outgoing"
    },
    "AdditionalMessageInformation": {}  //Not available yet
  }
}
```

```json
{
  "UpdatedEntityID": 690998, //(MessageID is the same as the inital ID of Webhook Insert Message)
  "UpdatedEntityType": "Message",
  "WebhookUpdateTypeTC": "U", // Update info after previous creation message
  "EntityDetail": {
    "OrderMessage": {
      "OrderID": 2615999,  //Unique Key for the matching
      "FileID": "bc9996b3-e2ef-4476-9873-28de2c61d999",//The UBL/XML file ID is included in this Update message
      "CreationDate": "2026-05-04T09:55:34.063",  // Date time of the first Creation Message
      "TransportType": "Peppol",
      "Success": true,  //Confirmation that delivery on Peppol is now successful.  When false : failed
      "Trials": 0,  //First attempt was successfule.  Count will increase when Billit has to perform retries.  When Success status is false, then no further retries will be performed.
      "Destination": "9925:BE0759529999",
      "MessageDirection": "Outgoing"
    },
    "AdditionalMessageInformation": {
      "EInvoiceFlowState": "Sent"  //Sent,Delivered,Accepted,Refused  (see description of the states)
    }
  }
}
```

```json
{
  "UpdatedEntityID": 690999,  //new ID as IMR is a new received message linked to OrderID
  "UpdatedEntityType": "Message",
  "WebhookUpdateTypeTC": "I",
  "EntityDetail": {
    "OrderMessage": {
      "OrderID": 2615999,  //OrderID of the sent invoice
      "Description": "AB: The document has been successfully received.",  //IMR code and description
      "FileID": "2320bea9-56d9-4185-a7c0-f1f2c9b999b9",  //File ID of the IMR
      "CreationDate": "2026-05-04T10:07:50.69",  //Creation date is date of the IMR receiving/processing in Billit
      "TransportType": "Peppol",
      "Success": true,
      "Trials": 0,
      "Destination": "9925:BE0759529202",
      "MessageDirection": "Incoming"  //After sending of the invoice, the IMR is received, so it is incoming direction
    },
    "AdditionalMessageInformation": {
      "EInvoiceFlowState": "Delivered"
    }
  }
}
```

```json
{
    "UpdatedEntityID": 690988, //(MessageID)
    "UpdatedEntityType": "Message",
    "WebhookUpdateTypeTC": "U",
    "EntityDetail" :
    {
        "OrderID" : 455654,
        "Description" : "Description",
        "FileID" : "2320bea9-56d9-4185-a7c0-f1f2c9b999b8",
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

The messages related to Orders will be much shorter.

### EinvoiceFlowState Values

" **Sent**" is the first one. the moment the Billit sending queue picks up the invoice you will receive this webhook. This status indicates that the receiver data are correct and that the content complies with the network requirements.

Followed by " **Accepted**" this means the network has succesfully acknowledged the invoice. (This is only for some networks).

then there are 2 **optional** final states:

" **Delivered**" the invoice is Delivered at the end customer and this is the final state of this E-Invoice life cycle. This can only happen when a customer does send an optional response to the sender (in case of Peppol : IMR/MLR).

" **Refused**" the invoice is refused by the customer or government system. The information might be avaible in the API. If not fully clear you can download the file with the refusal reason attached. This can only happen when a customer does send an optional response to the sender (in case of Peppol : IMR/MLR).

When Refused then additional field can be included, example : "AdditionalFlowStateInformation": "No Valid VAT"

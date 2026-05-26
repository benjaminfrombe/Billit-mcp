---
title: "sFTP Setup"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sftp-setup"
source_slug: "sftp-setup"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - sftp
  - setup
---

## Concepts

High level process view when sending sales invoices using sFTP: [https://www.billit.eu/media/vp1lqxaj/sftp-or-other-diagram.pdf](https://www.billit.eu/media/vp1lqxaj/sftp-or-other-diagram.pdf) ( [https://www.billit.eu/media/vp1lqxaj/sftp-or-other-diagram.pdf](https://www.billit.eu/media/vp1lqxaj/sftp-or-other-diagram.pdf))

sFTP accounts:

- Make sure you have access to a SFTP server and that you get connection information, including user and password.

2 Categories of Invoices can be Processed:

- Sales Invoices (Income, AR) : Files stored on the sFTP will be uploaded by Billit for sending.
- Purchase Invoices (Expense / AP) : Files received by Billit will be exported to SFTP for further processing by the accounting or ERP-software.

## Where to Find the sFTP Integration Setup

Action in order to start the setup :

![](https://files.readme.io/1ad9d01e029d82eedf89d6b62277eec983cd1cf4d9c08bc0654fb8cc5ed5559d-Afbeelding1.png)

## General Overview Configuration Options

General capabilities are described in this section, practical examples in the next point.

- Basic sFTP connection data
  - Type : sftp/ftps
  - Host/port
  - Username/Password
- Private Key file / password for private key.
  - This optional settings allows combined verification of private key and public key (stored on sftp server) for additional security.
- Folder name where we can insert the invoices :
  - Sales/income : upload folder of the invoices
- Invoice type to place in folder: Expense (when receiving supplier invoices) and income (when sending sales invoices)

- Insert pdf into folder.
  - Minimum input is XML file.
  - When PDF is delivered as a separate file (with same name as XML), then activate this.
- Folder name where we can extract the invoices (NL : “Mapnaam waar we de facturen mogen in plaatsen”)
  - When Invoice type to place in folder = Expenditure: Export of the received files to this folder after processing. Customer can upload from here.
  - When Invoice type to place in folder = Income. When the delivery to network is done, file can be inserted here.
- Folder name where we can extract the invoices:
  - Upload file and bring it to the Fast Input.
  - This can be useful for uploading, uploading to fast input. This allows verification by human being (via parameter can be automatic).
- Sync invoices in Billit from : date filter. Older files will not be uploaded.

- Create new 'success' folder for each day
  - This might be easier when you have larger volumes. You see all the invoices of one day together.
- Filters - Prefix file name (optional). Only download files whose filename starts with the specified filter.
  - Example of use: files for multiple companies arrive on one directory. Per company an sftp is linking to the same folder. If prefix contains info about the company, filtering helps to only process files of that company.
- Filters - Suffix file name (optional)
  - Same as previous but at the end of the word
- Filters - File extension (optional)
  - E.g. if no zip or pdf is needed, then deactivate these extensions. Files will stay on the directory.
- Filters - Sent status (optional) Mark the invoices as Sent for file names that contain the following word.
  - When customer is also sending files that do not have to be processed, activating the filter allows to move it directly to the success folder
- Filters - Export invoices (optional)
  - After creating an invoice put it in the file that includes the following word in the file name
- **Zip attachments** :
  - Name of the option: PDF files as attachment Download PDF files and add them as attachment to an existing invoice.

  - The PDF files should be zipped and the file name (of the .zip) should correspond exactly to the invoice number in Billit. The file name of the file in the Zip is free.

  - Sequence must be correct:
    - First upload the XML file (processed each 20 minutes)
    - Then (after the successful upload of XML), upload the .zip file (e.g. 1 hour later, then XML is processed) Zip the same file name. The zip file will then be linked to the invoice in Billit.
    - Mixed use of invoices with Zip and invoices without Zip is allowed.
- Processing successfully read files
  - Move to success folder: after success moved to this auto created folder.
    - Gives more ability to verify (and possibly reload).
    - Requires more storage space and cleanup afterwards.
  - Delete from folder (no cleanup later needed)

## Summary for Uploading Attachments

- No attachment needed: just insert XML files
- Include attachments, 3 scenario's:
  - Scenario 1 : Attachment is XML as encoded object
  - Scenario 2 : 1 XML, 1 PDF attachment
  - Scenario 3 : 1 XML, 1 PDF attachment
  - Scenario 1 + 2 : XML with encoded object + PDF attachment
  - Scenario 1 + 3 : XML with encoded object + ZIP attachment

## Polling Frequency

Each 20 minutes.

## Uploaded from sFTP : What does it mean ?

Uploaded with success, what is does mean:

- Document is transferred to Billit with success (so minimum arriving in the fast input)

What it does not mean:

- Content is fully correct correct
- Can be uploaded in Billit for further processing.

What happens if Billit cannot process the content of the file:

- File will stay a while in Billit in Fast Input trying to process
- Finally will be presented as file in error in Fast Input

---
title: "sFTP Example for Sales Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sftp-setup-example-salesinvoice"
source_slug: "sftp-setup-example-salesinvoice"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - sftp
  - setup
  - example
  - salesinvoice
  - sales
---

## Description of Scenario

Scenario:

- Billit receives the incoming purchase invoices
- Billit Exports to the sFTP

## Config Details

Example of a setup:

![](https://files.readme.io/74ebd7a5872686b72a2bcc2870c06eea963755dd0845d7cdaafc4b0b7b4a9a77-Conif_details.jpg)

Explanation of the Points with Coloured Digits:

1. sFTP Login Data

Provide the required sFTP login credentials for system access.
2. Income

Income invoices will be processed automatically.
3. PDF Upload Setting

Indicates whether PDFs should be inserted into the folder.

1. Yes: for each XML a seperate PDF is expected with the same name als the XML. If the PDF is not present, the UBL will not be uploaded.
2. No: only UBL will be inserted, seperate PDF file will not be uploaded.
3. In both cases, when PDF is embedded in UBL as encoded object, it will be uploaded.
4. Input Folder for Sales Invoices

This is the folder from which Billit will upload XML files for processing. The expected format is UBL; any other format will require additional mapping by Billit.
5. Daily Success Folder

A new success folder can be created each day. This setting is linked to point 7. If point 7 is configured to "move to success folder," you may choose to create a daily subfolder. This can make monitoring easier and may improve performance.
6. Allowed File Types

Define the default file types permitted for processing. These settings can be configured to be as strict as required.
7. Post-Processing Action

Specify what happens after successful processing: either delete the files or store a copy in the success folder.

Remark: **PDF Files as Zipped attachment** : see documentation about correct use : [https://docs.billit.be/docs/sftp-setup](sftp-setup.md)

## Uploaded from sFTP : What does it mean ?

Uploaded with success, what is does mean:

- Document is transferred to Billit with success (so minimum arriving in the fast input)

What it does not mean:

- Content is fully correct correct
- Can be uploaded in Billit for further processing.

What happens if Billit cannot process the content of the file:

- File will stay a while in Billit in Fast Input trying to process
- Finally will be presented as file in error in Fast Input

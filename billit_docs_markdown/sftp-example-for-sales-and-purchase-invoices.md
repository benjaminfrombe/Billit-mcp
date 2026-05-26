---
title: "sFTP Example Sales and Purchase Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sftp-example-for-sales-and-purchase-invoices"
source_slug: "sftp-example-for-sales-and-purchase-invoices"
category: "receiving-inbox"
topics:
  - receiving
  - inbox
  - sftp
  - example
  - sales
  - purchase
  - invoices
---

## Config Details

Example of a setup:

![](https://files.readme.io/7dc978e82cfc194b0f6d22ac009d6b5971b895171355a957d4516b52580b94ee-sales_purchase.jpg)

Explanation of the Points with Coloured Digits:

1. sFTP Login Data

Provide the required sFTP login credentials for system access.
2. Export Folder (Cost Invoices)

This is the export folder for Billit. By default, export files are in UBL format, and attachments are included as embedded objects.
3. Types:
1. No Selection : Both expense and income invoices will be processed.
2. Expenditure : only expenses
4. PDF and source UBL:
1. Insert PDF into folder : Upload Setting. Indicates whether PDFs should be inserted into the folder. Set to No if PDFs should not be exported.
2. Export Source UBL if present: if Yes : The file received from the source will be exported as UBL, without any change (only valid for receivings in UBL format)
3. Export as file type:
      1. if previous point is yes : will be the source file
      2. if previous point is no : will convert to the selected file format
5. Input Folder for Sales Invoices

Billit will upload XML files from this folder for processing. The expected format is UBL; any other format requires additional mapping by Billit.
6. Daily Success Folder

A new success folder can be created each day. This setting is linked to point 8. If point 8 is configured to "move to success folder," you may choose to create a daily subfolder. This can make monitoring easier and may improve performance.
7. Allowed File Types

Define the default file types permitted for processing. These settings can be configured to be as strict as required.
8. Post-Processing Action

Specify what happens after successful processing: either delete the files or store a copy in the success folder.

Remark: **PDF Files as Zipped attachment** (sales invoices): see documentation about correct use : [https://docs.billit.be/docs/sftp-setup](sftp-setup.md)

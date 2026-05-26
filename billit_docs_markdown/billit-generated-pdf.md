---
title: "Billit Generated PDF"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/billit-generated-pdf"
source_slug: "billit-generated-pdf"
category: "files-documents"
topics:
  - files
  - documents
  - billit
  - generated
  - pdf
---

## How to edit the Content of the Template

The content can be edited. Documentation on the Billit help pages:

- English: [Layout templates](https://www.billit.eu/en-int/help-page/invoice-layout/layout-templates/)
- Dutch: [Lay-outtemplates](https://www.billit.eu/nl-be/helpartikelen/factuurlay-out/lay-outtemplates/)
- French: [Modèles de mise en page](https://www.billit.eu/fr-be/articles-d-aide/mise-en-page-de-la-facture/modeles-de-mise-en-page/)

## How to start with the editing of the Template

Go to Settings, Corporate Style:

![](https://files.readme.io/dc4f09b2c89acdc0844ffde51862756a8af9dfc189ed85ebf0b2ee333e162777-2025-10-28_08-08-44.png)

Edit the types Invoice and Credit Note:

![](https://files.readme.io/14fd8680ecd0e84f260fdac2831eb4c5b4f055278fa099d88f87b6032853a35d-2025-10-28_08-09-59.png)

## What Information can be Edited on the Template

The fields marked in the menu "Keys" can be inserted into the template:

![](https://files.readme.io/e9894f466ea7327d47f0cfd9b1877cff5574fe3d10895f53b3c7a48223da4c13-2025-10-28_08-14-55.png)

Additional information:

- Fixed text can be added. It will appear as the same text in all languages.
- If you want to add information on the template that is not part of the allowed values in Keys:
  - On header level put the information in the Json tag "Comments". This corresponds to the Template variable $Order.Comments$. Here you can put multiple values preceded by the title. The content will appear the same for all languages.

## Language of the Template

The language is set automatically based on the language of the selected customer.

So there is no need to create a template for each language.

## How to Include your Logo and Terms and Conditions

Go to "My company", workshet company and scroll to the bottom for Company Settings:

![](https://files.readme.io/bcffec9735e33a6477eb0292d5785ae2c338945d6aeb7bde3d07abf179ae890c-2025-10-28_08-21-38.png)

Here you can upload:

- One logo for the company (cannot be inserted via API)
- 1x Terms and Conditions (1 version for the company, valid for all languages). Remark: most senders refer to their website for the Terms and Conditions, they do not include Terms and Conditions as an attachment.

## Other document types than Invoice and Credit Note

Templates are also available for:

- other doctypes: Quotation, Order, Delivery note
- Cover letters : the text of the cover letters used when sending per email

## Multiple Templates for one document type

It is possible to create multiple templates for document type.

The template can be selected manually in the MyBillit interface when sending an email, but not via API.

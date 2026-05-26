---
title: "Possible Errors"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/possible-errors"
source_slug: "possible-errors"
category: "reference-errors"
topics:
  - reference
  - errors
  - possible
---

# Possible Errors

Error code 400 indicates that Billit has detected an error. When receiving an error 400 then the this is a Business type exception. The invoice will not be sent.

Many errors will be related to a non compliant UBL files. The best option is to validate your UBL with one of the Peppol validation tools.

Below additional information about the most common Billit errors.

| Value (example) | Sample value |
| --- | --- |
| "Code" : "TheCustomerDoesNotSupportPeppolForType\_0" "Description" : "De klant ondersteunt geen Peppol voor type Invoice" | This can be related to the Party Customer and/or the party Supplier. 1) Customer (no Peppol receivings for the Customer endpoint ID) check the Peppol registration of the customer. (If sandbox check Peppol test environment. If production check Peppol production environment). 2) For the Supplier : VAT number or Company Number is not correct or not the same as the Company registration at MyBillit. Compare MyBillit company settings with UBL Supplier data. |
| "Code" : "GenericError" "Description" : "A buyer reference or purchase order MUST be provided" | Make sure that in UBL the tags OrderReference/ID or Buyer Reference. |
| "Code": "GenericError" "Description" : "Data is Required" | This is a more basic error that can point to several things. Make sure that all structured IDs have a backslash e.g. schemeID= "0208". Check the compliance of your UBL (excluding the backslash signs) via a Peppol validation tool, correct the UBL and continue with Billit testing when the UBL errors are removed. |
| "Code": "Generic Error". "Description: Invoice Line net amount must equal (Invoiced quantity \* (Item net price/item price base quantity) + Sum of invoice line charge amount - sum of invoice line allowance amount) | The amount validations give an error. Improve the content until alle volumes and prices are correct. |
| "Code": "Generic Error". "Description: \[BR-S-08\] - For each different value of VAT category rate........... " | Check the VAT percentages and all VAT data in your UBL |
| "Code": "Generic Error". "Description: Sequence contains no elements" | In the UBL there are syntax errors, or certain tags are punt in a wrong sequence |
| "Code": "Generic Error". "Description: Document must not contain empty elements" | Certain tags in the UBL are present but the content is empty. Action : 1) add content or 2) If not mandatory remove the tag. |
| "Code": "Generic Error". "Description : The element 'Invoice' in namespace ..... has invalid child element 'Note' in namespace ........" | Check the tag referenced (e.g. Note) and check it is an allowed tag and that it is put in the right sequence in the UBL. |

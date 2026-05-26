---
title: "Bank Accounts"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ksef-bank-accounts"
source_slug: "ksef-bank-accounts"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - bank
  - accounts
---

## Make sure that Bank Accounts are defined in Billit

Preparations:

- make sure multiple bank accounts are created in Billit (My Company / Bank Accounts)
- It is recommended that the bank accounts are verified (production)

Example of multiple bank accounts created in Billit:

![](https://files.readme.io/1bc354c604537b3eba6511b51f63feb18f60f641a35df3df3aabdacbed94fad1-2026-04-27_08-27-58.png)

Include one bank account number in the Json body on the header level (not in the supplier segment). Example Below. If no IBAN is included, Billit will add the default bank.

## When working with one Bank Account

Example of Bank info in the header of the Json:

Header Bank Info

```json
    "IBAN": "PL30160010840004050120499999",
    "BIC": "PPABPLPK"
```

## Add Additional Bank Account Numbers

Via custom field on header more bank account numbers can be added.

You have two options:

- First bank via IBAN, from second bank on via custom fields
- All banks in the custom fields

Example:

Second BankMultiple Additional Banks

```json
  "CustomFields": {
        "Faktura.Fa.Platnosc.RachunekBankowy2.NrRB" : "PL571600108400040501204999999",
        "Faktura.Fa.Platnosc.RachunekBankowy2.SWIFT" : "PPABPLPK"
    }
```

```text
  "CustomFields": {
        "Faktura.Fa.Platnosc.RachunekBankowy2.NrRB" : "PL571600108400040501204999999",
        "Faktura.Fa.Platnosc.RachunekBankowy2.SWIFT" : "PPABPLPK",
        "Faktura.Fa.Platnosc.RachunekBankowy3.NrRB" : "PL571600108400040502174999999",
        "Faktura.Fa.Platnosc.RachunekBankowy3.SWIFT" : "PPABPLPK"
    }
```

Result in the KSeF XML (total of 2 bank accounts)

![](https://files.readme.io/c7ab4843ba84c82bf3e0a3821b6100f8e7ffaaa6265f106657299bc18a5529f2-banks.png)

Limitation:

- The additional bank account(s) cannot be added in case of CreditNote (KOR) (CreditNote : bank accounts are never included in KSeF XML by Billit)

## Include Name and Description of the Bank Account (Header)

It might be interesting to add additional information about the bank accounts:

- Name of the bank
- Description: here you can add information : why to pay on this bank account. E.g. bank account has specific currency.

Status : available since 20/05/2026.

Examples how to set up : (3 Scenario's):

1\. default bank2\. Default Bank + 1 extra bank3\. Default Bank + 2 extra banks

```json
 "CustomFields": {
        "Faktura.Fa.Platnosc.RachunekBankowy.NazwaBanku": "Name of Bank",
        "Faktura.Fa.Platnosc.RachunekBankowy.OpisRachunku": "Description"
 }
```

```json
"CustomFields": {
        "Faktura.Fa.Platnosc.RachunekBankowy1.NazwaBanku": "Name of Bank",
        "Faktura.Fa.Platnosc.RachunekBankowy1.OpisRachunku": "Description",
        "Faktura.Fa.Platnosc.RachunekBankowy2.NazwaBanku": "Name of Bank",
        "Faktura.Fa.Platnosc.RachunekBankowy2.OpisRachunku": "Description"
}
```

```text
"CustomFields": {
        "Faktura.Fa.Platnosc.RachunekBankowy.NazwaBanku": "Name of Bank",  // Name for the default bank.
        "Faktura.Fa.Platnosc.RachunekBankowy.OpisRachunku": "Description"  // description for the default bank
 				"Faktura.Fa.Platnosc.RachunekBankowy1.NazwaBanku": "Name of Bank",
        "Faktura.Fa.Platnosc.RachunekBankowy1.OpisRachunku": "Description",
        "Faktura.Fa.Platnosc.RachunekBankowy2.NazwaBanku": "Name of Bank",
        "Faktura.Fa.Platnosc.RachunekBankowy2.OpisRachunku": "Description"
}
```

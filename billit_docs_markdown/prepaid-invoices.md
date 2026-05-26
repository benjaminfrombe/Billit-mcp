---
title: "Prepaid Invoices"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/prepaid-invoices"
source_slug: "prepaid-invoices"
category: "orders-invoices"
topics:
  - orders
  - invoices
  - prepaid
---

# Prepaid Invoices

When Invoices are Prepaid, specific fields are used in KSeF. Overview:

| Billit Field (header) | Billit Field Type | KSeF Field | Content Description | Mandatory |
| --- | --- | --- | --- | --- |
| Paid | Boolean | Platnosc/Zaplacono | Prepaid flag |  |
| PaidDate | Date | Platnosc/DataZaplaty | Date of Payment | Yes, if Paid is set to true |

JSON API Partial ExampleXML KSEF Platnosc section

```json
{
    "OrderNumber": "10999999",
    "OrderDate": "2026-04-29",
    "ExpiryDate": "2026-04-29",
    "OrderType": "Invoice",
    "Paid": true,
    "PaidDate": "2026-04-29",
    "OrderDirection": "Income",
}
```

```xml
<Platnosc>
      <Zaplacono>1</Zaplacono>
      <DataZaplaty>2026-04-29</DataZaplaty>
      <TerminPlatnosci>
        <Termin>2026-04-29</Termin>
      </TerminPlatnosci>
      <RachunekBankowy>
        <NrRB>PL04105015751000009999999999</NrRB>
        <SWIFT>INGBPLPW</SWIFT>
	    </RachunekBankowy>
</Platnosc>
```

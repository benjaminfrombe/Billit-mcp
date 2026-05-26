---
title: "Other currency than PLN"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/ksef-other-currency-than-pln"
source_slug: "ksef-other-currency-than-pln"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - other
  - currency
  - than
  - pln
---

## Scenario

When you are sending from a Polish company, you might need to issue the invoice in another currency than PLN. This can apply to:

- invoices to customers outside Poland
- Invoices to customers in Poland

In that case, information must be added:

- The conversion rate PLN to the foreign currency
- VAT amount expressed in 2 currencies:
  - total VAT amount in the currency of the invoice
  - total VAT amount in PLN

## How to do with Billit API

The API content must contain the following elements:

| Description | Billit API Field | KSeF field | Max. Length |
| --- | --- | --- | --- |
| Free description | Comments | Stopka / Informacje / StopkaFaktury | 1000 |
| Foreign Currency Conversion | FXRateToForeign | KursWaluty (line, when invoice), KursWalutyZ (header). In case of Euro : is Euro to PLN, e.g. 4.2175. |  |
| Currency | Currency | Fa / KodWaluty |  |

Example in Json and result in KSeF XML:

POST v1/order International other currencyKSeF XML Header AmountsKSeF XML Line Amounts

```json
{
	"OrderNumber": "4098999",
	"Reference": "45123456789",
	"Currency": "EUR",  //Foreign currency : Euro in stead of PLN
	"OrderDate": "2026-01-23",
	"ExpiryDate": "2026-01-30",
	"OrderType": "Invoice",
	"Comments": "Additional text info on header ",
  "OrderDirection": "Income",
	"FXRateToForeign": 4.2175,  //Conversion rate foreign currency Euro to PLN
  "VentilationCode": "51",  // indicating the VAT codes when lines with 0 %.  See ventilation codes in documentation.
  "Customer": {
        "Name": "TESTCOMPANY BELGIUM ",
        "Addresses": [\
            {\
                "AddressType": "InvoiceAddress",\
                "Name": "TESTCOMPANY POLSKA",\
                "Street": "TESTSTREET",\
                "StreetNumber": "14",\
                "Zipcode": "9000",\
                "City": "GENT",\
                "CountryCode": "BE"\
            }\
        ],
        "VATNumber": "BE0570899999",
        "PartyType": "Customer",
        "VATLiable": true,
        "Language": "EN",
        "VATDeductable": true
},
	"OrderLines": [\
		{\
			"Quantity": 1.0,\
			"UnitPriceExcl": 1.00,\
			"Description": "test",\
			"VATPercentage": 23.00\
		},\
	]
}
```

```xml
<Faktura xmlns:etd="http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://crd.gov.pl/wzor/2025/06/25/13775/">
 <Fa>
   <KodWaluty>EUR</KodWaluty> //foreign currency
   <P_1>2026-02-25</P_1> // invoice date
   <P_2>test8</P_2> //invoice number
   <P_6>2026-02-25</P_6> // date of supply
   <P_13_1>10.00</P_13_1> // taxable base in currency of the invoice
   <P_14_1>2.30</P_14_1> //   VAT amount derived from P13_1 base amount in Euro
   <P_14_1W>9.68</P_14_1W>   //  VAT amount equivalent in PLN (calculated by Billit based on exchange rate)
   <P_15>12.30</P_15> // total amount including VAT (currency of the invoice)
   <KursWalutyZ>4.21000</KursWalutyZ>  // > foreign conversion rate used on header level
 </Fa>
</Faktura>
```

```xml
<FaWiersz>
   <NrWierszaFa>1</NrWierszaFa>
      <P_7>12157_3329_5339_0_6.5e</P_7>
      <P_8A>MTR</P_8A>
      <P_8B>6.50000</P_8B>
      <P_9A>6.24000</P_9A>
      <P_11>40.56</P_11>
      <P_12>oo</P_12>  //Tax rate of the line
      <KursWaluty>4.21000</KursWaluty>  //conversion rate used for foreign currency, put on the line
</FaWiersz>
```

---
title: "Extra KSeF Fields (Advanced)"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/extra-kse-fields-advanced"
source_slug: "extra-kse-fields-advanced"
category: "ksef-poland"
topics:
  - ksef
  - poland
  - extra
  - kse
  - fields
  - advanced
---

## Additional Structured Descriptions - DodatkowyOpis - (Header +Lines)

You may want to add additional descriptions, with a specific structure or signification.

Below the method:

- Is included in Billit Json on header level, stored in KSeF XML on header level
- Refers to :
  - an Invoice line
  - the invoice header
- Multiple occurrencies are possible, even for one invoice line
- Billit Added a Sequence Numbering:
  - e.g. DodatkowyOpis1, DodatkowyOpis2 : this for verification of the coherence by Billit.
  - This sequence number is mandatory. If not used, invoices will go in error.
- Data elements:

| Description | Billit API Header Custom Field | Max length | Mandatory |
| --- | --- | --- | --- |
| Key : the signification of your field | Faktura.FA.DodatkowyOpis1.Klucz | 256 | Mandatory |
| The value / (content of the field) | Faktura.FA.DodatkowyOpis1.Wartosc | 256 | Mandatory |
| Link to invoice line number. When added : linked to a line. When not present : linked to the header | Faktura.FA.DodatkowyOpis2.NrWiersza |  | Optional |

Example:

API JSON With only line based infoAPI JSON linked to line numbers and header

```json
    "CustomFields":
    {
        "Faktura.FA.DodatkowyOpis1.NrWiersza": "2", // Link to invoice line number
        "Faktura.FA.DodatkowyOpis1.Klucz": "Numer awiza",  //key
        "Faktura.FA.DodatkowyOpis1.Wartosc": "SIRL12040454042",  // the value - content for that key
        "Faktura.FA.DodatkowyOpis2.NrWiersza": "2",  // second reference linked to the line
        "Faktura.FA.DodatkowyOpis2.Klucz": "Numer pozycji zamówienia klienta",
        "Faktura.FA.DodatkowyOpis2.Wartosc": "001000",
        "Faktura.FA.DodatkowyOpis3.NrWiersza": "3",
        "Faktura.FA.DodatkowyOpis3.Klucz": "Numer pozycji zamówienia klienta",
        "Faktura.FA.DodatkowyOpis3.Wartosc": "002000"
    },
```

```json
	"CustomFields": {
		"Faktura.FA.DodatkowyOpis1.Klucz": "BDO",
		"Faktura.FA.DodatkowyOpis1.Wartosc": "000040999", //Header value
		"Faktura.FA.DodatkowyOpis2.Klucz": "TEST1",
		"Faktura.FA.DodatkowyOpis2.Wartosc": "0000565", //Header value
    "Faktura.FA.DodatkowyOpis3.Klucz": "TEST2",
		"Faktura.FA.DodatkowyOpis3.Wartosc": "0000569",
		"Faktura.FA.DodatkowyOpis3.NrWiersza": "1",  //For Line 1
    "Faktura.FA.DodatkowyOpis4.Klucz": "TEST3",
		"Faktura.FA.DodatkowyOpis4.Wartosc": "0000560",
		"Faktura.FA.DodatkowyOpis4.NrWiersza": "1", //For Line 1
    "Faktura.FA.DodatkowyOpis5.Klucz": "TEST4",
		"Faktura.FA.DodatkowyOpis5.Wartosc": "0000561",
		"Faktura.FA.DodatkowyOpis5.NrWiersza": "2", //For Line 2
    "Faktura.FA.DodatkowyOpis6.Klucz": "TEST5",
		"Faktura.FA.DodatkowyOpis6.Wartosc": "0000562",
		"Faktura.FA.DodatkowyOpis6.NrWiersza": "2" //For Line 2
    "Faktura.FA.DodatkowyOpis7.Klucz": "Sample Key",
		"Faktura.FA.DodatkowyOpis7.Wartosc": "000050103" //Header value
	},
```

## Alternative Payment Term Information (Header)

The due date is filled in the normal KSeF area : Platnosc / TerminPlatnosci / Termin.

There are legal scenario's where the althernative TermOpis can be used. So on request and via API, this specific information can be included.

Example:

API JSON With only line based infoKSeF XML Result

```json
    "CustomFields":
    {
        "Faktura.Fa.Platnosc.TerminPlatnosci.TerminOpis.Ilosc" : "14", // this is the quantity
        "Faktura.Fa.Platnosc.TerminPlatnosci.TerminOpis.Jednostka" : "day", // this I a unit as free text
        "Faktura.Fa.Platnosc.TerminPlatnosci.TerminOpis.ZdarzeniePoczatkowe" : "Payment deadline description"  // free text, maximum 256 characters

    },
```

```xml
    <Platnosc>
      <TerminPlatnosci>
        <Termin>2026-04-17</Termin>
        <TerminOpis>
          <Ilosc>14</Ilosc>
          <Jednostka>day</Jednostka>
          <ZdarzeniePoczatkowe>Payment deadline description</ZdarzeniePoczatkowe>
        </TerminOpis>
      </TerminPlatnosci>
    </Platnosc>
```

## Add Payment Method (Header)

Payment methods exist in KSeF to compare with Peppol PaymentMeanscode. This appears in the segment Platnosc, field FormaPlatnosci.

Following information:

- Not a mandatory field
- KSeF verification : must be in a list of allowed values

Table with the values:

| Value | Description | Payment Method Description at Billit |
| --- | --- | --- |
| 1 | Gotówka | Cash |
| 2 | Karta | Bancontact |
| 3 | Bon |  |
| 4 | Czek |  |
| 5 | Kredyt | Visa |
| 6 | Przelew | Wired (= bank transfer, is most common value) |
| 7 | Mobilna |  |

Example:

API JSON Example

```json
    "CustomFields":
    {
        "Faktura.Fa.Platnosc.FormaPlatnosci" : "6"
    },
```

## Other Payment Method than value in list of FormaPlatnosci (Header)

When your payment method is another method than the allowed list (values 1 tot 7), then an alternative is available. Method:

- do **not** use custom field : Faktura.Fa.Platnosc.FormaPlatnosci
- 2 other custom fields have to be used.

| Field | Allowed values |
| --- | --- |
| Faktura.Fa.Platnosc.PlatnoscInna | value is 1 if applicable |
| Faktura.Fa.Platnosc.OpisPlatnosci | add free text to describe the alternative payment method |

Example below:

API Json custom field contentKSeF XML Platnosc section

```json
"CustomFields": {
        "Faktura.Fa.Platnosc.PlatnoscInna": "1",
        "Faktura.Fa.Platnosc.OpisPlatnosci": "Free description text"
    }
```

```xml
 <Platnosc>
      <TerminPlatnosci>
        <Termin>2026-04-13</Termin>
      </TerminPlatnosci>
      <PlatnoscInna>1</PlatnoscInna>
      <OpisPlatnosci>Free description text</OpisPlatnosci>
      <RachunekBankowy>
        <NrRB>PL04105015751000002315876322</NrRB>
        <SWIFT>INGBPLPW</SWIFT>
      </RachunekBankowy>
    </Platnosc>
```

## Delivery Address in Transport Segment (Header)

In the transport segment, Billit supports a number of fields via custom Fields on header level.

| Billit | Descripton | Mandatory |
| --- | --- | --- |
| Faktura.Fa.WarunkiTransakcji.Transport.RodzajTransportu | Type of transport : set value from list | yes |
| Faktura.Fa.WarunkiTransakcji.Transport.OpisLadunku | Type of cargo : set value from list | yes |
| Faktura.Fa.WarunkiTransakcji.Transport.JednostkaOpakowania | Packing Unit | no |
| Faktura.Fa.WarunkiTransakcji.Transport.WysylkaDo.KodKraju | Country code | yes |
| Faktura.Fa.WarunkiTransakcji.Transport.WysylkaDo.AdresL1 | Street and street number | yes |
| Faktura .Fa.WarunkiTransakcji.Transport.WysylkaDo.AdresL2" | Zip and City | yes |

Example below.

API JSON KSeF XML Result

```json
    "CustomFields":
    {
               "Faktura.Fa.WarunkiTransakcji.Transport.RodzajTransportu" : "3", // TransportType 3: Road transport (most common type).  This is from a list (value 1 to 8)
        "Faktura.Fa.WarunkiTransakcji.Transport.OpisLadunku" : "13", // Cargo type 13: Pallet.  This is from a list (value 1 to 20)
        "Faktura.Fa.WarunkiTransakcji.Transport.JednostkaOpakowania" : "1 cardboard box/40 pieces", // Packing unit
        "Faktura.Fa.WarunkiTransakcji.Transport.WysylkaDo.KodKraju" : "PL",  //Country
        "Faktura.Fa.WarunkiTransakcji.Transport.WysylkaDo.AdresL1" : "ul. Sadowa 1 lok. 3",  //Street and number
        "Faktura .Fa.WarunkiTransakcji.Transport.WysylkaDo.AdresL2" : "00-002 Kraków"  // Zip and City
    },
```

```xml
 <WarunkiTransakcji>
      <Zamowienia />
      <Transport>
        <RodzajTransportu>3</RodzajTransportu>
        <OpisLadunku>13</OpisLadunku>
        <WysylkaDo>
          <KodKraju>PL</KodKraju>
          <AdresL1>ul. Sadowa 1 lok. 3</AdresL1>
        </WysylkaDo>
      </Transport>
    </WarunkiTransakcji>
```

List of other values for TransportTypes: See KSeF documentation.

## Incoterms / Delivery in Warunkitransakcji

There is a specific header field in KSeF, Warunkitransakcji/MiejsceDostawy, where Incoterms or other delivery information can be included.

| Billit | Description | Max. Length | Mandatory |
| --- | --- | --- | --- |
| Faktura.Fa.WarunkiTransakcji.WarunkiDostawy | Header field for Incoterms, or other delivery information | 256 | No |

Example:

API JSON Example

```json
     "CustomFields": {
        "Faktura.Fa.WarunkiTransakcji.WarunkiDostawy" : "Desciption to be added (Incoterms)"
    }
```

## Add in Rejestry BDO and REGON References

In Rejestry following information elements can be used on header level

| Reference | What |
| --- | --- |
| Rejestry : BDO | Waste Database Number |
| Rejestry : REGON | National Business Registry Number |

Behaviour:

- header fields
- optional
- one or multiple occurencies

API Json Example 1 valueAPI Json Example 2 valueq

```json
	"CustomFields": {
        "Faktura.Stopka.Rejestry.BDO" : "000040473", // BDO
        "Faktura.Stopka.Rejestry.REGON" : "000099999" // this I a unit as free text
	},
```

```json
	"CustomFields": {
        "Faktura.Stopka.Rejestry1.BDO" : "000040473",
        "Faktura.Stopka.Rejestry1.REGON" : "000099999"
        "Faktura.Stopka.Rejestry2.BDO" : "000040473",
        "Faktura.Stopka.Rejestry2.REGON" : "000099999"
	},
```

## P\_18A in the Adnotacje Element (Annotations)

The P\_18A header field in Adnotacje (Annotations) needs to be filled when split payment is cocerned under following conditions.

In the case of an invoice bearing the note "split payment mechanism", where the total amount due exceeds the amount of PLN 15,000 or its equivalent expressed in a foreign currency, covering the supply of goods or the provision of services listed in Annex 15 to the Act made to the taxpayer, whereby the rules for converting amounts expressed in foreign currency into PLN shall be applied to determine the tax base - the value "1" should be entered; otherwise, the value "2" should be entered.

You can set the value of P\_18A via a specific field. See example below.

P\_18A

```text
    "CustomFields": {
        "Faktura.Fa.Adnotacje.P_18A": "1",
    },
```

## Podmiot 2 : Set values for JST/GV (Header)

In certain cases, depending on roles in Podmiot3, the values of the Podmiot 2 fields JST and GV need to be set to the correct value. Podmiot 2 refers to the customer section.

This can be set via custom fields. The allowed values for JST and GV are 1 or 2.

Below an example.

JST/GV

```text
  CustomFields: {
 "Faktura.Podmiot2.JST": "1",
 "Faktura.Podmiot2.GV": "1"
}
```

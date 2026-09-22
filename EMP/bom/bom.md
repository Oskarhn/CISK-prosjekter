# Komponentliste med detaljerte forklaringer

## Hovedkondensator C1
- **Verdi:** 1000 µF, 450 V
- **Type:** Elektrolytisk, fotoflash (lav ESR, høy pulsstrøm)
- **Delenummer:** Nichicon LLS2W102MELC (Farnell 184-8404) eller Kemet ALC10A102EL450 (RS 136-6285)
- **Hvorfor:** Må lagre 80 J og tåle utladningsstrømmer på >10 kA. Fotoflash-kondensatorer er spesielt konstruert for slike pulsbelastninger. De har lav ekvivalent seriemotstand (ESR) og høy pålitelighet under gjentatte høye strømtopper.

## MOSFET Q1
- **Verdi:** IRF840 (500 V, 8 A, N-kanal)
- **Delenummer:** Farnell 146-3412, RS 700-4322
- **Hvorfor:** Brukes i flyback-omformeren. Tåler høye spenningstopper under avslag. Den har en drain-source spenning på 500 V, noe som gir god margin for vår applikasjon.

## Diode D1
- **Verdi:** UF4007 (1000 V, 1 A, rask gjenoppretting)
- **Delenummer:** Farnell 146-7590, RS 700-4287
- **Hvorfor:** Likeretter høyspentpulsene fra transformatoren. Rask diode er nødvendig for å unngå tap i flyback-kretsen. UF4007 har en reverse recovery time på 75 ns, som er tilstrekkelig for vår svitsjefrekvens.

## Zenerdiode D2
- **Verdi:** 15 V, 0.5 W
- **Delenummer:** Farnell 170-0750, RS 544-3245
- **Hvorfor:** Beskytter MOSFET-gate mot overspenning fra tilbakekoblingsviklingen. Zeneren klemmer gate-spenningen til maksimalt 15 V, noe som er innenfor MOSFET-ens spesifikasjoner (typisk ±20 V).

## LED D3
- **Verdi:** Grønn, 5 mm, høy lysstyrke
- **Delenummer:** Farnell 102-4030, RS 228-5608
- **Hvorfor:** Indikerer at kondensatoren er ladet til >200 V. Grønn er valgt for god synlighet. LED-en begynner å lyse svakt ved ca. 200 V og er fullt lys ved 400 V.

## Diode D4 (gatebeskyttelse)
- **Verdi:** 1N4148
- **Delenummer:** Farnell 146-7600, RS 700-4290
- **Hvorfor:** Plasseres i serie med zener D2 (katode mot gate) for å hindre negativ gatespenning. Dette beskytter MOSFET-en mot potensiell skade og reduserer støy.

## Motstand R1
- **Verdi:** 1 kΩ, 0.25 W
- **Delenummer:** Farnell 933-1520, RS 707-7694
- **Hvorfor:** Begrenser strømmen fra tilbakekoblingsviklingen til gate, og demper oscillasjoner. Sammen med zeneren og D4 gir den en robust gate-driver.

## Motstand R11 (utladning)
- **Verdi:** 1 kΩ, 50 W (trådviklet)
- **Delenummer:** Farnell 247-8500, RS 160-2160
- **Hvorfor:** Gir en tidskonstant på 1 sekund med 1000 µF. Hold knappen inne i minst 5 sekunder for å lade ut til <10 V. 50 W er nødvendig for å håndtere pulsenergien trygt.

## Motstand R12 (LED)
- **Verdi:** 220 kΩ, 1 W (metallfilm)
- **Delenummer:** Farnell 933-1560, RS 707-7740
- **Hvorfor:** Tåler 0.72 W kontinuerlig ved 400 V. En 1 W motstand gir god margin.

## Brytere S1, S2
- **Type:** Momentan trykknapp, SPST
- **Delenummer:** Farnell 108-2240, RS 734-7221
- **Hvorfor:** S1 brukes til lading (må holdes inne), S2 til utladning. Momentan funksjon sikrer at ladingen stopper når knappen slippes.

## Bryter S3
- **Type:** Vippebryter, SPST, panelmontering
- **Delenummer:** Farnell 108-2260, RS 734-7243
- **Hvorfor:** Hovedstrømbryter for å koble fra batteriet helt. Gir en ekstra sikkerhetsbarriere.

## Sikring F1
- **Verdi:** 2 A, 250 V, 5×20 mm
- **Delenummer:** Farnell 123-4567, RS 700-1234
- **Hvorfor:** Beskytter batterikretsen mot kortslutning. Plasseres i serie med batteriets plussledning.

## Transformator T1
- **Kjerne:** E20/10/6 ferritt (N27), med spoleholder
- **Tråd:** 0.5 mm (primær), 0.1 mm (sekundær), 0.2 mm (tilbakekobling)
- **Hvorfor:** Hjemmelaget for å matche våre spesifikasjoner. Se byggeveiledning for detaljer om vikling. Viktig: Design for å unngå metning; anbefalt luftgap 0.1 mm, primærinduktans ~50 µH.

## Gnistgap G1
- **Materiale:** 1.6 mm wolframelektroder (TIG-sveise-elektroder)
- **Hvorfor:** Wolfram tåler ekstrem varme og erosjon fra lysbuen. Elektrodene kan enkelt formes og slipes for å oppnå ønsket gap-avstand.

## Spole L1
- **Tråd:** 10 AWG (2.588 mm) emaljert kobbertråd, ca. 2 meter
- **Hvorfor:** Tykkt nok til å føre 9 kA uten å smelte, og lav motstand. Emaljert tråd forhindrer kortslutning mellom vindingene.

## Batteriklemmer
- **Type:** 9V snap-kontakter, 6 stk.
- **Delenummer:** Farnell 165-0672, RS 455-8300
- **Hvorfor:** For å koble 6 stk. 9V-batterier i serie. Merk: Alkaliske batterier har høy indre motstand; for bedre ytelse anbefales en 6S LiPo-pakke (22.2 V) med tilpasset flyback-design.

## Diverse
- Loddetinn, krympestrømpe, isolasjonstape, skruer, avstandsstykker, ledninger (2.5 mm² for høystrømsforbindelser).

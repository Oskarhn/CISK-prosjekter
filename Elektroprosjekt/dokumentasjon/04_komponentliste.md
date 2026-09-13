# 04 — Komponentliste (BOM)

Full komponentliste med nøyaktige verdier, varenummer og hvorfor hver del er valgt.
Fylt utgave av kursens bestillingsmal: **`../bestilling/bestilling_utfylt.xlsx`**.

8 ulike komponenttyper (kravet er 5–10): **motstand, kondensator, spole, diode,
MOSFET, IC, bryter, kontakter** (testpunkter/terminaler/headers).

## 4.1 Kraftdel

| Ref | Del | Verdi/spesifikasjon | Varenummer | Antall | Hvorfor |
|---|---|---|---|---|---|
| C1, C2 | Lav-ESR elektrokondensator | 2 × 470 µF / 50 V (parallel: 940 µF, ESR ≈ 16 mΩ) | RS 7083945 (Panasonic EEUFR1H471) | 2 | Energibanken. 24 V lagrer 270,7 mJ. 50 V-rating gir 2× margin. Lav-ESR-serie holder ESR lav nok til ζ ≈ 0,32 |
| COIL_T | Senderpole | 15 vikt, r = 15 mm, 1,0 mm emaljert kobber, L = 6,69 µH, R = 31 mΩ | RS 7790735 (ledning, 1,0 mm OD, 0,82 mm², 56 m) | 1 | Feltet lages her: B_center = 104 mT ved 186,5 A. L satt av viklingstall (se `05_spoler.md`) |
| PU | Mottakspole | 15 vikt, Ø20 mm, 0,5 mm emaljert kobber, L ≈ 3,6 µH | RS 0534116 (ledning, 0,5 mm OD, 0,2 mm², 25 m) | 1 | Målepole i boret: M = 2,66 µH gir 9,5 V oppgang + 41,9 V spiss til scope |
| Q1 | N-kanal kraft-MOSFET | IRF3707: 30 V, 62 A, Rds(on) 1,25 mΩ @ 10 V, TO-220AB | RS 8274057 | 1 | Avskjører 186,5 A-pulsen. Rds(on) = 1,25 mΩ er 2,3 % av løkkmotstanden. Vds: maks ≈ 17 V i normal drift (1,76× margin mot 30 V); D1 klamer drain ved avskjering |
| D1 | Ultrahastig farihjuldiode | MUR1560: 600 V, 15 A, TO-220AC | Farnell dp/4245037 | 1 | Tvinger polestrømmen i farihjulløkka ved avskjering; holder drain-spenning under ~17 V og begrenser di/dt til 15,8 MA/s. 600 V er overkill (villig: ingen spiss kan ødelegge den) |
| R_FW | Farihjul-snubber | 0,47 Ω / 5 W viklet | RS 0732294 (TE FWFU5WR47J) | 1 | Setter farihjul-τ = 11,9 µs og maks di/dt. Øre for 186,5 A i 12 µs (0,16 mJ per puls) |
| R_SHUNT | Strømsens-shunt | 0,01 Ω / 5 W / 1 % viklet | RS 1249291 (Arcol Ohmite 15FR010E) | 1 | Scope-måling av senderstrøm: 1,87 V ved topp. 5 W tåler topp-P ≈ 3,5 kW i ~0,5 ms |
| R_CHG | Ladingsmotstand | 100 Ω / 2 W metal film | RS 6835685 (Vishay PR02000201000JA100) | 1 | Lader banken fra forsyningen på ~0,5 s med 5,8 W (tåler 2 W gjennomsnitt; pulsbelastning er kort) |
| R_BLEED | Utladningsmotstand | 10 kΩ / 0,4 W / 1 % | RS 1997793 (Yageo MF0204FTE52-10K) | 1 | Utlader banken til < 1 V på ~10 s etter en puls (sikkerhet + gjentagbar preslading) |
| D4 | Forsynings-klamp | SMBJ24A TVS: 24 V, 600 W | Farnell dp/1827614 (Littelfuse) | 1 | Klammer forsyningstransienter til ~38 V (under 50 V kond-rating) |
| TB1 | Terminalblokk | 2-polig, 5,08 mm, PCB | RS 1468345 (RS PRO CTB0509) | 1 | Forsyning +24 V / − |

## 4.2 Styredel (555-monostabil)

| Ref | Del | Verdi/spesifikasjon | Varenummer | Antall | Hvorfor |
|---|---|---|---|---|---|
| IC1 | Timer | NE555P, DIP-8 | Farnell dp/3006909 (TI) | 1 | Monostabil: T = 1,1·R·C = 106,7 µs. Avskjærer MOSFET-en i toppstrømmen (t_pk = 104,2 µs) |
| R1 | Timingmotstand | 9,70 kΩ / 1 % / 0805 | Vishay CRCW08059K70FKEA (bekreft i butikk) | 1 | Med C_TIM = 10 nF gir T = 106,7 µs. 1 % + C0G holder pulsen ±1,5 % |
| C_TIM | Timingkondensator | 10 nF / 50 V / C0G / 0805 | Farnell dp/4540277 (MC0805N103J500CT) | 1 | C0G (NP0): temperaturdrift ±10 ppm/°C → pulsbredde stabil |
| C3 | Triggerkondensator | 10 nF / 50 V / C0G / 0805 | Farnell dp/4540277 | 1 | Serieresistiv trigger: én puls per trykk, knappebounce immunn |
| R2 | Trigger-resistor | 10 kΩ / 0805 | (søk 10 kΩ 0805) | 1 | Holder triggerpinen over ⅔VCC; C3+R2 former differensiator |
| R4 | Gate pull-down | 10 kΩ / 0805 | (søk 10 kΩ 0805) | 1 | Sørger for at MOSFET-en er AV når 555-ut er lav |
| R3 | Gate-styring | 10 Ω / 0,5 W / 0805 | (søk 10 Ω 0,5 W 0805) | 1 | Lader gatekapasiteten (~1,5 nC) på < 200 ns; holder gate-løkken kort |
| R9 | Skinnemotstand | 820 Ω / 0805 | (søk 820 Ω 0805) | 1 | Deler 24 V → ~13 V til D2-regulatoren (0,17 W) |
| D2 | 555-regulator | 1N4742A: 12 V / 1,3 W Zener | Farnell dp/1612366 (Vishay) | 1 | 12 V-skinn for 555-en (NE555 er god til 16 V, 12 V gir margin og jevnere puls) |
| D3 | Gate-klamp | 1N4744A: 15 V / 1,3 W Zener | Farnell dp/1612368 (Vishay) | 1 | Klammer gate-spenning til 15 V (Vgs-max = 20 V; 27 % margin) |
| C4 | CTRL-bypass | 100 nF / 50 V / X7R / 0805 | (søk 100 nF 50 V X7R 0805) | 1 | 555-anbefalt CTRL-bypass; holder 1/3VCC-trerskel stabil |
| C5 | 555-bulk | 10 µF / 25 V / 0805 | Farnell dp/3764157 (0805X106M250CP) | 1 | 555-anbefalt VCC-bulk (demper pulskanten) |
| S1 | Avfyringsknapp | 6 × 6 mm taktbryter, 4 ben | (søk 6 × 6 mm tact switch) | 1 | Trykk → én puls (C3 blokkerer bounce) |

## 4.3 Kontakter og mekanikk

| Ref | Del | Spesifikasjon | Varenummer | Antall | Hvorfor |
|---|---|---|---|---|---|
| TP1–TP6 | Testpunkter | 6-polig 2,54 mm header | RS 2518137 | 1 | Scope-tilgang til A, E, shunt-par, gate, 555-ut |
| TP7/TP8 | Mottak UT | 2-polig 2,54 mm header | RS 2272142 | 1 | Mottakspulsen til scope CH2 |
| Spoletube | Spoleform | 31 mm OD plasttube, ~20 mm | RS 177-1103 | 1 | Holder de 15 viklingene tett og samentris (L-stabil) |
| Fot | Fotskruer | M3 × 6 mm nylon, 4 stk | RS 190-4271 | 4 | Løfter spolen opp fra platen slik at mottaket passer i boret |
| PCB | Plat | 80 × 80 mm, 2-lags, 35 µm Cu, 1,6 mm FR-4, matt tenn | RS PCB-service | 5 | Helt designet (se `07_pcb_layout.md`). 5 stk = 1 oppbygging + reserve |

## 4.4 Budsjett (se `../bestilling/bestilling_utfylt.xlsx`)

| Post | NOK (ex MVA) |
|---|---|
| Kraftdel (kondensatorer, poler, MOSFET, dioder, shunt, R_FW, R_CHG, R_BLEED, TVS) | ≈ 207 |
| Styredel (555 + passiv + knapp) | ≈ 90 |
| Kontakter + mekanikk | ≈ 32 |
| PCB (5 stk) | 250 |
| **Sum ex MVA** | **≈ 580** |
| **Totalsum med 25 % MVA** | **≈ 725** |

Prisene er estimater fra butikkene 09.09.2026 (sjekk i varekurven før bestilling).

## 4.5 Varetilgjengelighet og fallbacker

Varenumrene i denne filen er verifisert mot RS (no.rs-online.com) og Farnell
(no.farnell.com) 09.09.2026. Oppgaven tillater like deler med same spesifikasjon, så ethvert
lagerdelt som oppfyller spesifikasjonen er gyldig:

* **R_SHUNT** (0,01 Ω / 5 W): hvis tomt: to × 0,02 Ω / 5 W i serie (holder 1 % tolerance).
* **MUR1560**: MUR1520 (60 V / 15 A) er like god (drain er klamped to ~17 V).
* **IRF3707**: ethvert 30–60 V N-kanal MOSFET with Rds(on) ≤ 2 mΩ (TO-220) fungerer; ved
  48 V-skaleringstesten i `09_eksperimenter.md` velg en 60 V+ del (drain spiss stiger til ~33 V).
* **C0G 10 nF**: ethvert NP0 10 nF / 50 V / 0805 (f.eks. KEMET C0805C103...).
* **0,47 Ω 5 W wirewound**: 0,5 Ω / 5 W viklet motstand er innenfor design toleransen.
* **0805 passives** (R1–R4, R9, C4, C5): vanlige varer, ethvert merke, rett verdi.

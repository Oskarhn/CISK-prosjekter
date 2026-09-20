# 04 — Komponentliste (BOM)

**Antall komponenttyper brukt: 8** (innenfor kursets grense på 5–10): motstand,
kondensator, spole (håndviklet), diode, MOSFET, IC, bryter, kontakt.

Leverandører: **no.rs-online.com** og **no.farnell.com** (per kursets krav). Delnumrene
under er katalogvarene fra disse leverandørene; bekreft lagerstatus og pris før
bestilling — der et delnummer er merket `(search)`, velg en
vilkårlig vare som møter spesifikasjonen (kurset aksepterer lignende komponenter med
samme spesifikasjoner). Priser er NOK-estimater eks. MVA for bestillingsarket.

En utfylt versjon av kursets bestillingsmal er: **`Bestillingprosjekt_utfylt.xlsx`**.

## 4.1 Effekt-/pulsvei

| Ref | Verdi | Antall | Spesifikasjon (det som betyr noe) | Foreslått del (leverandør) | Pris ≈ NOK | Hvorfor den trengs |
|---|---|---|---|---|---|---|
| C1, C2 | 470 µF / 50 V | 2 | Lav-ESR radial elektrolytt, ESR ≤ 25 mΩ @ 100 kHz, 105 °C (f.eks. Panasonic FR/TE, KEMET, Nichicon PW) | RS: lav-ESR 470 µF 50 V radial (søk "470 µF 50 V low ESR") | 18 stk | Energilager: 940 µF × 24 V = 270,7 mJ. Parallell halverer ESR og strøm per kondensator. |
| R_CHG | 100 Ω / 2 W | 1 | Metallfilm, 1 %, gjennomhull | Farnell: 100 R 2 W metallfilm 1 % (søk "100R 2W") | 7 | Begrenser ladestrømmen til 240 mA (~0,5 s full lading). |
| R_BLEED | 10 kΩ / ¼ W | 1 | Vilkårlig film, gjennomhull | (søk "10k 1/4W") | 2 | Sikkerhetsutlading: 24 V → 2 V på ~4 s. |
| COIL_T | 15 vikt, r = 15 mm | 1 | 1,0 mm (17 AWG) isolert Cu, tettviklet på 29–31 mm OD **ikke-metallisk** rør, l ≈ 15,3 mm | Magnettråd 1,0 mm (RS: 17 AWG Cu isolert) + 31 mm OD plast-/PVC-rør | 45 + 12 | EMP-strålingselementet. L ≈ 6,7 µH, R ≈ 31 mΩ, B_senter ≈ 104 mT @ 186,5 A. |
| D1 | MUR1560 | 1 | Ultrahurtig likeretter, 15 A, ≥ 600 V (alt: MUR1520 60 V er tilstrekkelig) | Farnell: 1269600 (MUR1560) eller søk "MUR1560" | 12 | Flyback-/frihjulsdiode over spolen; setter frihjul-di/dt together with R_FW (gives ≈ 110 V spike on the drain). |
| R_FW | 0,5 Ω / 5 W | 1 | Trådviklet, 1 % | RS: 0,47 R 5 W trådviklet (søk "0.5R 5W wirewound") | 12 | Frihjulsbrems: τ_fw = 11,9 µs → 15,8 MA/s spiss. 101,7 mJ/puls. |
| MOSFET | IRF3707 | 1 | N-kanal effekt-MOSFET, 30 V, R_DS(on) ≤ 1,6 mΩ @ V_GS = 10 V, pulset I_D ≥ 250 A, TO-220AB (avskjeringsspiss ≈ 110 V — overskrir ratingen; se 03_beregninger.md) | Farnell: IRF3707 (søk "IRF3707"); alt: IRF3710 / IRF3716 | 22 | Bryteren. 1,25 mΩ holder ζ = 0,321; 30 V rating overskres by the ≈ 110 V turn-off spike. |
| R_SHUNT | 0,01 Ω / 5 W | 1 | Trådviklet shunt 10 mΩ (alt: 2 × 0,02 Ω i serie → I_pk ≈ 175 A) | RS: "10 mΩ shunt 5 W" (søk "0.01R 5W") | 20 | Strømsensor: 1,87 V ved 186,5 A for scopet. Ikke i strømbanen under frihjul (rent signal). |
| TB1 | 5,08 mm 2-pin | 1 | PCB-terminalblokk, 24 V-klasse | RS: 5,08 mm 2-pin PCB-terminal (søk) | 6 | Forsyningsinngang. |
| D4 | SMBJ24A | 1 | Unidireksjonell TVS, 24 V (alt: SMAJ24A) | RS: SMBJ24A (søk "SMBJ24A") | 9 | Klamper transienter på forsyningsinngangen ved ~38 V. |

## 4.2 Styringsvei (555 + gate-driv)

| Ref | Verdi | Antall | Spesifikasjon | Foreslått del | Pris ≈ NOK | Hvorfor den trengs |
|---|---|---|---|---|---|---|
| IC1 | NE555P | 1 | 555-timer, DIP-8 | Farnell: 1065735 (NE555P) / RS: 188-9643 | 13 | Monostabil: én 106,7 µs puls per knappetrykk = avslåing ved strømtoppen. |
| R1 | 9,70 kΩ 1 % | 1 | Metallfilm, 0805 | Farnell 0805 1 %-serie (søk "9k7 1% 0805") | 1,5 | T = 1,1RC = 106,7 µs ≈ t_pk. |
| C_TIM | 10 nF / 50 V | 1 | C0G/NP0, 0805 | Farnell: 1095994 (10 nF 50 V C0G 0805) eller søk | 2 | Timingkondensator (stabil med C0G). |
| C3 | 10 nF / 50 V | 1 | C0G/NP0, 0805 | samme som over | 2 | Triggerdifferensiator → nøyaktig én puls per trykk, prellsikker. |
| R2 | 10 kΩ | 1 | Film, 0805 | Farnell 0805-serie (søk "10k 0805") | 1,5 | Trigger-oppdrag. |
| R4 | 10 kΩ | 1 | Film, 0805 | samme som over | 1,5 | Gate-nedtrekk (garantert av). |
| R3 | 10 Ω / ½ W | 1 | Film, 0805 | (søk "10R 0805 1/2W") | 1,5 | Gate-driv; demper gate-ringing. |
| D3 | 1N4744A | 1 | Zener 15 V, 1 W | Farnell: 1N4744A (søk) | 6 | Gate-klamp (V_GS ≤ 15 V < 30 V-rating). |
| R9 | 820 Ω | 1 | Film, 0805 | (søk "820R 0805") | 1,5 | Setter 12 V-skinnestrømmen (~14,6 mA). |
| D2 | 1N4742A | 1 | Zener 12 V, 1 W | Farnell: 1N4742A (søk) | 6 | Spenningsregulator for 555 (NE555 maks 15,5 V — direkte 24 V ville ødelagt den). |
| C4 | 100 nF / 50 V | 1 | X7R, 0805 | Farnell 0805 X7R (søk "100n 50V 0805") | 2 | Bypass på 555-kontrollpinnen. |
| C5 | 10 µF / 25 V | 1 | X7R, 0805 | (søk "10u 25V 0805") | 2,5 | 555 bulkkondensator (gate-driv-transient). |
| S1 | 6 × 6 mm | 1 | Trykknapp, 1 A | RS: 6 mm trykknapp (søk) | 3 | Avfyringsknapp. |

## 4.3 Måling

| Ref | Verdi | Antall | Spesifikasjon | Foreslått del | Pris ≈ NOK | Hvorfor den trengs |
|---|---|---|---|---|---|---|
| PU | 15 vikt, r = 10 mm | 1 | 0,5 mm (32 AWG) isolert Cu, tettviklet på 20 mm OD ikke-metallisk former | Magnettråd 0,5 mm (RS: 32 AWG Cu isolert) | 40 | Feltvitne for scopet: M = 2,66 µH → 9,5 V stigning + 41,9 V spiss i senter. |
| HDR1 | 2,54 mm, 2-pin | 1 | Pin-header (mottaksutgang) | RS: 2,54 mm header (søk) | 4 | Mottak → scope BNC/klips. |
| HDR2 | 2,54 mm, 6-pin | 1 | Pin-header (TP1–TP6) | RS: 2,54 mm header (søk) | 4 | Testpunkter: kond+, drain, shuntpar, gate, 555-ut. |

## 4.4 Mekanisk / PCB

| Del | Antall | Spesifikasjon | Pris ≈ NOK | Notater |
|---|---|---|---|---|
| PCB 80 × 80 mm, 2-lags, 35 µm Cu | 1 (eller 5) | 1,6 mm FR-4, matt tinn eller ENIG | 250 (5 stk) | Bestilles fra et PCB-verksted; layout i `07_pcb_layout.md`. |
| Avstandsstykker M3 × 6 mm, nylon | 4 | | 6 | Holder spolerøret over platen. |
| Spolerør (COIL_T) | 1 | 31 mm OD × ~20 mm, PVC/polyamid/PLA (ikke-ledende, ikke-magnetisk) | 12 | Kuttes fra rør eller 3D-printes. Metall = kortsluttet vikling (ikke bruk kobber/aluminium). |
| Mottaksformer | 1 | 20 mm OD × ~18 mm rør | 8 | Eller vikle rundt en 20 mm dor og skyv røret på. |
| Loddetinn, flussmiddel, avbitertang | — | | — | Standard labutstyr. |

**Bestilles ikke (eksternt, labutstyr):** 24 V / 3 A benkforsyning (en hvilken som helst
0–30 V DC-forsyning), oscilloskop ≥ 100 MHz med ≥ 2 kanaler (kursets labutstyr).

## 4.5 Budsjettsammendrag (se bestillingsarket `Bestillingprosjekt_utfylt.xlsx`)

Bestillingsarket summerer `max(antall, min. kjøp) × pr.stk` per rad (Farnell 0805-linjer
kjøpes i multipler av 5, som i maleksempelet):

| Gruppe | NOK (eks. MVA) |
|---|---|
| Motstander (9) | 69,0 |
| Kondensatorer (6) | 68,5 |
| Dioder (4) | 33,0 |
| MOSFET + IC | 35,0 |
| Bryter + kontakter (4) | 17,0 |
| Magnettråd (2) | 85,0 |
| PCB + rør + avstandsstykker | 268,0 |
| **Delsum** | **575,5** |
| +25 % MVA | 143,9 |
| **Totalt ≈ 719 NOK** | |

## 4.6 Delvalg og alternativer

Hver spesifikasjon er eksakt, så enhver del på lager som møter den er akseptabel per
oppgaven ("lignende komponenter med samme spesifikasjoner").

De tre mest risikable radene (tilgjengelighet): 10 mΩ-shunten (fallback: 2 × 0,02 Ω 5 W i
serie), lav-ESR 470 µF/50 V-kondensatoren (fallback: en hvilken som helst 470 µF/50 V med
ESR ≤ 25 mΩ; en standard 470 µF/50 V med 50 mΩ ESR senker I_pk til ≈ 150 A — fortsatt
akseptabelt), og 0,5 Ω/5 W trådviklet motstand (fallback: 0,47 Ω/5 W, neglisjerbar
endring).

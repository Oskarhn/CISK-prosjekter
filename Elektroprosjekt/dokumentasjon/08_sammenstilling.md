# 08 — Oppbygging og test (steg for steg)

Arbeidsrekkefølge: **viklet spole → benkeprototype → (Proteus-sim) → PCB → lodd → feilsøk
→ endelig måling.** Hvert steg har et godkjenningskriterium før du går videre.

## Fase 0 — Før du bygger

* [ ] Deler bestilt (`../bestilling/bestilling_utfylt.xlsx`), sjekket mot `04_komponentliste.md`.
* [ ] Scope ≥ 100 MHz, 2+ kanaler; 24 V / 3 A labforsyning; DMM; LCM-meter (eller 10 Ω +
      0,1 Ω shunt for tidskonstant-metoden).
* [ ] `../beregninger/beregninger.py` kjørt → forventede tall printet (I_pk ≈ 187 A, t_pk ≈ 104 µs,
      B ≈ 104 mT, mottaksspiss ≈ 41,9 V).
* [ ] Valgfritt, men anbefalt: bygg kretsen i **Proteus** først (`10_proteus.md`) — fang
  koblingsfeil før loding.

## Fase 1 — Vikle og mål polene

1. Vikle COIL_T: 15 vikt, 1,0 mm ledning, Ø30 mm, på 29 mm ID-tube (la 70 mm tupper).
2. Vikle PU: 15 vikt, 0,5 mm ledning, Ø20 mm, på 18–20 mm former.
3. Mål COIL_T på LCM-meter på 1 kHz → **forvent 6,5–7,2 µH, ESR ≈ 31 mΩ**
   (`05_spoler.md` 5.2). Utenfor området: omvikle før noe annet.
4. Mål PU-motstand (bør være ~80 mΩ) og COIL_T-motstand (~31 mΩ, DMM 2-tråd OK for denne
   verdien).

## Fase 2 — Benkeprototype (leddbrett/perforert brett, 5 V først, deretter 24 V)

Kjør først bare styringsveien (555, R1/C_TIM, R2/C3/S1, R9/D2 fra en 12 V forsyning,
C4/C5, R3/R4/D3 til en MOSFET-gate koblet til en 100 Ω dummy til jord):

1. Trykk S1 → scope CH på 555 pin 3: **forvent en 106,7 µs høy puls** på ~10,5 V.
   For kort/lang: sjekk R1 (9,70 kΩ) og C_TIM (10 nF). Kontinuerlig: trigger festet lav
   — sjekk R2 (10 kΩ) og at C3 er den *serie* differensiatoren.
2. Legg på MOSFET-en med en 1 kΩ motstand som "spole" (dummy-last): gate 0→10,5 V,
   drain ser 10,5 V→0 overgang innen ~1 µs.
3. Nå, tenn pulseveien fra 24 V-forsyningen **med den ekte spolen** (fremdeles på benket):
   trykk S1 → scope:
   * CH1 på shunten (kople inn en 0,01 Ω eller 0,1 Ω shunt i kond−-tuppen): **1,87 V ramp
     til topp ved ~104 µs, deretter raskt fall når frihjul overtar.**
   * CH på spoleende (drain): holder seg nær 0 V under utladningen, hopper til ~110 V
     ved avskjering (spiss av R_FW-droppen), **ingen megavolt-nivå pegg** (D1 + R_FW holder den ned).
   * CH på kond+: 24 → 10 V.
   * CH på mottaket: 9,5 V oppgang + 41,9 V pegg.
4. **Godkjenningskriterium:** alle fire bølgeformer stemmer med `02_kretsskjema.md` 2.5 og
   `03_beregninger.md` innen ~15 %.

## Fase 3 — Proteus-simulering (kurskrav)

Bygg samme netlist i Proteus og kjør en transient-simulering (`10_proteus.md`).
Godkjenningskriterium: simulert I_pk og t_pk innen 20 % av håndberegnet 187 A / 104 µs
(modellforskjeller er forventet; se 10.4).

## Fase 4 — PCB-fabrikkasjon

1. Layout etter `07_pcb_layout.md` (eller kurs' Proteus AURORA PCB-verktøy).
2. Bestilling: 80 × 80 mm, 2-lags, 35 µm, 1,6 mm, matt tinn. (5 stk ≈ 250 NOK; 1 stk hvis
   budsjettbegrenset — bestill minst 2: en til oppbygging, en reserverte).
3. Mens du venter: kjøp og skjær spoletube, skjær søkk, forbered mottaksformer.

## Fase 5 — Lodding (PCB)

Komponentrekkefølge (enklest → vanskeligst):
1. Test-headers + 5,08 terminal + takt-knapp (gjennomhull, lett).
2. 555 DIP-8 (sjekk pin 1 orientering; pin 4 = pin 8 = VCC).
3. Resistorer/kondensatorer 0805 (eller gjennomhull-ekvivalenter om du byttet).
4. D4 TVS, D2/D3 Zenerer, D1 MUR1560 (polaritet!).
5. MOSFET (TO-220; fange → jordpad).
6. Shunt (5 W viklet — ikke overopphet loddeleddene).
7. **Spoleledere → A og E pads** (viktigste ledd: 187 A).
8. Kondensatorbank (470 µF × 2, + mot A).
9. Mottaksspole + tupper → TP7/TP8; fikser mottaket i spolemidten.

**Før-tenning sjekkliste:**
* [ ] DMM kontinuitet: A–E gjennom spole = ~31 mΩ; ingen kort A–F eller E–F.
* [ ] DMM diode-sjekk: D1 (anode E), D2 (kathode G), D3 (kathode gate), D4 (kathode +).
* [ ] 555 pin 1 = jord, pin 8 = 12 V (etter R9/D2 rail tennes, G = 12,0 V).
* [ ] Kondensatorpolaritet: + ved A.
* [ ] Ingen loddebroer på 0805 (inspekter med telefonkamera zoom).

## Fase 6 — Feilsøk (symptom → årsak)

| Symptom | Sannsynlig årsak | Rettelse |
|---|---|---|
| Ingen puls i det hele tatt | 555 uforsynt / pin 4 ikke bundet til VCC / kortsluttet trigger | Sjekk G = 12 V; R2 til stede |
| 555-ut kontinuerlig høy | Trigger pin festet < ⅓VCC (C3 feil verdi/plassering, R2 mangler) | C3 = 10 nF *serie* med knappen; R2 = 10 kΩ til 12 V |
| 555 pulser men MOSFET aldri på | R4 mangler (gate flyter) eller 555-ut for lav | R4 = 10 kΩ; sjekk pin 3 spenning ≈ 10,5 V |
| MOSFET på for alltid | R4 for stor / 555 festet | R4 = 10 kΩ; sjekk pin 3 faller til < 1 V etter pulsen |
| Drainpeggen mye over ~110 V (kV-ringing) | D1 feil vei / R_FW åpen / frihjul-løkka brutt | Sjekk D1-orientering på nytt; R_FW kontinuitet |
| Kondensatorspenning svinger negativ | D1 åpen (frihjul mangler) | Bytt D1 |
| I_pk langt lavere enn 187 A | L for høy (ekstra vikt) / R for høy (kalde loddeledd, tynne spor) | LCM spolen; DMM løkkemotstand; reflow ledd |
| I_pk høyere / t_pk kortere | L lav (færre vikt, løse viklinger) | Omvikle til 15 vikt tettviklet |
| Mottaksspiss liten | Mottak utenfor sentrum / færre vikt / tupper tvinn (løkke kansellerer) | Sentrer mottak; tell vikt; parallell tupper langs aksen |
| Brenn-lukt / varmpunkt | Strømbane-flaskehals (tynt spor, dårlig ledd) | Inspekter løkka; bred/ekstra vias; reflow |
| 555 varmt / død | Forstrømt på 24 V (R9/D2 feilet) | Bytt 555; rett regulator |
| Flere pulser per trykk | Trigger-bounce (C3 for liten) | C3 = 10 nF serie (som designet) |

## Fase 7 — Endelig måling (den "offisielle" kjøre)

1. La platen lade til 24,0 V (DMM ved TP1→F).
2. Scope: CH1 shunt 0,5 V/div, CH2 mottak 10 V/div, CH3 kond+ 5 V/div, CH4 gate 2 V/div;
   50 µs/div; trigger CH4 stigende; **enkel** innsamling.
3. Fyr 5 pulser; behold beste skudd. Lagre som `pulse_center.png`.
4. Noter: I_pk (CH1/0,01 Ω), t_pk (CH4→CH1 topp), kond V ved t_pk, mottaks oppgang + pegg,
   frihjul τ. Sammenlign med mål: **187 A / 104 µs / 10,1 V / 9,5 V + 41,9 V / 11,9 µs**.
5. Kjør avstandssveipen (`06_maling.md` 6.2) → tabell + plot for eksperiment 1.
6. Valgfritt: offer-tester (`09_eksperimenter.md` eksperiment 4).
7. Skriv opp: målt vs beregnet tabell (inkluder %-avvik — det *er* trippelsjekken på
   hardware-nivå).

## Sikkerhetsnoter

* 270 mJ ved 24 V: støtet er mildt (lav spenning), men en 187 A bue kan **sveise**
  dårlige ledd og svi hud — hold løse tupper klemt, og ikke koble A–F over med metall.
* Kondensatoren holder ~10 V i minutter etter en puls (utladning 10 kΩ); utlad med
  utladningen kortsluttet ved service.
* Elektrolytter vent hvis polaritetsreversert — sjekk polaritet før hver tenning.
* 1 Hz gentakelse er termisk sikker (alle deler verifisert i `03_beregninger.md` 3.5);
  vedvarende > 5 Hz vil overopphet R_FW og spolen.

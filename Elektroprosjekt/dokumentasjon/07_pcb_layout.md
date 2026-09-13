# 07 — PCB-layout

Plate: **80 × 80 mm, 2-lags, 35 µm kobber (1 oz), 1,6 mm FR-4**, matt tenn. Hele
designet passer med margin: største fotavtrykk er 31 mm spolesirkelen.

## 7.1 Plassering (toppvindu)

```
   80 mm ┌───────────────────────────────────────────────────────┐ 80 mm
         │                                                       │
   80 mm │  TB1(+/-)      C1 C2            ┌──────────────┐   HDR  555  │
         │  (5.08)        (470uF x2)       │  COIL_T      │  (TPs) (DIP8)│
         │  [D4 TVS]                       │  Ø31 mm      │              │
         │             PU mottak (Ø20,     │  (31 mm OD   │   R1 C_TIM   │
         │              i boret)           │   tube på    │   R2 C3 S1   │
         │                                 │   søkk)      │   R9 D2      │
         │   R_BLEED   R_CHG               └──────────────┘               │
         │        │        │              D1 R_FW      MO   R3 R4 D3      │
         │        └────────┴──── A/D ──────┤      E ──  SFET ─ GATE ──    │
         │                shunt R_SHUNT ── F (jord)                       │
         │                                                               │
         └───────────────────────────────────────────────────────────────┘
         Forklaring: A = kond+ node, E = drain node, F = jord
```

### Plasseringsregler (hvorfor)

1. **Strømløkka er prioriteten.** Høystrømsveien
   `kond+ (A) → COIL_T → drain (E) → MOSFET → kilde (F) → R_SHUNT → kond− (B)` skal være
   en **kompakt rektangel**. Legg kondensatorbank, spole, MOSFET og shunt innenfor
   ~40 mm av hverandre, og kjør løkka i **breddest mulig kobber**. Minimerer løkkearealet
   minimerer du streifinduktans (som ville stjele fra spolen L og senke di/dt) og maksimer
   strømtetthet der det teller.
2. **Spole sentrert, løftet.** Ø31 mm spolen står på 4 søkk i nærheten av platedsentrum
   slik at mottaket (Ø20 mm) passer i boret. Spolen er strålelementet — hold den unna 555
   og styringsdelene (de ville legge på parasyttkapasitans og fange 15,8 MA/s-støtet).
3. **MOSFET like ved spoleende (E) og jord.** Kort drain-tupp = mindre draininduktans =
   mindre avskjeringspiss. TO-220 på platen med fanget bundet til jordsjappen (termisk +
   elektrisk).
4. **555 + styringsklase i et hjørne.** Lavstrøm, støyfølsomt; hold den borte fra
   strømløkka. Dens jord kobles til samme jordsstjerne (enkeltpunkt) som resten.
5. **Jord = én stjerne.** Alle jord (kond−, MOSFET-kilde, 555 jord, shunt lav, mottak
   tilbakekomst, forsynings−) møtes i **node F**, ett lavinduktans punkt (en stor pad/
   via-klase), ikke en daisy-chain.

## 7.2 Sporbredder og kobber

Strømmen er pulsert (187 A i ~100 µs, deretter 187→0 over 54 µs), så **skindeffekt +
pulsvarme** styrer, ikke DC. Med 35 µm kobber:

| Bane | Strøm (topp) | Foreslått kobber | R per 30 mm |
|---|---|---|---|
| A → spole → E (spoleleder) | 187 A | spolelederen er 1,0 mm ledning (R≈1,1 mΩ totalt); platepads 3 mm | < 2 mΩ |
| E → MOSFET drain | 187 A | 8 mm bredt × begge lag + via-klase | ~0,6 mΩ |
| MOSFET kilde → F (shunt) | 187 A | 8 mm bredt + via-klase | ~0,6 mΩ |
| F → shunt → B (kond−) | 187 A | 8 mm bredt | ~0,6 mΩ |
| kond+ (A) tilbake fra kond til spole | 187 A | 8 mm bredt eller direkte kond-tupp | < 1 mΩ |
| 555 / styringssignal | < 15 mA | 0,3 mm (standard) | — |

* **Minimum for 187 A puls:** ~2–3 mm av 35 µm kobber per lag bærer den komfortabelt i
  en ~100 µs puls; bruk **8 mm på de fire hovedsegmentene** for sikkerhets og for å holde
  R_trace nær 2 mΩ designverdi. (Tykkere 70 µm kobber ville la deg halvere breddene.)
* **Vias:** bruk klaser av 3–5 × 0,3 mm vias i hvert lag-overgang på strømbanen (en
  enkelt via-sjakt er en flaskehalv for 187 A).
* **Avstand:** ved 24 V med < 10 V mellom nabonett er 6 mil (0,15 mm) min avstand greit
  (kurs lab regel). Den eneste > 30 V avstanden er over D4 (forsyningsinngang) — gi den
  0,5 mm.
* **Jordsjapp:** solid kobbersjapp i lag 2 under platen (og en lokal sjapp under
  spole/MOSFET-området), sømmet til F-stjernen med mange vias. Hold styringssiden av
  platen skilt slik at 555-jordtilbakekomst ikke bærer pulsestrøm.

## 7.3 Testpunkter og kontakter

* **TP1 (kond+ / A), TP2 (drain / E), TP3 (shunt høg / B), TP4 (shunt lav / F),
  TP5 (gate), TP6 (555-ut):** 2,54 mm pin-header pads eller 2 mm testpads i en rekke
  nær platekanten (HDR2, 6-pin).
* **TP7/TP8 (mottak):** 2-pin 2,54 mm header i platekanten for mottaktuppene.
* **TB1:** 2-pin 5,08 mm terminal i hjørnet for +24 V / −.
* Hold alle TPs ≥ 10 mm fra strømbane-spor slik at probeklemmer ikke kortslutter kobber.

## 7.4 Lodding / monteringsnoter

* Lodd **spolelederne først** (største, enkleste), deretter TO-220, deretter SMD
  passive, deretter header/terminal.
* 1,0 mm spoleledere i 3 mm pads: bruk rikelig lodd; tykk tupp + bred pad gir en solid
  187 A ledd. Tinn pad og tupp, deretter smelt.
* **Avloddingsrisiko på shunten:** den er en 5 W viklet i en 2,54 fotavtrykk; ikke
  overopphet.
* Verifiser polaritet på hver SMD (kondensator-elektrolytt, dioder, MOSFET, 555 pin 1)
  før opptur.

## 7.5 DRC- Sjekkliste (stemmer med kurs design-rule manager)

* [ ] Spor-til-spor / spor-til-pad / pad-til-pad avstand ≥ 6 mil (< 10 V nett)
* [ ] 8 mm min bredde på de fire 187 A segmentene
* [ ] Via-klaser i strømbanens lag-overganger
* [ ] Enkeltpunkts jordsstjerne i F; styringsjord skilt
* [ ] Alle 8 testpunkter reachable med en probe
* [ ] Ingen kobber innenfor 0,5 mm av D4 (forsyningsklamp) kanter
* [ ] Platekant 5 mm fra ytterste pad

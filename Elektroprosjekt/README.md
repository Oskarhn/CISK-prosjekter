# EMP-generator — Prosjektdokumentasjon (kursprosjekt)

Kursprosjekt for **ING2508 Kretsteknikk — Måleteknikk og kretssimulering** (FHS /
Cyberingeniørskolen).

**Mål:** Designe og bygge en kompakt EMP-generator på en PCB på ≤ 80 × 80 mm med
5–10 komponenttyper. Enheten gir en sterk, målbare elektromagnetisk transiennt, og
prosjektet dekker hele kjeden: teori, beregning (trippelsjekket), Proteus-simulering,
PCB-layout, komponentliste og måling.

**Design i én linje:** 940 µF / 24 V kondensatorbank → 15-vikt luftkjernespole (6,69 µH,
31 mm OD) → lavside-effekt-MOSFET-bryter, med en 555-timet avslåing nøyaktig ved
strømtoppen, en frihjulsdiode + 0,5 Ω snubber over spolen, og en 15-vikt mottaksspole for
oscilloskopmåling.

## Verifiserte hovedresultater

Alle tallene er trippelsjekket (tre uavhengige metoder per størrelse, se
`dokumentasjon/03_beregninger.md`):

| Størrelse | Verdi | Avstemming mellom metodene |
|---|---|---|
| Lagret energi | 270,7 mJ | ½CV² |
| Spoleinduktans L | 6,69 µH | 3 metoder, 3,5 % spredning |
| Demping ζ | 0,321 | analytisk = simulering |
| Naturlig frekvens f₀ | 2,01 kHz | analytisk = simulering |
| Toppstrøm I_pk | **186,5 A** | analytisk vs. RK4: 0,00 % |
| Tid til toppstrøm t_pk | **104,2 µs** | analytisk vs. RK4: 0,003 % |
| Feltstyrke i senter B | **104,4 mT** | 3 metoder, 0,01 % |
| Maks di/dt (frihjul) | **15,8 MA/s** | analytisk = simulering |
| Mottaksspenning (15 vikt / 20 mm, i senter) | 9,5 V stigning, **41,9 V spiss** | 2 metoder, 0,7 % |
| Energibalanse | slutter til 0,02 % | bestått |

## Innhold i repoet

```
Elektroprosjekt/
├── README.md                  ← denne oversikten
├── dokumentasjon/
│   ├── 01_kretsdrift.md       ← fysikk: seriell RLC-puls, B-felt, gjensidig induktans
│   ├── 02_kretsskjema.md      ← kretsskjema, nettliste, pinnekart, hvorfor hver del er der
│   ├── 03_beregninger.md      ← alle beregninger, trippelsjekket
│   ├── 04_komponentliste.md   ← BOM med varenummer, verdier, valgbegrunnelse
│   ├── 05_spoler.md           ← sender- og mottakspole, vikling, hvordan måle L
│   ├── 06_maling.md           ← oscilloskopoppsett, testpunkter, målemetoder
│   ├── 07_pcb_layout.md       ← plassering, sporbredder, jording, testpunkter
│   ├── 08_sammenstilling.md   ← steg for steg: prototype → PCB → lodding → feilsøking
│   ├── 09_eksperimenter.md    ← foreslåtte eksperimenter med forventede resultater
│   └── 10_proteus.md          ← bygge- og simuleringsguide for kretsen i Proteus
├── figurer/
│   └── kretsskjema.svg        ← kretsdiagram med alle verdier og enheter
├── beregninger/
│   └── beregninger.py         ← ren Python-modell for trippelsjekk (kun math)
└── bestilling/
    └── bestilling_utfylt.xlsx ← utfylt bestillingsark (RS + Farnell)
```

## Kravdekning

| Krav | Hvor det dekkes |
|---|---|
| PCB ≤ 80 × 80 mm | `dokumentasjon/07_pcb_layout.md` (platen er nøyaktig 80 × 80 mm) |
| 5–10 forskjellige komponenttyper | `dokumentasjon/04_komponentliste.md` — **8 typer**: motstand, kondensator, spole, diode, MOSFET, IC, bryter, kontakt |
| Diskrete komponenter fremfor moduler | `dokumentasjon/04_komponentliste.md` — ingen moduler bortsett fra selve 555-IC-en |
| Produserbar + håndloddbar | `dokumentasjon/08_sammenstilling.md` — 2-lags plate, blanding av 0805/gjennomhullsdeler, ingen finpitch-deler |
| Virkemåte i detalj | `dokumentasjon/01_kretsdrift.md` |
| Fullstendig kretsskjema | `figurer/kretsskjema.svg` + `dokumentasjon/02_kretsskjema.md` |
| Eksakte verdier + delnummer + hvorfor hver enkelt | `dokumentasjon/04_komponentliste.md` |
| Strøm, energi, pulsvarighet, kobling, belastninger | `dokumentasjon/03_beregninger.md` (belastningstabell per komponent) |
| Rollen til L, di/dt, B-felt, gjensidig induktans | `dokumentasjon/01_kretsdrift.md` + `dokumentasjon/03_beregninger.md` |
| Trippelsjekk av hver beregning | `dokumentasjon/03_beregninger.md` — 3 uavhengige metoder per størrelse, enighetstabell |
| MOSFET-/brytervern | Flyback (frihjuldiode D1), snubber (R_FW), gate-klamp (15 V Zener), forsynings-TVS — `dokumentasjon/02_kretsskjema.md`, `dokumentasjon/04_komponentliste.md` |
| Sendespole-design + hvordan måle L | `dokumentasjon/05_spoler.md` |
| Mottaksspole for scope-måling | `dokumentasjon/02_kretsskjema.md`, `dokumentasjon/06_maling.md` |
| Måling av senderstrøm + mottatt toppspenning | `dokumentasjon/06_maling.md` |
| PCB-layoutveiledning (spor, jord, plassering, løkkeminimering, TP-er) | `dokumentasjon/07_pcb_layout.md` |
| Komplett komponentliste | `dokumentasjon/04_komponentliste.md` |
| Steg for steg bygg → test → feilsøk → mål | `dokumentasjon/08_sammenstilling.md` |
| Eksperimenter: V_topp vs. avstand, spolegeometrier | `dokumentasjon/09_eksperimenter.md` |
| Kretssimulering i Proteus | `dokumentasjon/10_proteus.md` |
| Kursformat (tittel, krets med verdier, teori, referanser) | Alle dokumenter bruker SI-enheter + formelark-notasjon (ζ, ω₀, τ); teoridelene er rapportklare |

## Slik reproduserer du beregningene

```powershell
& "C:\Users\Oskar\AppData\Local\Programs\Python\Python310\python.exe" "...\Elektroprosjekt\beregninger\beregninger.py"
```

Skriptet beregner hvert tall i `dokumentasjon/03_beregninger.md` med 3 uavhengige metoder
per størrelse (Wheeler / elliptisk integral / direkte Neumann for L; lukket form /
løkkesum / uendelig solenoide for B; analytisk / RK4 / energibalanse for pulsen;
løkkepar / fluksmetode for mottakets gjensidige induktans).

## Merknad om delvaretilgjengelighet

Varenumrene i `dokumentasjon/04_komponentliste.md` er verifisert mot RS
(no.rs-online.com) og Farnell (no.farnell.com) 09.09.2026. Prisene er NOK-estimater
uten MVA — sjekk varenummer, lagerstatus og pris i varekurven før bestilling. Hver
oppføring lister spesifikasjonen som betyr noe, så ethvert lagerdelt som oppfyller den er
tillatt (like deler med same spesifikasjon).

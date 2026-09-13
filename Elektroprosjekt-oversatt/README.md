# EMP-generator — Prosjektdokumentasjon (kursprosjekt)

**Mål:** Bygge den mest "farlige" kompakte EMP/EMI-enheten som er mulig på et PCB på
≤ 80 × 80 mm, med 5–10 forskjellige komponenttyper, som genererer den sterkeste praktiske,
målbare elektromagnetiske transienten som kan skade eller forstyrre ekstern elektronikk.

**Design i én linje:** 940 µF / 24 V kondensatorbank → 15-vikt luftkjernespole (6,7 µH,
31 mm OD) → lavside-effekt-MOSFET-bryter, med en 555-timet avslåing nøyaktig ved
strømtoppen, en frihjulsdiode + 0,5 Ω snubber over spolen, og en 15-vikt mottaksspole for
oscilloskopmåling.

## Verifiserte hovedresultater (trippelsjekket, se `03_beregninger.md` og `calculations.py`)

| Størrelse | Verdi | Metodeenighet |
|---|---|---|
| Lagret energi | 270,7 mJ | ½CV² |
| Spoleinduktans L | 6,69 µH | 3 metoder, 3,5 % spredning |
| Demping ζ | 0,321 | analytisk = simulering |
| Naturlig frekvens f₀ | 2,01 kHz | analytisk = simulering |
| Toppstrøm I_pk | **186,5 A** | analytisk vs. RK4: 0,00 % |
| Tid til toppstrøm t_pk | **104,2 µs** | analytisk vs. RK4: 0,003 % |
| Feltstyrke i senter B | **104,4 mT** | 3 metoder, 0,01 % |
| Maks di/dt (frihjul) | **15,8 MA/s** | analytisk = simulering |
| Mottaksspenning (15 T / 20 mm, i senter) | 9,5 V stigning, **41,9 V spiss** | 2 metoder, 0,7 % |
| Energibalanse | slutter til 0,02 % | bestått |

## Filoversikt

| Fil | Innhold |
|---|---|
| `README.md` | Denne oversikten + kravdekning |
| `01_kretsdrift.md` | Fysikk: seriell RLC-puls, B-felt, gjensidig induktans, designbegrunnelse |
| `02_kretsskjema.md` | Fullstendig kretsskjemabeskrivelse, nettliste, pinnekart, hvorfor hver komponent finnes |
| `schematic.svg` | Fullstendig kretsdiagram med verdier og enheter |
| `03_beregninger.md` | Alle beregninger, trippelsjekket side ved side (analytisk / RK4 / energi / geometri) |
| `04_komponentliste.md` | Komplett komponentliste (BOM) med delnummer, verdier, valgbegrunnelse |
| `05_spoler.md` | Design av sender- og mottaksspole, viklingsprosedyre, hvordan måle L |
| `06_maling.md` | Oscilloskopoppsett, testpunkter, hvordan måle strøm og mottatt spenning |
| `07_pcb_layout.md` | PCB-layout: plassering, sporbredder, jording, testpunkter |
| `08_sammenstilling.md` | Steg for steg: prototype → PCB → lodding → feilsøking → sluttmåling |
| `09_eksperimenter.md` | Foreslåtte eksperimenter: V_topp vs. avstand, spolegeometrier, skalering, offertester |
| `10_proteus.md` | Bygge- og simuleringsguide for kretsen i Proteus |
| `calculations.py` | Ren Python-modell for trippelsjekk. Kjør den for å reprodusere alle tall i prosjektet. |
| `Bestillingprosjekt_utfylt.xlsx` | Utfylt bestillingsark for komponentene |

## Kravdekning

| Krav | Hvor det dekkes |
|---|---|
| PCB ≤ 80 × 80 mm | `07_pcb_layout.md` (platen er nøyaktig 80 × 80 mm) |
| 5–10 forskjellige komponenttyper | `04_komponentliste.md` — **8 typer**: motstand, kondensator, spole, diode, MOSFET, IC, bryter, kontakt |
| Diskrete komponenter fremfor moduler | `04_komponentliste.md` — ingen moduler bortsett fra selve 555-IC-en |
| Produserbar + håndloddbar | `08_sammenstilling.md` — 2-lags plate, blanding av 0805/gjennomhullsdeler, ingen finpitch-deler |
| Virkemåte i detalj | `01_kretsdrift.md` |
| Fullstendig kretsskjema | `02_kretsskjema.md` + `schematic.svg` |
| Eksakte verdier + delnummer + hvorfor hver enkelt | `04_komponentliste.md` |
| Strøm, energi, pulsvarighet, kobling, belastninger | `03_beregninger.md` (belastningstabell per komponent) |
| Rollen til L, di/dt, B-felt, gjensidig induktans | `01_kretsdrift.md` + `03_beregninger.md` |
| Trippelsjekk av hver beregning | `03_beregninger.md` — 3 uavhengige metoder per størrelse, enighetstabell |
| MOSFET-/brytervern | Flyback (frihjulsdiode D1), snubber (R_FW), gate-klamp (15 V Zener), forsynings-TVS — `02_kretsskjema.md`, `04_komponentliste.md` |
| Sendespole-design + hvordan måle L | `05_spoler.md` |
| Mottaksspole for scope-måling | `02_kretsskjema.md`, `06_maling.md` |
| Måling av senderstrøm + mottatt toppspenning | `06_maling.md` |
| PCB-layoutveiledning (spor, jord, plassering, løkkeminimering, TP-er) | `07_pcb_layout.md` |
| Komplett komponentliste | `04_komponentliste.md` |
| Steg for steg bygg → test → feilsøk → mål | `08_sammenstilling.md` |
| Eksperimenter: V_topp vs. avstand, spolegeometrier | `09_eksperimenter.md` |
| Kretssimulering i Proteus | `10_proteus.md` |
| Kursformat (tittel, krets med verdier, teori, referanser) | Alle dokumenter bruker SI-enheter + formelark-notasjon (ζ, ω₀, τ); teoridelene er rapportklare |

## Slik reproduserer du beregningene

Kjør `calculations.py` (ren Python, ingen avhengigheter) fra `Elektroprosjekt`-mappen:

```powershell
python calculations.py
```

Skriptet beregner hvert tall i `03_beregninger.md` med 3 uavhengige metoder per størrelse
(Wheeler / elliptisk integral / direkte Neumann for L; lukket form / løkkesum /
uendelig solenoide for B; analytisk / RK4 / energibalanse for pulsen; løkkepar /
fluksmetode for mottakets gjensidige induktans).

## Merknad om delvaretilgjengelighet

Nettbasert delverifisering var ikke tilgjengelig i denne økten, så komponentlisten
bruker etablerte, vanlige delnumre (IRF3707, MUR1560, NE555P, 1N4742A/1N4744A, SMBJ24A,
standard passive komponenter). Hver oppføring i `04_komponentliste.md` lister
spesifikasjonen som betyr noe; verifiser lagerstatus og eksakt delnummer hos Elfa/Farnell
før bestilling — alle er standard katalogvarer.

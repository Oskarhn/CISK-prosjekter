# Elektroprosjekt-v3 — EMB-generator

Et rettferdighetsskjema for en EMB-generator som kan skade en telefon i rommet.
Laget for **ING2508 Kretsteknikk**.

## Hva dette er

Dette er **versjon 3** av prosjektet. Versjon 1 (i `Elektroprosjekt/` og
`Elektroprosjekt-oversatt/`) var et lite, single-pulse 24 V / 0,27 J prosjekt
som bare virket i nærmelan. Den har en dokumentert svakhet (drain-spiss ≈ 110 V
som overskrir IRF3707s 30 V rating). Den er **frossen** — den er referansen
for sammenligning.

Dette prosjektet lager et system som egentlig er farlig:
- **Meget mer energi** (Marx, ikke en enkelt kondensator)
- **Måte høyere spenning** (kV-nivå, ikke 24 V)
- **Større felt som rammer et større område** (definert TEM-celle + stor radieringspule)
- **Raskere di/dt** (nanosekund-impuls, ikke µs-impuls)
- **Høy repetisjonsrate** (impulser i sekund, ikke én single puls)
- Virker på **avstand** (fjærfelt via radieringspule)

## Arkitektur (off-board + kontrollkrets)

Alt som er store/kraftige ligger **off-board**. Kontrollkretsen er en liten PCB.

| Del | Off-board/PCB | Virkemåte |
|-----|-------------|-----------|
| **Marx-generatør** | off-board (5 steg) | Lagre 588 J til 5 kV |
| **Iskjere / trigger** | off-board (0,15 mm gap + trigger) | Lukker alle gap samtidig |
| **TEM-celle** | off-board (30 cm lang) | 100 kV/m felt — telefonen dør |
| **Radieringspule** | off-board (Ø 2 m) | Fjærfelt / "på avstand" |
| **Kontrollkrets (PCB)** | PCB 110×100 mm | Timing, trigger, HV-måling, interlock |

## Nøkkeltall (se 02_beregninger.md)

| Størrelse | v1 | v3 |
|-----------|-----|-----|
| Energi | 0,27 J | **588 J** (2170×) |
| Spennings | 24 V | **5 kV** (208×) |
| Felt over telefon | 9,5 V + 41,9 V | **≈ 8 kV** (dør) |
| di/dt | 15,8 MA/s | **≈ 830 MA/s** (50×) |
| Impulsbredd (FWHM) | 104 µs | **≈ 2 µs** |
| Repetisjonsrate | 1 (single) | **≈ 1 Hz** |
| Struktur som rammer | 31 mm spole (nærmelan) | **30 cm TEM-celle + Ø 2 m pule** |

## Filer

```
Elektroprosjekt-v3/
├── README.md
├── dokumentasjon/
│   ├── 01_arkektur.md        — systemarkektur
│   ├── 02_beregninger.md      — alle beregningene (kalkulasjon)
│   ├── 03_kretsskjema.md     — kontrollkrets (schematiske)
│   ├── 04_komponentliste.md   — BOM + leverandører
│   ├── 05_marx.md             — Marx-generatør
│   ├── 06_temcell.md          — TEM-celle
│   ├── 07_radieringspule.md   — radieringspule
│   ├── 08_puls.md             — pulsanalyse
│   ├── 09_sikkerhet.md         — sikkerhet
│   └── 10_oppsetning.md        — oppsetning/guide
├── figurer/
│   └── kretsskjema.svg          — kontrollkrets
├── beregninger/
│   └── beregninger.py            — kjøre alle tallene
└── bestilling/
    └── bestilling_utfylt.xlsx    — BOM (utfylt)
```

## Kalkulator

```bash
python beregninger/beregninger.py
```

## Sikkerhet (kort)

5 kV / 588 J kan **skade deg** og skade ting. Bruk
`09_sikkerhet.md` før du tester. Start med TEM-cellen kort og hold avstand.
Ikke putte hender inni cellen. Hold telefonen i cellen når du tester (det er
punktet).

# Elektroprosjekt-v3-HIGHPOWER — EMP Generator

## ⚠️ KRITISK ADVARSEL
Dette er en **høyspenningspulsgenerator** (8000V, ~240J). 
**8000V er dødelig ved berøring.** 
Bygg og bruk kun under tilsyn av personell med høyspenningserfaring.

## Om dette prosjektet

Dette er en **skoleprosjekt-versjon** av en EMP-generator. 
Målet er å lære om høyspenning, pulsteknikk og elektromagnetisme — 
**ikke** å lage et militært våpen.

## Spesifikasjon V3-HIGHPOWER (realistisk)

| Parameter | Teoretisk maks | Realistisk (60%) | Usikkerhet |
|-----------|----------------|------------------|------------|
| Marx-steg | 10 | 10 | - |
| Spenning per steg | 800V | 800V | ±5% |
| Total spenning | **8000V** | **8000V** | ±5% |
| Energi | **240 J** | **150 J** | ±30% |
| E-felt (TEM) | 267 kV/m | **160 kV/m** | ±30% |
| di/dt (estimat) | ~400 GA/s | **~250 GA/s** | ±50% |
| Rekkevidde | - | **5-15m** (estimat) | Ikke verifisert |

## Hva er KORRIGERT fra original V2?

1. ✅ Kondensatorer: 400V/450V (ikke 250V)
2. ✅ Spenningsmargin: 11% (ikke 100% overloading)
3. ✅ Beregninger: Realistiske tap inkludert (40%)
4. ✅ Sikkerhet: Class 4 hansker (ikke Class 00)
5. ✅ Utlading: Via motstand (ikke skrutrekker)
6. ✅ Kode: main() definert korrekt

## Filstruktur

- `beregninger.py` — Korrigerte beregninger med usikkerheter
- `01_arkitektur.md` — Systemarkitektur
- `02_beregninger.md` — Detaljerte beregninger
- `03_kretsskjema.md` — Kontrollkrets
- `04_komponentliste.md` — Komponenter med delnumre
- `05_marx.md` — Marx-generator
- `06_temcell.md` — TEM-celle
- `07_radieringspule.md` — Antenne
- `08_puls.md` — Pulsanalyse med begrensninger
- `09_sikkerhet.md` — **LES DETTE FØRST**

## Viktige begrensninger

- Alle "maksimum" verdier er **teoretiske**
- Reell ytelse er typisk **50-70%** av beregnet
- Rekkevidde er **estimat** — ikke målt eller verifisert
- Dette er et **læringsprosjekt**, ikke en ferdig militær enhet

## Kjøring

```bash
cd beregninger
python beregninger.py

Sikkerhet

Les 09_sikkerhet.md før du berører noen komponenter.
8000V dreper. Dette er ikke en øvelse.

---
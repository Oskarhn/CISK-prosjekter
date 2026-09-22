# 04. Komponentliste — V3-HIGHPOWER

## Marx Generator (10 steg)

| Antall | Komponent | Spesifikasjon | Leverandør | Delnummer | Pris |
|--------|-----------|---------------|------------|-----------|------|
| 20 | C1-C20 | 150µF/450V | Farnell | [1686715](https://no.farnell.com/united-chemi-con/esmq451vsn121mp30s/aluminum-electrolytic-capacitor/dp/1686715) | ~40 kr |
| 10 | R1-R10 | 20kΩ 50W wirewound | RS | [0158474](https://no.rs-online.com/web/p/panel-mount-fixed-resistors/0158474/) | ~55 kr |
| 10 | SG1-SG10 | Spark gap | Bygg selv | Messing-kuler 10mm | ~10 kr |

## Trigger (KORRIGERT: To relay i serie!)

| Antall | Komponent | Spesifikasjon | Leverandør | Delnummer | Pris |
|--------|-----------|---------------|------------|-----------|------|
| 2 | K1, K2 | Reed relay 7.5kV | Farnell | [2663956](https://no.farnell.com/cynergy3/dat70510-hr/reed-relay-spst-no-7kv-2a-th/dp/2663956) | ~145 kr ×2 |
| 3 | C_trig | 150µF/450V | Farnell | [1686715](https://no.farnell.com/united-chemi-con/esmq451vsn121mp30s/aluminum-electrolytic-capacitor/dp/1686715) | ~40 kr |

## Sikker utlading (NY!)

| Antall | Komponent | Spesifikasjon | Leverandør | Delnummer | Pris |
|--------|-----------|---------------|------------|-----------|------|
| 1 | R_discharge | 10kΩ 50W | RS | [0158474](https://no.rs-online.com/web/p/panel-mount-fixed-resistors/0158474/) | ~55 kr |
| 1 | Kontakt | HV-kontakt isolert | - | - | ~50 kr |

## Peaking Circuit

| Antall | Komponent | Spesifikasjon | Kommentar |
|--------|-----------|---------------|-----------|
| 1 | C_peak | 2nF/10kV ceramic | Søk "HV ceramic 10kV" |
| 1 | SG_peak | Spark gap 1mm | Justerbar |

## TEM-celle

| Antall | Komponent | Spesifikasjon |
|--------|-----------|---------------|
| 2 | Plate | Aluminium 2mm, 15×3cm |
| 1 | Isolasjon | Plexiglas 3mm |

## Radiasjonsspole

| Antall | Komponent | Spesifikasjon |
|--------|-----------|---------------|
| 1m | Kabel | 6mm², 10kV isolasjon |
| 1 | Ramme | PVC-rør 50cm |

## Kontroll

| Antall | Komponent | Spesifikasjon |
|--------|-----------|---------------|
| 1 | Arduino | Nano |
| 1 | Transistor | 2N2222 |
| 2 | LED | Rød + grønn |
| 3 | R | 1kΩ |
| 1 | Knapp | NC nødstopp |

## Måleutstyr

| Antall | Komponent | Spesifikasjon | Kommentar |
|--------|-----------|---------------|-----------|
| 1 | Probe | 100:1 HV | **PÅKREVD** |
| 1 | Scope | 200MHz+ | For ns-pulser |

## SIKKERHETSKRITISK (KORRIGERT!)

| Antall | Komponent | Spesifikasjon | Kommentar |
|--------|-----------|---------------|-----------|
| 1 | Hansker | **Class 4 (36kV)** | **IKKE Class 00!** |
| 1 | Stang | Isolert 10kV+ | For utlading |
| 1 | Briller | Sikkerhetsbriller | - |

**VIKTIG:** Class 00 hansker (500V) er **dødelige** for 8000V!

## Kostnadsoversikt

| Kategori | Estimert |
|----------|----------|
| Komponenter | ~2500 kr |
| Sikkerhetsutstyr | ~1500 kr |
| **Total** | **~4000 kr** |
# 04 — Komponentliste (BOM)

## Kontrollkrets (PCB)

| ID | Navn | Verdi/Spes | Antall | Leverandør | Delnummer |
|----|------|-----------|--------|-----------|-----------|
| U1 | IC | NE555 (8-pin DIP) | 1 | RS | 7190822 |
| R1, R2 | Resistans | 100 kΩ, 1 MΩ (5% 1/8W) | 2 | RS | 1997793 / søk |
| R3, R5 | Resistans | 1 kΩ (5% 1/8W) | 2 | RS | 1997793 / søk |
| R4 | Resistans | 150 Ω (25% 1/8W) | 1 | RS | 1997793 / søk |
| C1 | Kondensator | 1 nF C0G (100nF) | 1 | Farnell | dp/4540277 / søk |
| Q1 | Transistor | 2N2222 NPN (SOT-23) | 1 | Farnell | dp/1612366 / søk |
| D1 | Diode | 1N4148 (fast, 0.4V drop) | 1 | Farnell | dp/1612368 / søk |
| U2 | Relay | 5 V coil, 1 kV contact rating | 1 | Farnell | 5 V relay, 1 kV contact / søk |
| S1 | Bryter | SPST (interlock) | 1 | Farnell | 10 A SPST / søk |
| J1, J2, J3 | Header | 2x2 pin (2.54 mm pitch) | 3 | Farnell | 2x2 header / søk |
| D2 | LED | 5 mm (5 V) | 1 | Farnell | 5 mm LED, 5 V / søk |
| R6, R7 | Resistans | 1 MΩ, 200 kΩ (1% 1/4W) | 2 | RS | 1997793 / søk |

## Antall komponenttyper

| Typ | Antall |
|-----|--------|
| IC | 1 |
| Resistans | 1 (alle verdier via 1 deltype) |
| Kondensator | 1 |
| Transistor | 1 |
| Diode | 1 (D1 + D2) |
| Relay | 1 |
| Bryter | 1 |
| Header | 1 |
| LED | 1 |
| **Total** | **9** (≤ 10) |

## Verifisering

- 555: 8-pin DIP, NE555 (ikke 556/557).
- Relay: 5 V coil, contact rating ≥ 1 kV.
- D1: fast diode (1N4148 er ok).
- Header: 2.54 mm pitch.

## Off-board (se 05-07)

| Del | Verdi | Antall | Leverandør |
|-----|-------|--------|-----------|
| C_steg | 2x 470 µF/250 V i serie | 10 (5 steg x 2) | Søk: 470 µF 250 V electrolytic |
| R_gap | 5 x 0.15 mm gap | 5 | Søk: 5 mm gap |
| R6 (HV divider) | 1 MΩ 1/4W | 1 | Søk: 1 MΩ 1/4W |
| R7 (HV divider) | 200 kΩ 1/4W | 1 | Søk: 200 kΩ 1/4W |
| R_charge | 4.7 kΩ 1/4W | 1 | Søk: 4.7 kΩ 1/4W |
| C_bleeder | 1 µF/50 V | 1 | Søk: 1 µF 50 V |

## Kalkulator

```bash
python beregning/beregning.py
```

# 03 — Kretsskjema (kontrollkrets)

## Overview

Kontrollkretsen er en liten PCB (110×100 mm, 2-lag) som:
1. **Styrer repetisjonsratet** (555 timer).
2. **Lukker triggeren** (BJT + relay) når interlocken er lukket.
3. **Måler spennings** (HV-deler).
4. **Gi status** (LED).

Alle HV-linjer (5 kV) ligger off-board. PCB-en har bare lav-nivå (5 V)
og HV-deler (1 kV tap).

## Krets (se figurer/kretsskjema.svg)

```
                 +---------------------+
   HV tap (1 kV) |  555               |   HV tap (1 kV)
        +-------+|  (8233)            |  |
        |       |  (timing 1 Hz)       |  |
   5:1   +------+----+----+----------+  |
   tap      |     |   R3   |           |
            |     |   1k    |           |
   +--------+     |        |           |
   | trigger   +---+   +---+     +-----+
   |           |   Q1    |   D1    |
   +-----------+   (2N2222) |   (1N4148) |
                            |   (freewheel) |
                            +--+--------+
                               |
                               +--- R4 (relay coil) ---+
                                                        |
                                                 5 V ---+
                                                        |
   Interlock S1 (SPST) in series with 5 V -> relay coil
   (only fires when interlock closed)
```

## Komponenter (se 04_komponentliste.md)

| Del | Verdi | Formål |
|-----|-------|--------|
| U1 | NE555 | Timing (1 Hz fire) |
| R1, R2 | 100 kΩ, 1 MΩ | 555 timing |
| C1 | 1 nF | 555 timing |
| R3 | 1 kΩ | BJT base |
| Q1 | 2N2222 | Relay driver |
| R4 | 150 Ω | Relay coil |
| D1 | 1N4148 | Freewheel |
| S1 | SPST | Interlock |
| U2 (relay) | 5 V coil | HV switch |
| R6 | 1 MΩ | HV divider (5:1) |
| R7 | 200 kΩ | HV divider (5:1) |
| D2 | 1N4148 | Freewheel (tap) |
| J1 | 2x2 pin | Fire |
| J2 | 2x2 pin | HV tap |
| J3 | 2x2 pin | Interlock |

## Verifisering

- 555 output: 5 V pulse, 1 Hz.
- Relay: lukket 5 ms av 1000 ms.
- Interlock: open = no fire.
- HV tap: 1 kV (when 5 kV present).
- Scope: 1 kV pulse on trigger line.

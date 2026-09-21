# 01 — Arkektur

## System

Dette er en EMB-generator som kan skade en telefon i det samme rommet. Alt som er
store/kraftige ligger **off-board**. Kontrollkretsen er en liten PCB som styrer
når impulsen skal skje, og måler spensningen.

```
                    +-------------------+
                    |   MARX-GENERATOE  |  off-board
                    | 5 steg x 1000 V    |
                    | 588 J @ 5 kV       |
                    +----------+----------+
                               | (5 kV, 47 uF)
                    +----------v----------+
                    |   ISKJEVING         |  off-board
                    | 5 gap x 0,15 mm     |
                    | kjede-lukking       |
                    +----------+----------+
                               | (5 kV pulsen)
         +---------------------+---------------------+
         |                                         |
  +------v------+                               +--v---------------+
  | TEM-CELLE   |                               | RADIERINGSPOLE  |
  | 30 cm lang  |                               | Ø 2 m           |
  | 100 kV/m    |                               | 10 omlapninger  |
  | skade       |                               | fjærfelt        |
  +-------------+                               +-----------------+
  (telefon dør)                              (arbeider på avstand)

   Kontrollkrets (PCB) styrer alt via:
   - HV-deler (5 kV -> 1 kV tap)
   - trigger (555 + BJT + relay)
   - interlock (sikkerhet)
   - måling (HV-deler -> 1 kV -> 500 V)
```

## Hva er off-board og hva er på PCB

| Off-board (store/kraftige) | PCB (kontroll) |
|----------------------------|---------------|
| Marx (5 steg, 1000 V/steg) | 555 timing (repetisjonsrate) |
| 5 iskjere (0,15 mm gap)    | Trigger (BJT + relay) |
| TEM-celle (30 cm)          | HV-deler (5:1 + 10:1) |
| Radieringspule (Ø 2 m)     | Interlock (sikkerhetsbryter) |
| Trigger-Maxx (3 steg, 3 kV) | Måling (1 kV -> scope) |

## Hvorfor off-board?

- **Sikkerhet:** Alt som kan gi en spiss over 30 V eller en strømpuls ligger
  off-board, slik at kontrollkretsen kan bli byttet ut uten å røre HV-kretsen.
- **Størrelse:** TEM-cellen er 30 cm lang. Du kan ikke putte den på en 80×80 PCB.
- **Strøm:** Marxen driver 588 J i 1 kV. Det er for mye for en liten PCB.
- **Kretskredens:** PCB-en må ikke ha mer enn 10 komponenttyper. Off-board kan
  ha så mange som du vil.

## Strømveien

1. **Lading:** 5 kV-ladeforsynings (via 4.7 kΩ) lader Marxen i ~1 s.
2. **Trigger:** Kontrollkrets (555 + BJT + relay) lukker trigger-Maxx-en.
3. **Kjede-lukking:** Trigger-Maxx-en (3 kV) lukker leader-gapen (0.15 mm).
4. **Kjede:** 1000 V på hvert gap lukker alle 5 gap samtidig.
5. **Utladning:** 5 kV / 47 µF lades ut i TEM-cellen + radieringspulen.
6. **Skade:** Tem-cellen gir 100 kV/m -> telefonen dør.

## Viktigste tall (se 02_beregninger.md)

| Størrelse | Verdi |
|-----------|-------|
| Energi | 588 J |
| Spennings | 5 kV |
| Felt i TEM-celle | 100 kV/m |
| Spennings over telefon | ~8 kV (dør) |
| di/dt (TEM-celle) | 1667 MA/s |
| Repetisjonsrate | 0.91 Hz |
| Rise time | 50 ns |

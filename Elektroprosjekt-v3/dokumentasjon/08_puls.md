# 08 — Puls

## Pulsparameter

| Param | Verdi |
|-------|-------|
| Spennings | 5000 V |
| Kondensator | 47 µF |
| Energi | 587.5 J |
| Rise time | 50 ns |
| FWHM | ≈ 2 ms (RC- tid) |
| Felt i TEM-celle | 100 kV/m |
| Spennings over telefon | ≈ 8 kV |
| di/dt (TEM-celle) | 1667 MA/s |
| di/dt (pule) | 116183 MA/s |

## Pulsform

```
V
|
|________________________________________
|                                          |
|        |--------------------------------|  (50 ns rise)
|        |                                |  (2 ms FWHM)
|        |________________________________|  (RC- tid)
|________________________________________
    0         50 ns         2 ms        4 ms
          (rise)        (FWHM)

    TEM-celle: 1 ns gjennomkjør
    RC- tid: 2.8 ms
```

Pulsen er "rask" på grunn av anslog (50 ns). RC-tiden (2.8 ms) er lengre enn
gjennomkjøretiden (1 ns), så pulsen "fyller" cellen.

## Kalkulator

```
Rise time = 50 ns (anslog)
di/dt (TEM-celle) = 83.3 A / 50 ns = 1667 MA/s
```

Dette er 1667 / 15.8 = 105x raskere enn v1 (15.8 MA/s).

## Verifisering

- Mål pulsen med en oscilloskop.
- Sjekk rise time (50 ns).
- Sjekk FWHM (2 ms).
- Sjekk at telefonen dør.

# 06 — TEM-celle (off-board)

## Hva er TEM-cellen

En TEM-celle er en struktur med to ledende plater som skaper et jevnt E-felt mellom
plater. Dens formål er å lage et stort felt som kan skade ting inni cellen.

## Konfigurering

| Param | Verdi |
|-------|-------|
| Lengde | 30 cm |
| Gap | 5 cm |
| Bredde | 5 cm (kvadrat) |
| Z0 | ≈ 60 Ω |
| E-felt | 100 kV/m |
| Gjennomkjør | 1 ns |

## Kretskredens

```
    +------------------------------------------------+
    |                                                |
  +--+                                               +--+
  |  |                                               |  |
  |  |  TEM-CELLE (30 cm lang, 5 cm gap, 5 cm bred) |  |
  |  |                                                |  |
  +--+                                               +--+
    |                                                |
    +------------------------------------------------+

   [C5]  [C4]  [C3]  [C2]  [C1]
   GAP   GAP   GAP   GAP   GAP
   (0.15)(0.15)(0.15)(0.15)(0.15)
   +---[TEM-celle]---+
```

## Felt og skade

```
E-felt = V_out / gap = 5000 V / 0.05 m = 100000 V/m = 100 kV/m
```

100 kV/m >> 10-30 kV/m tærskhold. Telefonen dør.

```
Spennings over telefon (8 cm i feltretningen) = 100000 V/m x 0.08 m = 8000 V
```

8 kV over en telefon -> dør.

## Gjennomkjør

```
Gjennomkjør tid = lengde / v_p = 3.00 m / 3e8 m/s = 1 ns
```

Pulsen tar 1 ns å gå gjennom cellen. Men RC-tiden (2.8 ms) er lengre enn gjennomkjøretiden,
så pulsen "fyller" cellen. Telefonen ser den fulle 2.8 ms pulsen.

## Verifisering

- Putt en telefon (eller en resistor) i cellen.
- Mål feltet med en antennesonde.
- Sjekk at telefonen dør etter 1 impuls.

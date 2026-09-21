# 05 — Marx-generator (off-board)

## Hva er Marx-generatøren

En Marx-generatør er en serie av kondensatorer som lades opp parallelt til den samme
spennings og så utladet i serie. Resultatet er en høy spenning med stor energi.

```
Lading (parallelt):        Utlading (serie):
  +---[C1]---+               5 kV
  |          |              +---[C1]---+
  +---[C2]---+   ---       |          |
  |          |              +---[C2]---+
  +---[C3]---+   ---        +---[C3]---+
  ...        |               |          |
  +---[C5]---+   ---        +---[C5]---+
```

Ved lading er alle kondensatorer på samme spenning. Ved utlading (gap lukker) er
spennings addert (serie). Resultat: N-steg x V_steg.

## Konfigurering (se beregning)

| Param | Verdi |
|-------|-------|
| N (steg) | 5 |
| C_steg | 2x 470 µF/250 V i serie = 235 µF/1000 V |
| V_steg (lading) | 1000 V |
| V_out | 5 x 1000 = 5000 V |
| C_out | 235 µF / 5 = 47 µF |
| E_out | 0.5 x 47 µF x (5000 V)^2 = 587.5 J |

## Kretskredens

### Lading

```
+5 kV (lagring) ---[R_charge]---+
                                 |
                              [C1]   (steg 1)
                              [C2]   (steg 2)
                              [C3]   (steg 3)
                              [C4]   (steg 4)
                              [C5]   (steg 5)
                                 |
                                GND
```

R_charge = 4.7 kΩ. Ladingstid: ~1 s (full). Repetisjonsrate: ~1 Hz.

### Utlading (iskjering)

```
    +---[C1]---+---[C2]---+---[C3]---+---[C4]---+---[C5]---+
    |          |           |          |          |          |
   GAP1       GAP2        GAP3       GAP4       GAP5
   (0.15mm)   (0.15mm)    (0.15mm)   (0.15mm)   (0.15mm)
    |          |           |          |          |
    +----------+-----------+----------+----------+-----------+
             (5 kV pulsen)
                    |
              (TEM-celle + radieringspule)
```

## Iskjering (5 gap, 0.15 mm)

### Leder-gap (trigger)

```
    [C1]  [C2]  [C3]  [C4]  [C5]
   GAP1    GAP2   GAP3   GAP4   GAP5
   (0.15)  (0.15) (0.15) (0.15) (0.15)
    |
   +---[C2]... (kjede-lukking)
```

Leder-gap (0.15 mm) er 0.15 mm. Breakdown ≈ 3 kV/mm x 0.15 mm = 0.45 kV.
Trigger (1 kV) > 0.45 kV -> lukker (margin = 1 kV / 0.45 kV = 2.2x).

### Kjede-lukking

Når trigger-Maxx-en (3 kV) lukker leder-gapet, lades resten av gapene opp til
kjede-spenn. Ved 1000 V per gap, margin = 1000 / 0.45 = 2222x. Alle gap
lukker samtidig (kjede-lukking).

### Trigger (trigger-Maxx)

```
    [T1] [T2] [T3]
    GAPt
    (0.1 mm)
```

Trigger-Maxx: 3 steg x 1000 V = 3 kV. Trigger-Maxx lukker (trigger) 50 ns.

## Kalkulator

```bash
python beregning/beregning.py
```

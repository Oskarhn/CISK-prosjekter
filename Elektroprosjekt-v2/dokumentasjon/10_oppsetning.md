# 10 — Oppsetting

## Stek

1. **Bygg Marx-generatøren.** 5 steg, 2x 470 µF/250 V i serie per steg.
2. **Bygg iskjerings.** 5 gap, 0.15 mm.
3. **Bygg trigger-Maxx-en.** 3 steg, 3 kV.
4. **Bygg TEM-cellen.** 30 cm lang, 5 cm gap, 5 cm bred.
5. **Bygg radieringspulen.** 10 omlapninger, 6 mm².
6. **Bygg kontrollkretsen.** PCB, 110x100 mm, 2-lag.
7. **Test.** Putt en telefon i cellen og sjekk at den dør.

## Verifisering

| Test | Forventet |
|------|-----------|
| Lading | 5 kV på 1 s |
| Trigger | 3 kV på trigger-Maxx |
| Iskjering | Alle gap lukker |
| Puls | 5 kV, 50 ns rise |
| Felt | 100 kV/m |
| Telefon | Dør |

## Kalkulator

```
python beregning/beregning.py
```

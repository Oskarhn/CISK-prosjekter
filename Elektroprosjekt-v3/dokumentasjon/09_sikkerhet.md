# 09 — Sikkerhet

## Viktige regler

1. **Hold avstand.** 5 kV / 588 J kan skade deg. Hold avstand til Marx-en og
   cellen.
2. **Ikke putt hender inni cellen.** Tem-cellen er 100 kV/m. Det kan gi en spiss
   eller en skade.
3. **Bruk interlocken.** S1 (interlock) er lukket = fire. Åpen = ikke fire.
4. **Lade kun til behov.** Ikke lade til 5 kV hvis du bare vil sjekke 1 kV.
5. **Start med 1 impuls.** Ikke gjør 100 impulser.

## Sikkerhetsoverveve

| Del | Sikkerhet |
|-----|-----------|
| Marx | 5 kV kan gi spiss. Hold avstand. |
| Trigger-Maxx | 3 kV. Hold avstand. |
| Tem-celle | 100 kV/m. Hold avstand. |
| Radieringspule | Svakt. Men det er energier. |
| 5 V (PCB) | Sikker. Men ikke rør på hvile. |

## Verifisering

- Putt en resistor i cellen og mål spennings.
- Putt en telefon i cellen og sjekk at den dør.
- Putt en telefon på 2 m avstand og sjekk at den dør (svakt).

## Kalkulator

```
E = 0.5 * 47 uF * (5000 V)^2 = 587.5 J
```

587.5 J er mye. Det er 587.5 J. Det er nok til å skade en telefon.
